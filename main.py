import json
import re


def verify_aws_iam_role_policy(json_file):
    """
    verifies the input JSON data.
    Input data format is defined as AWS::IAM::Role Policy.
    :param json_file: path to json file
    :return: False if an input JSON Resource field contains a single asterisk, True in any other case and
    prints message if any error occurred
    """
    try:
        with open(json_file, "r") as inserted_json_file:
            parsed_json = json.load(inserted_json_file)  # load JSON file
            if len(parsed_json) == 0:
                raise ValueError("Empty JSON input")
            policy_name = parsed_json.get("PolicyName")
            if policy_name is None:
                raise AttributeError("PolicyName field is not defined in JSON file")
            if not isinstance(policy_name, str):
                raise TypeError("PolicyName must be a string")
            if not re.match(r"[\w+=,.@-]+", policy_name):
                raise ValueError("PolicyName does not match expected pattern")
            if len(policy_name) >= 128:
                raise ValueError("PolicyName should have between 1 and 128 characters")
            policy_document = parsed_json.get("PolicyDocument")
            if policy_document is None:
                raise AttributeError("PolicyDocument field is not defined in JSON file")
            if not isinstance(policy_document, dict):
                raise TypeError("PolicyDocument must be a JSON object")
            statements = policy_document.get("Statement")
            if statements is None:
                raise AttributeError(
                    "Statement field is not defined in one of the policy documents"
                )
            for statement in statements:
                resource = statement.get("Resource")
                if resource == "*":
                    return False
                if resource is None:
                    raise AttributeError(
                        "Resource field is not defined in one of the statements."
                    )  # no 'Resource' field founded in 'Statement'
    except FileNotFoundError:
        print("File not found.")  # provided file's path is wrong
    except json.JSONDecodeError as e:
        print(
            f"JSON decoding error occurred: {e.msg}: line {e.lineno}, position {e.pos}"
        )  # JSON data is invalid
    except ValueError as e:
        print(f"ValueError occurred: {e}")  # raised ValueError occurred
    except TypeError as e:
        print(f"TypeError occurred: {e}")  # raised TypeError occurred
    except AttributeError as e:
        print(f"AttributeError occurred: {e}")  # raised AttributeError occurred
    else:
        return True


if __name__ == "__main__":
    output = verify_aws_iam_role_policy("./example.txt")
    if isinstance(output, bool):  # check if returned value is True or False
        print(output)  # prints outcome
