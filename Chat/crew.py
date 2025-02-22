from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool

# Read File
@CrewBase
class LiveChat():
    """Configs crew for live chat"""
    agents_config = 'Configs/agents.yaml'
    tasks_config = 'Configs/tasks.yaml'
    
    file_read_tool = FileReadTool(file_path='/home/aturzone/Dynamik/Chat/Data/ProjectData.txt')
    # خواندن داده‌ها از فایل
    with open("/home/aturzone/Dynamik/Chat/Data/ProjectData.txt", "r") as file:
        file_content = file.read()

    # مطمئن شوید که داده‌ها به درستی خوانده شده‌اند
    print(f"File content: {file_content[:100]}")  # نمایش چند کاراکتر اول از فایل

    @agent
    def Intent_Detection_Agent(self) -> Agent:
        return Agent(
            config=self.agents_config['Intent_Detection_Agent'],
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

    @agent
    def Optimizer_Agent(self) -> Agent:
        return Agent(
            config=self.agents_config['OptimizerAgent'],
            tools=[self.file_read_tool],  # ابزار برای خواندن فایل
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

    @task
    def optimizer_task(self) -> Task:
        return Task(
            config=self.tasks_config['optimizer_task'],
            agent=self.Optimizer_Agent()
        )

    @task
    def manager_task(self) -> Task:
        return Task(
            config=self.tasks_config['manager_task'],  # فرض می‌کنیم در فایل tasks.yaml تنظیم شده
            agent=self.Manager_Agent()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.Optimizer_Agent(),
                self.Intent_Detection_Agent(),
                self.Manager_Agent(),
                self.Editor_Agent(),
            ],
            tasks=[
                self.optimizer_task(),
                self.intent_Detection_task(),
                self.manager_task(),
                self.editor_task()
            ],
            process=Process.hierarchical,
            verbose=False
        )

    # تعریف متد analyze_and_edit_output
    def analyze_and_edit_output(self, manager_output, inputs):
        """
        بررسی کیفیت خروجی و ارسال به ویرایشگر در صورت نیاز
        """
        is_good_enough = self.analyze_quality(manager_output)  # فرض می‌کنیم که متدی برای تحلیل کیفیت داریم

        if not is_good_enough:
            # ارسال به EditorAgent برای ویرایش
            task = self.editor_task()
            edited_output = task.run({
                'output_to_edit': manager_output, 
                'project_data': inputs['project_data']
            })
            return edited_output
        return manager_output
    
    # متد kickoff که حالا خروجی ManagerAgent را بررسی می‌کند
    def kickoff(self, inputs):
        # چاپ ورودی‌ها برای بررسی
        print(f"Inputs in kickoff: {inputs}")

        if not isinstance(inputs, dict):
            print(f"Error: inputs is not a dictionary, it is {type(inputs)}")
            return {"error": "Invalid inputs format"}

        # مرحله اول: پردازش ورودی توسط OptimizerAgent
        task = self.optimizer_task()
        optimized_input = task.run(inputs)

        # مرحله دوم: پردازش ورودی توسط IntentDetectionAgent
        task = self.intent_Detection_task()
        intent_result = task.run({"optimized_input": optimized_input})

        # مرحله سوم: پردازش ورودی توسط ManagerAgent
        task = self.manager_task()
        result = task.run({
            "user_input": optimized_input['user_message'],
            "intent_result": intent_result
        })
        
        # چاپ نتیجه برای بررسی
        print(f"Result from manager task: {result}")

        return result
