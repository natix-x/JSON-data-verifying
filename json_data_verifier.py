import json
import re
import sys


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
        self.verify_aws_iam_role_policy()

    @staticmethod
    def error_handler(error):
        """
        prints error message and  exits a programme
        :param error: occurred error
        :return: error message
        """
        print(f"Error occurred: {error}")
        sys.exit(1)

    def verify_aws_iam_role_policy(self):
        """
        verifies the input JSON data according to AWS::IAM::Role Policy, prints error message if any error occurred,
        returns False if resource field contains a single asterisk or True in any other case
        :return: True, False or error message
        """
        try:
            self.load_json_file()
            self.verify_policy_name()
            self.verify_policy_document()
            resource = self.verify_statement_and_resource()
            if resource == "*":
                return False
            else:
                return True
        except (TypeError, ValueError, AttributeError) as e:
            self.error_handler(e)

    def load_json_file(self):
        """
        loads JSON file, check if file exists or if it is empty, if so raises suitable error
        :return: updated parsed_json_file attribute or ValueError
        """
        try:
            with open(self.json_file, "r") as inserted_json_file:
                self.parsed_json_file = json.load(inserted_json_file)  # load JSON file
        except FileNotFoundError as e:  # handle situation if file not found
            self.error_handler("No such file")
        if len(self.parsed_json_file) == 0:
            raise ValueError("Empty JSON input")  # JSON input is empty

    def verify_policy_name(self):
        """
        verifies Policy Name field in parsed json file,
        checks if that field exists, has expected pattern and length (between 1 and 128 characters) and type(str)
        and then raises suitable error
        :return: updated policy name attribute or Attribute/Type/Value error
        """
        self.policy_name = self.parsed_json_file.get("PolicyName")
        if self.policy_name is None:
            raise AttributeError("PolicyName field is not defined in JSON file")
        if not isinstance(self.policy_name, str):
            raise TypeError("PolicyName must be a string")
        if not re.match(r"[\w+=,.@-]+", self.policy_name):
            raise ValueError("PolicyName does not match expected pattern")
        if len(self.policy_name) >= 128:
            raise ValueError("PolicyName should have between 1 and 128 characters")

    def verify_policy_document(self):
        """
        verifies Policy Document field in parsed json file,
        checks if that field exists and has appropriate type(Json)
        and then raises suitable error
        :return: updated policy document attribute or Attribute/Type error
        """
        self.policy_document = self.parsed_json_file.get("PolicyDocument")
        if self.policy_document is None:
            raise AttributeError("PolicyDocument field is not defined in JSON file")
        if not isinstance(self.policy_document, dict):
            raise TypeError("PolicyDocument must be a JSON object")

    def verify_statement_and_resource(self):
        """
        verifies 'Statement' and 'Resource' field, checks if they exist
        :return: Content of resource field or Attribute Error
        """
        statements = self.policy_document.get("Statement")
        if statements is None:
            raise AttributeError(
                "Statement field is not defined in one of the policy documents"
            )
        for statement in statements:
            resource = statement.get("Resource")
            if resource is None:
                raise AttributeError(
                    "Resource field is not defined in one of the statements."
                )
            return resource
