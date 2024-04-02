import json


def verify_aws_iam_role_policy(json_file):
    """
    verifies the input JSON data.

    Input data format is defined as AWS::IAM::Role Policy - definition and example
    :param json_file: path to json file
    :return: False if an input JSON Resource field contains a single asterisk, True in any other case
    """
    try:
        with open(json_file, "r") as inserted_json_file:
            parsed_json = json.load(inserted_json_file)  # load JSON file
            statements = parsed_json.get("PolicyDocument").get("Statement")
            for statement in statements:
                resource = statement.get("Resource")  # get 'Resource' value
                if resource == "*":
                    return False
            else:
                return True
    except FileNotFoundError:
        print("File not found.")  # provided file's path is wrong
    except json.JSONDecodeError as e:
        print(f"JSON decoding error occurred: {e.msg}: line {e.lineno}, position {e.pos}")  # JSON data is invalid


if __name__ == "__main__":
    print(verify_aws_iam_role_policy('./example.txt'))

