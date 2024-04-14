from json_data_verifier import JsonDataVerifier


if __name__ == "__main__":
    verify_json = JsonDataVerifier("./example.txt")
    print(verify_json.verify_aws_iam_role_policy())
