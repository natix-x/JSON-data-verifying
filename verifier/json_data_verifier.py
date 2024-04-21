import json
import re


class JsonDataVerifier:
    """
    verifies the input JSON data.
    Input data format is defined as AWS::IAM::Role Policy.
    """

    def __init__(self, json_file):
        self.json_file = json_file
        self.parsed_json_file = None
        self.policy_name = None
        self.policy_document = None
        self.resource = None
        self.verify_aws_iam_role_policy()

    @staticmethod
    def error_handler(error):
        """
        prints error message and  exits a programme
        :param error: occurred error
        :return: error message
        """
        return f"Error occurred: {error}"

    def verify_aws_iam_role_policy(self):
        """
        verifies the input JSON data according to AWS::IAM::Role Policy, returns error message if any error occurred,
        if no: execute checks_resource method and returns False if resource field contains a single asterisk or True in any other case
        :return: True, False or error message
        """

        return (
            self.load_json_file()
            or self.verify_policy_name()
            or self.verify_policy_document()
            or self.verify_statement_and_resource()
            or self.check_resource()
        )

    def check_resource(self):
        """
        returns False if resource field contains a single asterisk or True in any other case
        :return: True or False
        """
        if (self.resource == "*") or ("*" in self.resource):
            return False
        else:
            return True

    def load_json_file(self):
        """
        loads JSON file, check if file exists and is valid and not empty
        :return: error message if occurred or None
        """
        try:
            with open(self.json_file, "r") as inserted_json_file:
                self.parsed_json_file = json.load(inserted_json_file)  # load JSON file
            if len(self.parsed_json_file) == 0:
                return self.error_handler("Empty JSON input")  # JSON input is empty
        except FileNotFoundError as e:  # handle situation if file not found
            return self.error_handler("No such file")
        except json.decoder.JSONDecodeError:
            return self.error_handler("JSON data is invalid")

    def verify_policy_name(self):
        """
        verifies Policy Name field in parsed json file,
        checks if that field exists, has expected pattern, length (between 1 and 128 characters) and type(str)
        :return: error message or None
        """
        self.policy_name = self.parsed_json_file.get("PolicyName")
        if self.policy_name is None:
            return self.error_handler("PolicyName field is not defined in JSON file")
        if not isinstance(self.policy_name, str):
            return self.error_handler("PolicyName must be a string")
        if not re.match(r"[\w+=,.@-]+", self.policy_name):
            return self.error_handler("PolicyName does not match expected pattern")
        if len(self.policy_name) >= 128:
            return self.error_handler(
                "PolicyName should have between 1 and 128 characters"
            )

    def verify_policy_document(self):
        """
        verifies Policy Document field in parsed json file,
        checks if that field exists and has appropriate type(Json)
        :return: error_message or None
        """
        self.policy_document = self.parsed_json_file.get("PolicyDocument")
        if self.policy_document is None:
            return self.error_handler(
                "PolicyDocument field is not defined in JSON file"
            )
        if not isinstance(self.policy_document, dict):
            return self.error_handler("PolicyDocument must be a JSON object")

    def verify_statement_and_resource(self):
        """
        verifies 'Statement' and 'Resource' field, checks if they exist and
        if 'Statement' field has proper format
        :return: error message or None
        """
        statements = self.policy_document.get("Statement")
        if statements is None:
            return self.error_handler(
                "Statement field is not defined in one of the policy documents"
            )

        if isinstance(statements, dict):
            statements = [statements]   # If individual statement put it in the list
        elif not isinstance(statements, list):
            return self.error_handler(
                    "Each individual statement block must be enclosed in curly braces { }. "
                    "For multiple statements, the array must be enclosed in square brackets [ ]"
            )
        for statement in statements:
            self.resource = statement.get("Resource")
            if self.resource is None:
                return self.error_handler(
                    "Resource field is not defined in one of the statements."
                )
