@echo off
pip install pytest
cd tests
pytest test_json_data_verifier.py
cd ..