from typing import List
from crewai import Agent
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool
from tools.youtube_search_tools import YoutubeVideoSearchTool


class ResearchAgents():

    def __init__(self):
        self.searchInternetTool = SerperDevTool()
        self.youtubeSearchTool = YoutubeVideoSearchTool()
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    def research_manager(self, technologies: List[str], businessareas: List[str]) -> Agent:
        return Agent(
            role="Research Manager",
            goal=f"""Generate a list of JSON objects containing the urls for 3 recent blog articles and 
                the url and title for 3 recent YouTube videos, for each technology in each business area.
             
                Technologies: {technologies}
                Business Areas: {businessareas}

                Important:
                - The final list of JSON objects must include all technologies and business areas. Do not leave any out.
                - If you can't find information for a specific industry or business area, fill in the information with the word "MISSING".
                - Do not generate fake information. Only return the information you find. Nothing else!
                - Do not stop researching until you find the requested information for each business area in each technology.
                - All the technologies and business areas exist so keep researching until you find the information for each one.
                - Make sure you each researched business area for each technology contains 3 blog articles and 3 YouTube videos.
                """,
            backstory="""As a Research Manager, you are responsible for aggregating all the researched information into a list.""",
            llm=self.llm,
            tools=[self.searchInternetTool, self.youtubeSearchTool], # TODO: Add tools
            verbose=True,
            allow_delegation=True
        )

    def research_agent(self) -> Agent:
        return Agent(
            role="Research Agent",
            goal="""Look up the specific business areas for a given technology and find urls for 3 recent blog articles and 
                the url and title for 3 recent YouTube videos in the specified business area. It is your goal to return this collected 
                information in a JSON object""",
            backstory="""As a Research Agent, you are responsible for looking up specific business areas 
                within a technology and gathering relevant information.
                
                Important:
                - Once you've found the information, immediately stop searching for additional information.
                - Only return the requested information. NOTHING ELSE!
                - Do not generate fake information. Only return the information you find. Nothing else!
                """,
            tools=[self.searchInternetTool, self.youtubeSearchTool], # TODO: Add tools
            llm=self.llm,
            verbose=True
        )