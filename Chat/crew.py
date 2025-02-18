from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool

# Read File
file_read_tool = FileReadTool()
#or
file_read_tool = FileReadTool(file_path='/home/aturzone/Dynamik/Chat/Data/ProjectData.txt')

@CrewBase
class LiveChat():
        """Configs crew for live chat"""
        agents_config = 'Configs/agents.yaml'
        tasks_config = 'Configs/tasks.yaml'
        

        @agent
        def Intent_Detection_Agent(self) -> Agent:
            return Agent(
                config=self.agents_config['Intent_Detection_Agent'],
                #tools=[file_read_tool]
                verbose=False,
                memory=False
            )
        
        @agent
        def Manager_Agent(self) -> Agent:
            return Agent(
                config=self.agents_config['Manager_Agent'],
                verbose=False,
                memory=False
            )
            
        @agent
        def Assistant_Agent(self) -> Agent:
            return Agent(
                config=self.agents_config['Assistant_Agent'],
                verbose=False,
                memory=False
            )
        
        @agent
        def Editor_Agent(self) -> Agent:
            return Agent(
                config=self.agents_config['Editor_Agent'],
                verbose=False,
                memory=False
            )
            
        @task
        def intent_Detection_task(self) -> Task:
            return Task(
                config=self.tasks_config['intent_Detection_task'],
                agent=self.Intent_Detection_Agent()
            )
            
        @task
        def task_Analiyze_task(self) -> Task:
            return Task(
                config=self.tasks_config['task_Analiyze_task'],
                agent=self.Assistant_Agent()
            )
        
        @task
        def risks_Analysis_task(self) -> Task:
            return Task(
                config=self.tasks_config['risks_Analysis_task'],
                agent=self.Assistant_Agent()
            )
        
        @task
        def editor_task(self) -> Task:
            return Task(
                config=self.tasks_config['editor_task'],
                agent=self.Editor_Agent()
            )
            
        @crew
        def crew(self) -> Crew:
            return Crew(
                    agents=self.agents,
                    tasks=self.tasks,
                    process=Process.hierarchical,
                    verbose=False
            )

def kickoff(self, inputs):
    
    task = self.intent_Detection_task()
    intent_result = task.run(inputs)
    
    task = self.manager_task()
    result = task.run({"user_input": inputs['user_message'], "intent_result": intent_result})
    
    
    return result