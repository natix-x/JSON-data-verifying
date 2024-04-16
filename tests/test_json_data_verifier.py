import pytest
import json
from method.json_data_verifier import JsonDataVerifier


class TestJsonDataVerifier:
    @pytest.fixture
    def json_file_with_asteriks_existing_path(self, tmp_path):
        data = {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": ["iam:ListRoles", "iam:ListUsers"],
                        "Resource": "*",
                    }
                ],
            },
        }
        file_path = tmp_path.joinpath("existing.json")
        with open(file_path, "w") as file:
            json.dump(data, file)
        return file_path

    @pytest.fixture
    def verifier_existing_file_with_asteriks(
        self, json_file_with_asteriks_existing_path
    ):
        return JsonDataVerifier(json_file_with_asteriks_existing_path)

    @pytest.fixture
    def json_file_with_other_resource_existing_path(self, tmp_path):
        data = {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": ["iam:ListRoles", "iam:ListUsers"],
                        "Resource": "arn:aws:iam::account-ID-without-hyphens:user/Bob",
                    }
                ],
            },
        }
        file_path = tmp_path.joinpath("existing.json")
        with open(file_path, "w") as file:
            json.dump(data, file)
        return file_path

    @pytest.fixture
    def verifier_existing_file_with_other_resource(
        self, json_file_with_other_resource_existing_path
    ):
        return JsonDataVerifier(json_file_with_other_resource_existing_path)

    @pytest.fixture
    def json_file_invalid_path(self, tmp_path):
        file_path = tmp_path.joinpath("not_existing.json")
        return file_path

    @pytest.fixture
    def verifier_non_existing_file(self, json_file_invalid_path):
        return JsonDataVerifier(json_file_invalid_path)

    def test_load_json_file_valid_path(self, verifier_existing_file_with_asteriks):
        verifier_existing_file_with_asteriks.load_json_file()
        assert verifier_existing_file_with_asteriks.parsed_json_file is not None

    def test_load_json_file_invalid_path(self, verifier_non_existing_file):
        error_message = verifier_non_existing_file.load_json_file()
        assert error_message == "Error occurred: No such file"

    def test_load_json_file_empty_file(self, tmp_path):
        data = {}
        file_path = tmp_path.joinpath("existing.json")
        with open(file_path, "w") as file:
            json.dump(data, file)
        verifier = JsonDataVerifier(file_path)
        error_message = verifier.load_json_file()
        assert error_message == "Error occurred: Empty JSON input"

    def test_verify_policy_name_valid(self, verifier_existing_file_with_asteriks):
        verifier_existing_file_with_asteriks.verify_policy_name()
        assert verifier_existing_file_with_asteriks.policy_name is not None

    def test_verify_policy_name_no_policy_name(
        self, verifier_existing_file_with_asteriks
    ):
        verifier_existing_file_with_asteriks.parsed_json_file.pop(
            "PolicyName"
        )  # No policy name field

        error_message = verifier_existing_file_with_asteriks.verify_policy_name()
        assert (
            error_message
            == "Error occurred: PolicyName field is not defined in JSON file"
        )

    def test_verify_policy_name_wrong_type(self, verifier_existing_file_with_asteriks):
        verifier_existing_file_with_asteriks.parsed_json_file.update(
            {"PolicyName": 123}
        )  # Wrong type of data, string expected
        error_message = verifier_existing_file_with_asteriks.verify_policy_name()
        assert error_message == "Error occurred: PolicyName must be a string"

    def test_verify_policy_name_wrong_pattern(
        self, verifier_existing_file_with_asteriks
    ):
        verifier_existing_file_with_asteriks.parsed_json_file.update(
            {"PolicyName": "#123"}
        )  # Invalid pattern (no word at the beginning)
        error_message = verifier_existing_file_with_asteriks.verify_policy_name()
        assert (
            error_message
            == "Error occurred: PolicyName does not match expected pattern"
        )

    def test_verify_policy_name_too_long(self, verifier_existing_file_with_asteriks):
        verifier_existing_file_with_asteriks.parsed_json_file.update(
            {
                "PolicyName": "rootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootroot"
            }
        )  # too long string

        error_message = verifier_existing_file_with_asteriks.verify_policy_name()
        assert (
            error_message
            == "Error occurred: PolicyName should have between 1 and 128 characters"
        )

    def test_verify_policy_document_valid(self, verifier_existing_file_with_asteriks):
        verifier_existing_file_with_asteriks.verify_policy_document()
        assert verifier_existing_file_with_asteriks.policy_document is not None

    def test_verify_policy_document_no_policy_document(
        self, verifier_existing_file_with_asteriks
    ):
        verifier_existing_file_with_asteriks.parsed_json_file.pop(
            "PolicyDocument"
        )  # no PolicyDocument field

        error_message = verifier_existing_file_with_asteriks.verify_policy_document()
        assert (
            error_message
            == "Error occurred: PolicyDocument field is not defined in JSON file"
        )

    def test_verify_policy_document_wrong_type(
        self, verifier_existing_file_with_asteriks
    ):
        verifier_existing_file_with_asteriks.parsed_json_file.update(
            {"PolicyDocument": "123"}
        )  # wrong type, JSON expected
        error_message = verifier_existing_file_with_asteriks.verify_policy_document()
        assert error_message == "Error occurred: PolicyDocument must be a JSON object"

    def test_verify_statement_and_resource_valid_with_asterisk(
        self, verifier_existing_file_with_asteriks
    ):
        verifier_existing_file_with_asteriks.verify_statement_and_resource()
        assert verifier_existing_file_with_asteriks.resource is not None

    def test_verify_statement_and_resource_valid_other(
        self, verifier_existing_file_with_other_resource
    ):
        verifier_existing_file_with_other_resource.verify_statement_and_resource()
        assert verifier_existing_file_with_other_resource.resource is not None

    def test_verify_statement_and_resource_no_statement_field(
        self, verifier_existing_file_with_asteriks
    ):
        verifier_existing_file_with_asteriks.parsed_json_file["PolicyDocument"].pop(
            "Statement"
        )  # no statement field

        error_message = (
            verifier_existing_file_with_asteriks.verify_statement_and_resource()
        )
        assert (
            error_message
            == "Error occurred: Statement field is not defined in one of the policy documents"
        )

    def test_verify_statement_and_resource_no_resource_field(
        self, verifier_existing_file_with_asteriks
    ):
        verifier_existing_file_with_asteriks.parsed_json_file["PolicyDocument"].update(
            {
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": ["iam:ListRoles", "iam:ListUsers"],
                        "Something": "*",
                    }
                ]
            }
        )
        error_message = (
            verifier_existing_file_with_asteriks.verify_statement_and_resource()
        )
        assert (
            error_message
            == "Error occurred: Resource field is not defined in one of the statements."
        )

    def test_error_handler(self, verifier_existing_file_with_asteriks):
        error = verifier_existing_file_with_asteriks.error_handler(
            "error_message_test"
        )  # test if method returns any error message correctly
        assert error == "Error occurred: error_message_test"

    def test_check_resource_asteriks(self, verifier_existing_file_with_asteriks):
        output = verifier_existing_file_with_asteriks.check_resource()
        assert output is False

    def test_check_resource_other(self, verifier_existing_file_with_other_resource):
        output = verifier_existing_file_with_other_resource.check_resource()
        assert output is True

    def test_verify_aws_iam_role_policy_valid_asteriks(
        self, verifier_existing_file_with_asteriks
    ):
        output = verifier_existing_file_with_asteriks.verify_aws_iam_role_policy()
        assert output is False

    def test_verify_aws_iam_role_policy_valid_other(
        self, verifier_existing_file_with_other_resource
    ):
        output = verifier_existing_file_with_other_resource.verify_aws_iam_role_policy()
        assert output is True

    def test_verify_aws_iam_role_policy_multiple_resources_other(self, tmp_path):
        data = {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": ["iam:ListRoles", "iam:ListUsers"],
                        "Resource": [
                            "arn:aws:dynamodb:us-east-2:account-ID-without-hyphens:table/books_table",
                            "arn:aws:dynamodb:us-east-2:account-ID-without-hyphens:table/magazines_table",
                        ],
                    }
                ],
            },
        }
        file_path = tmp_path.joinpath("existing.json")
        with open(file_path, "w") as file:
            json.dump(data, file)
        verifier = JsonDataVerifier(file_path)
        output = verifier.verify_aws_iam_role_policy()
        assert output is True

    def test_verify_aws_iam_role_policy_multiple_resources_asteriks(self, tmp_path):
        data = {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": ["iam:ListRoles", "iam:ListUsers"],
                        "Resource": [
                            "arn:aws:dynamodb:us-east-2:account-ID-without-hyphens:table/books_table",
                            "*",
                        ],
                    }
                ],
            },
        }
        file_path = tmp_path.joinpath("existing.json")
        with open(file_path, "w") as file:
            json.dump(data, file)
        verifier = JsonDataVerifier(file_path)
        output = verifier.verify_aws_iam_role_policy()
        assert output is False

    def test_verify_aws_iam_role_policy_error_occurrence(self, tmp_path):
        data = {  # no PolicyName
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": ["iam:ListRoles", "iam:ListUsers"],
                        "Resource": "*",
                    }
                ],
            },
        }
        file_path = tmp_path.joinpath("existing.json")
        with open(file_path, "w") as file:
            json.dump(data, file)
        verifier = JsonDataVerifier(file_path)
        output = verifier.verify_aws_iam_role_policy()
        assert output == "Error occurred: PolicyName field is not defined in JSON file"
