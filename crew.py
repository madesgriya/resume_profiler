from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import (
    FileReadTool,
    ScrapeWebsiteTool,
    PDFSearchTool,
    SerperDevTool
)
@CrewBase
class ResumeProfiler():
    """ResumeProfiler crew"""
    def __init__(self):
        self.agents: List[BaseAgent]
        self.tasks: List[Task]
        self.search_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()
        self.read_resume = FileReadTool(file_path='./fake_resume.pdf')
        self.semantic_search_resume = PDFSearchTool(pdf='./fake_resume.pdf')

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            tools = [self.scrape_tool, self.search_tool],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ResumeProfiler crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
