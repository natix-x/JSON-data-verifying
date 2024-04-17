# JSON-data-verifying

## Table of contents: 
* [General info](#general-info)
* [Project structure](#project-structure)
* [Requirements](#requirements)
* [Setup](#setup)

### General info
The aim of this task is to write a method verifying the input JSON data.
Input data format is defined as AWS::IAM::Role Policy - definition and example [(AWS IAM Role JSON definition and example)](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-role-policy.html).
Method returns logical false if an input JSON Resource field contains a single asterisk and true in any other case. 
### Requirements and used libraries
python 3.11+, json, pytest
### Project structure
├── JSON_data
│   ├── example.txt
│   ├── example.py
│   ├── another_example.py
│   └── ...
│
├── tests
│   ├── test_json_data_verifier.py
│   └── __init__.py
│
├── verifier
│   ├── json_data_verifier.py
│   ├── main.py
│   └── __init__.py
│
├── .gitignore
├── README.md
├── run.bat
└── run_tests.bat

### Setup
1. First, clone this repository:
   ```sh
   git clone https://github.com/natix-x/JSON-data-verifying.git
   ```
2. For running programme: run.bat:
   ```sh
   run.bat
   ```
If you want to check another file, add it to JSON_data directory and run upper command again. 
3. For running tests: run_test.bat:
   ```sh
   run_tests.bat
   ```