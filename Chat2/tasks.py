class Task:
    def __init__(self, name, description, agent, expected_output):
        self.name = name
        self.description = description
        self.agent = agent
        self.expected_output = expected_output

    def execute(self, *args, **kwargs):
        raise NotImplementedError

class OptimizerTask(Task):
    def __init__(self, optimizer_agent):
        super().__init__(
            name="Optimize Input",
            description="Optimize user input for clarity and completeness.",
            agent=optimizer_agent,
            expected_output="An optimized version of the user input."
        )

    def execute(self, user_input):
        return self.agent.respond(user_input)

class IntentDetectionTask(Task):
    def __init__(self, intent_detection_agent):
        super().__init__(
            name="Detect Intent",
            description="Detect the intent behind the optimized user input.",
            agent=intent_detection_agent,
            expected_output="The detected intent behind the user input."
        )

    def execute(self, optimized_input):
        return self.agent.respond(optimized_input)

class ManagerTask(Task):
    def __init__(self, manager_agent):
        super().__init__(
            name="Manage Project",
            description="Generate a comprehensive response based on user input, detected intent, and project data.",
            agent=manager_agent,
            expected_output="A comprehensive response generated based on the inputs."
        )

    def execute(self, optimized_input, detected_intent):
        return self.agent.respond(optimized_input, detected_intent)

class EditorTask(Task):
    def __init__(self, editor_agent):
        super().__init__(
            name="Edit Response",
            description="Edit and improve responses based on feedback.",
            agent=editor_agent,
            expected_output="An edited and improved version of the response."
        )

    def execute(self, manager_response, feedback):
        return self.agent.respond(manager_response, feedback)