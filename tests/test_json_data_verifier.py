import pytest
import json
from method.json_data_verifier import JsonDataVerifier


class TestJsonDataVerifier:

    @pytest.fixture
    def verifier_existing_file(self, json_file_valid_path):
        return JsonDataVerifier(json_file_valid_path)

    @pytest.fixture
    def verifier_non_existing_file(self, json_file_invalid_path):
        return JsonDataVerifier(json_file_invalid_path)

    @pytest.fixture
    def json_file_valid_path(self, tmp_path):
        data = {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": [
                            "iam:ListRoles",
                            "iam:ListUsers"
                        ],
                        "Resource": "*"
                    }
                ]
            }
        }
        file_path = tmp_path.joinpath("existing.json")
        with open(file_path, "w") as file:
            json.dump(data,file)
        return file_path

    @pytest.fixture
    def json_file_invalid_path(self, tmp_path):
        file_path = tmp_path.joinpath("not_existing.json")

        return file_path

    def test_load_json_file_valid_path(self, verifier_existing_file):
        verifier_existing_file.load_json_file()
        assert verifier_existing_file.parsed_json_file is not None

    def test_load_json_file_invalid_path(self, verifier_non_existing_file):
        error_message = verifier_non_existing_file.load_json_file()
        assert error_message == "Error occurred: No such file"

    @pytest.fixture
    def json_file_empty(self, tmp_path):
        data = {}
        file_path = tmp_path.joinpath("existing.json")
        with open(file_path, "w") as file:
            json.dump(data,file)
        return file_path

    def test_load_json_file_empty_file(self, json_file_empty):
        verifier = JsonDataVerifier(json_file_empty)
        with pytest.raises(ValueError):
            verifier.load_json_file()

    def test_verify_policy_name_valid(self, verifier_existing_file):
        verifier_existing_file.verify_policy_name()
        assert verifier_existing_file.policy_name is not None

    def test_verify_policy_name_existence(self, verifier_existing_file):
        verifier_existing_file.parsed_json_file.pop("PolicyName")  # Remove policy name field
        with pytest.raises(AttributeError):
            verifier_existing_file.verify_policy_name()

    def test_verify_policy_name_type(self, verifier_existing_file):
        verifier_existing_file.parsed_json_file["PolicyName"] = 123  # Invalid policy name
        with pytest.raises(TypeError):
            verifier_existing_file.verify_policy_name()

    def test_verify_policy_name_pattern(self, verifier_existing_file):
        verifier_existing_file.parsed_json_file["PolicyName"] = "#123"  # Invalid pattern (no word at the beginning)
        with pytest.raises(ValueError):
            verifier_existing_file.verify_policy_name()

    def test_verify_policy_name_length(self, verifier_existing_file):
        verifier_existing_file.parsed_json_file["PolicyName"] = "rootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootrootroot"  # too long str
        with pytest.raises(ValueError):
            verifier_existing_file.verify_policy_name()

    def test_verify_policy_document_valid(self, verifier_existing_file):
        verifier_existing_file.verify_policy_document()
        assert verifier_existing_file.policy_document is not None

    def test_verify_policy_document_type(self, verifier_existing_file):
        verifier_existing_file.parsed_json_file["PolicyDocument"] = "123"
        with pytest.raises(TypeError):
            verifier_existing_file.verify_policy_document()














