
import inspect
from typing import get_type_hints

class Action:

    def __init__(self, function, parameters) -> None:
        self.function = function

        # Check if the provided parameters match the function signature
        if self.has_matching_parameters(parameters):
            self.parameters = parameters
        else:
            raise ValueError("The provided parameters do not match the function's signature")
    
    def has_matching_parameters(self, parameters) -> bool:
        # Get the function's signature and type hints
        function_signature = inspect.signature(self.function)
        type_hints = get_type_hints(self.function)
        
        # Get the function's expected parameter names
        expected_params = list(function_signature.parameters.keys())

        # Check if the number of provided parameters matches the number of expected parameters
        if len(expected_params) != len(parameters):
            return False

        # Check if the types of the provided parameters match the expected types
        for i, param_name in enumerate(expected_params):
            expected_type = type_hints.get(param_name, None)  # None if no type hint is provided
            provided_value = parameters[i]

            if expected_type and not isinstance(provided_value, expected_type):
                print(f"Type mismatch for parameter '{param_name}': expected {expected_type}, got {type(provided_value)}")
                return False

        return True
    
    def execute(self):
        # Execute the function with the provided parameters
        return self.function(*self.parameters)
