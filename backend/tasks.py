from crewai import Task, Agent
from textwrap import dedent


from log_manager import append_event
from models import BusinessareaInfo, BusinessareaInfoList


class ResearchTasks():

    def __init__(self, input_id):
        self.input_id = input_id

    def append_event_callback(self, task_output):
        print(f"Appending event for {self.input_id} with output {task_output}")
        append_event(self.input_id, task_output.exported_output)

    def manage_research(self, agent: Agent, technologies: list[str], businessareas: list[str], tasks: list[Task]):
        return Task(
            description=dedent(f"""Based on the list of technologies {technologies} and the business areas {businessareas},
                use the results from the Research Agent to research each business area in each technology.
                to put together a json object containing the URLs for 3 blog articles, the URLs and title 
                for 3 YouTube interviews for each business area in each technology.
                               
                """),
            agent=agent,
            expected_output=dedent(
                """A json object containing the URLs for 3 blog articles and the URLs and 
                    titles for 3 YouTube interviews for each business area in each technology."""),
            callback=self.append_event_callback,
            context=tasks,
            output_json=BusinessareaInfoList
        )

    def technology_research(self, agent: Agent, technology: str, businessareas: list[str]):
        return Task(
            description=dedent(f"""Research the business areas {businessareas} for the {technology} technology. 
                For each business area, find the URLs for 3 recent blog articles and the URLs and titles for
                3 recent YouTube videos in each business area.
                Return this collected information in a JSON object.
                               
                Helpful Tips:
                - To find the blog articles names and URLs, perform searches on Google such like the following:
                    - "{technology} [BUSINESS AREA HERE] blog articles"
                - To find the youtube videos, perform searches on YouTube such as the following:
                    - "{technology} in [BUSINESS AREA HERE]"
                               
                Important:
                - Once you've found the information, immediately stop searching for additional information.
                - Only return the requested information. NOTHING ELSE!
                - Do not generate fake information. Only return the information you find. Nothing else!
                - Do not stop researching until you find the requested information for each business area in the technology.
                """),
            agent=agent,
            expected_output="""A JSON object containing the researched information for each business area in the technology.""",
            callback=self.append_event_callback,
            output_json=BusinessareaInfo,
            async_execution=True
        )