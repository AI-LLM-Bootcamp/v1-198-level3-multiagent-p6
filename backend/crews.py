from langchain_openai import ChatOpenAI
from log_manager import append_event
from agents import ResearchAgents
from tasks import ResearchTasks
from crewai import Crew

class TechnologyResearchCrew:
    def __init__(self, input_id: str):
        self.input_id = input_id
        self.crew = None
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    def setup_crew(self, technologies: list[str], businessareas: list[str]):
        print(f"""Setting up crew for
        {self.input_id} with technologies {technologies}
        and businessareas {businessareas}""")

        # DONE: SETUP AGENTS
        agents = ResearchAgents()

        research_manager = agents.research_manager(technologies, businessareas)
        research_agent = agents.research_agent()
  
        # DONE: SETUP TASKS
        tasks = ResearchTasks(input_id=self.input_id)

        technology_research_tasks = [
            tasks.technology_research(research_agent, technology, businessareas)
            for technology in technologies
        ]

        manage_research_task = tasks.manage_research(
            research_manager, technologies, businessareas, technology_research_tasks)
        
        # DONE: CREATE CREW
        self.crew = Crew(
            agents=[research_manager, research_agent],
            tasks=[*technology_research_tasks, manage_research_task],
            verbose=2,
            )

    def kickoff(self):
        if not self.crew:
            print(f"""Crew not found for 
            {self.input_id}""")
            return
        
        append_event(self.input_id, "CREW STARTED")
        
        try:
            print(f"""Running crew for 
            {self.input_id}""")
            results = self.crew.kickoff()
            append_event(self.input_id, "CREW COMPLETED")
            return results

        except Exception as e:
            append_event(self.input_id, "CREW FAILED")
            return str(e)