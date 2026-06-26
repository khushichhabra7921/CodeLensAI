import os
import subprocess
import pickle
import yaml


API_KEY = "sk-test-hardcoded-api-key"
password = "admin123"
TOKEN = "secret-token-value"
URL = "http://example.com/api"


def run_eval(user_input):
    return eval(user_input)


def run_exec(code):
    exec(code)


def run_system_command(command):
    os.system(command)


def run_subprocess(command):
    subprocess.run(command, shell=True)


def load_pickle_data(file_path):
    with open(file_path, "rb") as file:
        return pickle.load(file)


def load_yaml_data(yaml_text):
    return yaml.load(yaml_text)


def safe_function(a, b):
    return a + b