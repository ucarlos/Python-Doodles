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
import argparse

ACCESS_TOKEN = ""
SYNAPSE_USER = "matrix"

ROOT = Path(Path.cwd().root)
SYNAPSE_EXECUTABLE = ROOT / SYNAPSE_USER / ".local" / "bin" / "synctl"
SYNAPSE_MAIN_DIRECTORY = ROOT / SYNAPSE_USER / "Synapse"
BASE_URL = "http://localhost:8080"

DEBUG_MODE = False


def execute_http_request(http_method_callback, url_path, data_parameters, url_parameters):
    """Execute a HTTP Request using the requests library.

    :param http_mthod_callback:
    :param url_path
    :param data_parameters
    :param url_parameters
    :return: a Dictionary containing fields returned by the response.
    """
    logging.debug("execute_http_request: Attempting to create a HTTP request with the following information:")
    logging.debug(f"\nURL Link: {url_path}\nData Options: {data_parameters}\nURL Parameters: {url_parameters}")
    try:
        request = http_method_callback(url_path, data=data_parameters, url_aram=url_parameters)
        request.raise_for_status()
    except request.HTTPError:
        logging.error("Error: HTTP POST request failed!")
        print("Error: The HTTP POST request failed!")
        exit(1)

    return dict(request.json())


def generate_registration_token():
    """Generate a registration Token."""
    valid_token_time = "10min"

    data_options = {
        "access_token": ACCESS_TOKEN,
        "uses_allowed": 1,
        "expiry_time": valid_token_time,
        "length": 48
    }

    parameters = {"access_token": ACCESS_TOKEN}

    expiration_date = ""
    url_path = f"{BASE_URL}/_synapse/admin/v1/registration_tokens/new"
    response = execute_http_request(requests.post, url_path, data_options, parameters)

    # logging.debug("Attempting to create a HTTP POST request with the following information:")
    # logging.debug(f"\nURL Link: {url_path}\nData Options: {data_options}\nParameters: {parameters}")
    # try:
    #     request = requests.post(url_path, data=data_options, params=parameters)
    #     request.raise_for_status()
    # except request.HTTPError:
    #     logging.error("Error: HTTP POST request failed!")
    #     print("Error: The HTTP POST request failed!")

    if not response['registration_tokens']:
        raise KeyError("Error: Could not find the 'registration_tokens' key in the response dictionary.")
    else:
        token_response = response['registration_tokens']
        token = token_response['token'] if token_response['token'] else ""
        # expiry_time  = token_response['expiry_time'] if token_response['expiry_time'] else ""

        print(f"Your registration Token is {token}")
        print(f"It is valid until {expiration_date}")


def delete_registration_token(token=""):
    """Delete a specific registration Token."""
    pass


def get_all_registration_tokens():
    """Retrieve all registration tokens."""
    pass


def delete_all_registration_tokens():
    """Delete all registration tokens."""
    pass


def start_synapse():
    """Start up the Synapse server."""
    pass


def stop_synapse():
    """Shutdown the Synapse server."""
    pass


def argparse_condition(key, value):
    """Predicate used by the sum function to determine if the argparse list is valid."""
    return False if key == "admin_token" or not value else True


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
    if DEBUG_MODE:
        ACCESS_TOKEN = "syt_dWx5c3Nlcw_FPpGhLTtdxmkMTJpBZuG_0rPk1N"
        generate_registration_token()

    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()

    parser.add_argument("--start", help="Start up the Synapse server.", action="store_true")
    parser.add_argument("--stop", help="Shutdown the Synapse server.", action="store_true")
    parser.add_argument("--create-token", help="Create a Registration token.", action="store_true")
    parser.add_argument("--delete-token", help="Delete a given Registration token.", type=str, required=False)
    parser.add_argument("--delete-all-tokens", help="Delete all existing Registration tokens.", action="store_true")

    parser.add_argument("admin_token",
                        help="The Admin token to use in order to authenticate the HTTP request.",
                        type=str)

    args = parser.parse_args()

    # admin_token = args.admin_token
    # print(f"Admin Token: {admin_token}")
    # print(f"Args array: {args}")
    # Only check for ONE item at a time:

    valid_argparse = is_argparse_list_valid(args)
    if not valid_argparse:
        print("Error: Only one option can be passed as a argument.")
        exit(1)

    # print(f"Is argparse list valid? {is_argparse_list_valid(args)}")
