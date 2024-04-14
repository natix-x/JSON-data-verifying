# JSON-data-verifying

## Table of contents: 
* [General info](#general-info)
* [Requirements](#requirements)
* [Setup](#setup)

### General info
The aim of this task is to write a method verifying the input JSON data.
Input data format is defined as AWS::IAM::Role Policy - definition and example [(AWS IAM Role JSON definition and example)](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-role-policy.html).
Method returns logical false if an input JSON Resource field contains a single asterisk and true in any other case. 
### Requirements and used libraries
python 3.11+
### Setup
1. First, clone this repository:
   ```sh
   git clone https://github.com/natix-x/JSON-data-verifying.git
   ```
2. Run main.py
   ```sh
   python main.py
   ```