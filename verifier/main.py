import os
from json_data_verifier import JsonDataVerifier

directory = "../JSON_data"

if __name__ == "__main__":
    for filename in os.scandir(directory):
        if filename.is_file():
            verify_json = JsonDataVerifier(filename.path)
            verifier = verify_json.verify_aws_iam_role_policy()
            print(f"{filename.name}: {verifier}")
