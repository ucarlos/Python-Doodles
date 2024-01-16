#!/usr/bin/env python3
# -------------------------------------------------------------------------------
# Created by Ulysses Carlos on 02/14/2023 at 07:36 PM
#
# Syanpse.py
# A Python wrapper around some common synapse behavior that I want to wrap around
# -------------------------------------------------------------------------------
from pathlib import Path
import requests
import logging
import json
import argparse
from time import time
from datetime import datetime
from subprocess import run
from shlex import split

ACCESS_TOKEN = ""
SYNAPSE_USER = "matrix"

ROOT = Path(Path.cwd().root)
SYNAPSE_EXECUTABLE = ROOT / "home" / SYNAPSE_USER / ".local" / "bin" / "synctl"
SYNAPSE_MAIN_DIRECTORY = ROOT / "home" / SYNAPSE_USER / "Synapse"
SYNAPSE_MAIN_YAML_PATH = SYNAPSE_MAIN_DIRECTORY / "config" / "homeserver.yaml"
BASE_URL = "http://localhost:8008"

DEBUG_MODE = False


def execute_http_request(http_method, url_path, data_parameters={}, url_parameters={}):
    """Execute an HTTP Request using the requests library.

    :param http_method
    :param url_path
    :param data_parameters
    :param url_parameters
    :return: a Dictionary containing fields returned by the response.
    """
    logging.debug("execute_http_request: Attempting to create a HTTP request with the following information:")
    logging.debug(f"\nURL Link: {url_path}\nData Options: {data_parameters}\nURL Parameters: {url_parameters}")

    # Make sure to turn the data_parameters into JSON:
    json_data = json.dumps(data_parameters)

    try:
        request = requests.request(http_method, url_path, data=json_data, params=url_parameters)
        request.raise_for_status()
    except requests.HTTPError:
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.error(f"Error: HTTP {http_method} request failed!")
            logging.error(f"Here's the JSON Response: {request.json()}")
        else:
            print(f"Error: The HTTP {http_method} Request failed!")
        exit(1)

    return dict(request.json())


def generate_registration_token():
    """Generate a registration Token."""
    # Set the registration token to expire within 10 minutes:
    valid_token_time_in_min = 10
    unix_expiry_time = int(time()) + valid_token_time_in_min * 60

    data_options = {
        "access_token": ACCESS_TOKEN,
        "uses_allowed": 1,
        "expiry_time": unix_expiry_time * 1000,
        "length": 48
    }

    parameters = {"access_token": ACCESS_TOKEN}

    expiration_date = datetime.fromtimestamp(unix_expiry_time).strftime("%A, %B %d %Y %H:%M:%S")
    url_path = f"{BASE_URL}/_synapse/admin/v1/registration_tokens/new"

    response = execute_http_request("post", url_path, data_options, parameters)

    if not response['token']:
        raise KeyError("Error: Could not find the 'token' key in the response dictionary.")
    else:
        token = response['token'] if response['token'] else ""
        print(f"Your registration Token is {token}")
        print(f"It is valid until {expiration_date}")


def delete_registration_token(token):
    """Delete a specific registration Token."""
    data_options = {
        "access_token": ACCESS_TOKEN
    }

    parameters = {
        "access_token": ACCESS_TOKEN
    }

    url_path = f"{BASE_URL}/_synapse/admin/v1/registration_tokens/{token}"

    response = execute_http_request("delete", url_path, data_options, parameters)

    if not response:
        print(f"Token {token} has been deleted successfully.")
    else:
        print(f"An Error has occurred while deleting token {token}:")
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug(f"JSON response: {str(response)}")


def get_all_registration_tokens():
    """Retrieve all registration tokens."""
    data_options = {
        "access_token": ACCESS_TOKEN
    }

    parameters = {
        "access_token": ACCESS_TOKEN
    }

    url_path = f"{BASE_URL}/_synapse/admin/v1/registration_tokens"

    response = execute_http_request("get", url_path, data_options, parameters)

    logging.debug(f"Response: {str(response)}")

    return response['registration_tokens']


