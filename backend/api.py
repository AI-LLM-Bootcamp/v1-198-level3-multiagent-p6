from flask import Flask, jsonify, request, abort
from uuid import uuid4
from threading import Thread
from crews import TechnologyResearchCrew
from log_manager import append_event, outputs, outputs_lock, Event
from datetime import datetime
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

def kickoff_crew(input_id, technologies: list[str], businessareas: list[str]):
    print(f"Running crew for {input_id} with technologies {technologies} and businessareas {businessareas}")

    results = None
    try:
        company_research_crew = TechnologyResearchCrew(input_id)
        company_research_crew.setup_crew(
            technologies, businessareas)
        results = company_research_crew.kickoff()

    except Exception as e:
        print(f"CREW FAILED: {str(e)}")
        append_event(input_id, f"CREW FAILED: {str(e)}")
        with outputs_lock:
            outputs[input_id].status = 'ERROR'
            outputs[input_id].result = str(e)

    with outputs_lock:
        outputs[input_id].status = 'COMPLETE'
        outputs[input_id].result = results
        outputs[input_id].events.append(
            Event(timestamp=datetime.now(), data="Crew complete"))

@app.route('/api/multiagent', methods=['POST'])
def run_crew():
    data = request.json
    if not data or 'technologies' not in data or 'businessareas' not in data:
        abort(400, description="Invalid request with missing data.")
 
    input_id = str(uuid4())
    technologies = data['technologies']
    businessareas = data['businessareas']
    
    thread = Thread(target=kickoff_crew, args=(input_id, technologies, businessareas))
    thread.start()
    
    # return jsonify({"status": "success"}), 200
    return jsonify({"input_id": input_id}), 200


@app.route('/api/multiagent/<input_id>', methods=['GET'])
def get_status(input_id):
    with outputs_lock:
        output = outputs.get(input_id)
        if output is None:
            abort(404, description="Output not found")

     # Parse the output.result string into a JSON object
    try:
        result_json = json.loads(output.result)
    except json.JSONDecodeError:
        # If parsing fails, set result_json to the original output.result string
        result_json = output.result

    return jsonify({
        "input_id": input_id,
        "status": output.status,
        "result": result_json,
        "events": [{"timestamp": event.timestamp.isoformat(), "data": event.data} for event in output.events]
    })

if __name__ == '__main__':
    app.run(debug=True, port=3001)