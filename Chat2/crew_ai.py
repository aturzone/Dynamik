from optimizer_agent import OptimizerAgent
from intent_detection_agent import IntentDetectionAgent
from manager_agent import ManagerAgent
from editor_agent import EditorAgent
from tasks import OptimizerTask, IntentDetectionTask, ManagerTask, EditorTask

class CrewAI:
    def __init__(self):
        self.optimizer_agent = OptimizerAgent()
        self.optimizer_task = OptimizerTask(self.optimizer_agent)
        self.intent_detection_agent = IntentDetectionAgent()
        self.intent_detection_task = IntentDetectionTask(self.intent_detection_agent)
        self.manager_agent = ManagerAgent()
        self.manager_task = ManagerTask(self.manager_agent)
        self.editor_agent = EditorAgent()
        self.editor_task = EditorTask(self.editor_agent)

    def run(self):
        print("## Welcome to CrewAI\n____________________________")
        while True:
            user_input = input("You: ").strip()

            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            optimized_input = self.optimizer_task.execute(user_input)
            detected_intent = self.intent_detection_task.execute(optimized_input)
            manager_response = self.manager_task.execute(optimized_input, detected_intent)
            final_response = self.editor_task.execute(manager_response, "Please edit the response for clarity and completeness.")
            print(f"Optimized Input: {optimized_input}")
            print(f"Detected Intent: {detected_intent}")
            print(f"Manager Response: {manager_response}")
            print(f"Final Response: {final_response}")