def print_all_registration_tokens():
    """Print each existing registration token."""
    token_list = get_all_registration_tokens()

    if not token_list:
        print("Error: No Registration_tokens were found.")
    else:
        print(f"{len(token_list)} token(s) found:")
        for token in token_list:
            print("-" * 80)
            print(f"Token Name  : {token['token']}")
            print(f"Uses Allowed: {token['uses_allowed']}")
            pending_status = "No" if not token['pending'] else "Yes"
            completed_status = "No" if not token['completed'] else "Yes"

            expiration_date = "n/a"
            if token['expiry_time'] > 0:
                expiration_date = datetime.fromtimestamp(token['expiry_time'] / 1000).strftime("%A, %B %d %Y %H:%M:%S")

            print(f"Pending?    : {pending_status}")
            print(f"Completed?  : {completed_status}")
            print(f"Expires on  : {expiration_date}")
            print("-" * 80 + "\n")


def delete_all_registration_tokens():
    """Delete all registration tokens."""
    token_list = get_all_registration_tokens()

    if len(token_list):
        print("Deleting all registration tokens:")
        for token in token_list:
            delete_registration_token(token['token'])
        print("Complete!")
    else:
        print("Error: No Registration tokens found.")


def ban_user():
    """Ban and remove all data involving a user."""
    pass


def start_synapse():
    """Start up the Synapse server."""
    command = f"sudo -u {SYNAPSE_USER} {str(SYNAPSE_EXECUTABLE)} start {str(SYNAPSE_MAIN_YAML_PATH)}"
    run(split(command))


def stop_synapse():
    """Shutdown the Synapse server."""
    command = f"sudo -u {SYNAPSE_USER} {str(SYNAPSE_EXECUTABLE)} stop {str(SYNAPSE_MAIN_YAML_PATH)}"
    run(split(command))


def argparse_condition(key, value):
    """Predicate used by the sum function to determine if the argparse list is valid."""
    return False if key == "admin_token" or not value else True


def execute_argument(argument_list):
    """Hideous function to select what function to run. Please let me know if there's a better way to do this."""
    if (argument_list.start):
        start_synapse()
    elif (argument_list.stop):
        stop_synapse()
    elif (argument_list.create_token):
        generate_registration_token()
    elif (argument_list.delete_token):
        delete_registration_token(argument_list.delete_token)
    elif (argument_list.delete_all_tokens):
        delete_all_registration_tokens()
    elif (argument_list.list_all_tokens):
        print_all_registration_tokens()
    else:
        message = "select_function(): If you see this, you've fucked up somewhere. Please make sure that you've mapped each argument to a function in this if else chain."
        logging.error(message)


def is_argparse_list_valid(argparse_list):
    """Validate that the argparsed list contains only one argument.

    :param argparse_list
    :return True if there's only valid argument. False otherwise.
    """
    var_list = vars(argparse_list)

    true_sum = sum(argparse_condition(key, value) for key, value in var_list.items())

    # Return true_sum == 1 or (true_sum < 0 && delete-token is not null)
    return (true_sum == 1) or (true_sum < 1 and argparse_list.delete_token)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if DEBUG_MODE:
        ACCESS_TOKEN = "[insert admin token here]"
        exit(0)

    parser = argparse.ArgumentParser()

    parser.add_argument("--start", help="Start up the Synapse server.", action="store_true")
    parser.add_argument("--stop", help="Shutdown the Synapse server.", action="store_true")
    parser.add_argument("--create-token", help="Create a Registration token.", action="store_true")
    parser.add_argument("--delete-token", help="Delete a given Registration token.", type=str, required=False)
    parser.add_argument("--delete-all-tokens", help="Delete all existing Registration tokens.", action="store_true")
    parser.add_argument("--list-all-tokens", help="List all existing Registration tokens.", action="store_true")
    parser.add_argument("admin_token",
                        help="The Admin token to use in order to authenticate the HTTP request.",
                        type=str)

    args = parser.parse_args()
    logging.debug(f"Argument Array: {args}")

    valid_argparse = is_argparse_list_valid(args)
    if not valid_argparse:
        print("Error: Only one option can be passed as a argument.")
        exit(1)
    else:
        ACCESS_TOKEN = args.admin_token
        execute_argument(args)
