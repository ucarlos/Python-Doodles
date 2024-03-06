#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Created by Ulysses Carlos on 02/13/2024 at 04:41 PM
#
# JSONParser.py
# Simple class to parse JSON.
# ------------------------------------------------------------------------------

import json
import argparse
import logging
from pathlib import Path
from sys import argv

EXIT_SUCCESS = 0; EXIT_FAILURE = 1


class TerminalColor(object):
    """Simple class to display color in print statements."""
    RED = "\033[91m"
    CLEAR_COLOR = "\033[0m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"


def print_error(message: str):
    """Simple function to print an error message with color."""
    print(f"{TerminalColor.RED}{TerminalColor.BOLD}{message}{TerminalColor.CLEAR_COLOR}")


def generate_json_object_from_string(raw_json: str):
    """Attempt to generate a JSON Object from a passed string parameter."""
    try:
        json_object = json.loads(raw_json)
    except json.JSONDecodeError:
        print_error("Error: Cannot parse JSON String since either a section (or all of it) is invalid.")
        exit(EXIT_FAILURE)

    # Next, you may have to go through
    return json_object


def generate_json_object_from_file(filepath_string: str):
    """Attempt to generate a JSON Object from a filepath."""
    filepath = Path(filepath_string)
    # First, verify if the damn file exists:
    if not filepath.exists():
        print_error(f"Error: The file {str(filepath)} does not exist.")
        exit(EXIT_FAILURE)

    if not filepath.is_file():
        print_error(f"Error: {str(filepath)} is NOT a file. Please try again.")
        exit(EXIT_FAILURE)

    # Now attempt to parse the json_object:

    with open(str(filepath), "r") as input_json_file:
        try:
            json_object = json.load(input_json_file)
        except json.JSONDecodeError:
            print_error(f"Error: Cannot parse JSON from {str(filepath)} since either a section (or all of it) "
                        "is invalid.")
            exit(EXIT_FAILURE)

    # Now return the json_object:
    return json_object


def map_walk(json_object: dict, format_string: str, format_counter: int):
    """Walk through the dict."""
    map_string = ""
    for key, value in json_object.items():
        # If the value is a part of a dict, do a recursive call:
        if not key:
            continue
        if isinstance(value, dict):
            map_string += (f"{format_string * format_counter}{key}:\n")
            map_string += map_walk(value, format_string, format_counter + 1)
        else:
            map_string += f"{format_string* format_counter}{key}: {value}\n"

    return map_string


def print_json_object(json_object: dict):
    """Print the JSON object."""
    print(map_walk(json_object, "\t", 0))


def pretty_print_json(json_object: dict):
    """Pretty Print the JSON object."""
    print(json.dumps(json_object, indent=4, sort_keys=True))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--json", help="The JSON string that will be parsed by the program", default=None,
                        type=str,
                        required=False)

    parser.add_argument("--file_path", help="The filepath to the .json file that will be parsed.",
                        default=None,
                        type=str,
                        required=False)

    arguments = parser.parse_args()

    if len(argv) == 1:
        parser.print_help()
        exit(EXIT_SUCCESS)

    logging.debug(f"main(): Passed Arguments: {arguments}")
    # Prevent both options from being used:
    if arguments.json and arguments.file_path:
        logging.debug("main(): Aborting program since both options cannot be selected.")
        print_error("Error: both --json and --file_path options cannot be used together. Either use --json OR "
                    "--file_path.")
        exit(EXIT_FAILURE)

    if arguments.json:
        json_object = generate_json_object_from_string(arguments.json)
        pretty_print_json(json_object)
    elif arguments.file_path:
        json_object = generate_json_object_from_file(arguments.file_path)
        pretty_print_json(json_object)
