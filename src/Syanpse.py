#!/usr/bin/env python3
# -------------------------------------------------------------------------------
# Created by Ulysses Carlos on 02/14/2023 at 07:36 PM
#
# Syanpse.py
#
# -------------------------------------------------------------------------------
from pathlib import Path
import requests
import logging

ACCESS_TOKEN = ""
SYNAPSE_USER = "matrix"
SYNAPSE_EXECUTABLE = Path.root / SYNAPSE_USER / ".local" / "bin" / "synctl"
SYNAPSE_MAIN_DIRECTORY = Path.root / SYNAPSE_USER / "Synapse"
BASE_URL = "http://localhost:8080"


def generate_registration_token():
    """Generate Registration Token."""
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

    logging.debug("Attempting to create a HTTP POST request with the following information:")
    logging.debug(f"\tURL Link: {url_path}\nData Options: {data_options}\nParameters: {parameters}")
    try:
        request = requests.post(url_path, data=data_options, params=parameters)
        request.raise_for_status()
    except request.HTTPError:
        logging.error("Error: HTTP POST request failed!")
        print("Error: The HTTP POST request failed!")
        exit(1)

    # If everything's good, then turn the json into a dict:
    response = dict(request.json())

    if not response['registration_tokens']:
        raise KeyError("Error: Could not find the 'registration_tokens' key in the response dictionary.")
    else:
        token_response = response['registration_tokens']
        token = token_response['token'] if token_response['token'] else ""
        # expiry_time  = token_response['expiry_time'] if token_response['expiry_time'] else ""

        print(f"Your registration Token is {token}")
        print(f"It is valid until {expiration_date}")


def delete_registration_token(token=""):
    """Generate Registration Token."""
    pass


def get_all_registration_tokens():
    """Generate Registration Token."""
    pass


def delete_all_registration_tokens():
    """Generate Registration Token."""
    pass


def start_synapse():
    """Generate Registration Token."""
    pass


def stop_synapse():
    """Generate Registration Token."""
    pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
