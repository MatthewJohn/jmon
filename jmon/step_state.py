
class StepState:

    def clone_to_child(self):
        """Clone current state to state for child step"""
        raise NotImplementedError

    def integrate_from_child(self, child):
        raise NotImplementedError

class SeleniumStepState(StepState):

    def __init__(self, selenium_instance, element):
        self.element = element
        self.selenium_instance = selenium_instance

    def clone_to_child(self):
        """Clone current state to state for child step"""
        return SeleniumStepState(
            selenium_instance=self.selenium_instance,
            element=self.element
        )

    def integrate_from_child(self, child):
        """Integrate child state back into current state"""
        pass


class RequestsStepState(StepState):

    def __init__(self, response):
        """Store state member variables"""
        self.response = response

    def clone_to_child(self):
        """Clone current state to state for child step"""
        return RequestsStepState(response=self.response)

    def integrate_from_child(self, child):
        """Integrate child state back into current state"""
        # Copy response back to parent object
        self.response = child.response
