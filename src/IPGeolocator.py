#!/usr/bin/env python3
# -------------------------------------------------------------------------------
# Created by Ulysses Carlos on 01/13/2024 at 01:59 PM
#
# IPLocator.py
# Simple script to be used on the raspberry pi to grab the geographical location
# of the various IPs that fail2ban bans for failed ssh logins.
#
# NOTE: This was originally created on 01/13/2024, and then updated on 01/16/2024.
# Due to some sensitive information, this script has been sanitized.
# -------------------------------------------------------------------------------

import mysql.connector
import requests
import logging
import json

import subprocess
from shlex import split

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def retrieve_current_banned_sshd_ips():
    """Retrieve a list of currently banned ips that attempted to login through SSH."""
    command_list = [
        "sudo fail2ban-client status sshd",
        "grep -Ei \"Banned IP list:\"",
        "awk -F : '{print $2;}'"
    ]

    # You'll have to use Popen since you're piping the results:
    process: subprocess.Popen = subprocess.Popen(split("printf \"\""))

    index = 0
    for command in command_list:
        stdin_value = process.stdout if index != 0 else None
        split_command = split(command)
        logging.debug(f"retrieve_currently_banned_sshd_ips(): Splitting {command} to {split_command}")
        logging.debug("retrieve_currently_banned_sshd_ips(): Now running the process:")
        logging.debug(f"retrieve_currently_banned_sshd_ips(): Current stdout value: {process.stdout}")
        process = subprocess.Popen(split_command, stdin=stdin_value, stdout=subprocess.PIPE)
        index += 1

    # Finally, use run to get back your result.
    last_process = subprocess.run("cat", stdin=process.stdout, capture_output=True)

    text_result = last_process.stdout.decode("utf-8").strip()

    ip_list = [] if not text_result else text_result.split(" ")

    logging.debug(f"retrieve_currently_banned_sshd_ips(): IP List: {ip_list}")
    return ip_list


def find_ip_geography_info(ip_address: str):
    """Identify the geographic information for the passed IP Address by creating a GET Request to geolocation-db.com"""
    url_path = f"https://geolocation-db.com/jsonp/{ip_address}"
    try:
        request: requests.Response = requests.get(url_path)
        request.raise_for_status()

    except requests.HTTPError:
        logging.error(f"Error: HTTP GET Request to {url_path} failed. Here's the reason: {request.reason}.\n"
                      f"Here's the raw text that was returned: {request.text}")
        exit(EXIT_FAILURE)

    # # Now remove the callback() text from the json and then transform it:
    request.encoding = "utf-8"
    raw_json = request.text[9:-1]
    return raw_json


def identify_all_ip_addresses(raw_ip_address_list: list):
    """Retrieve the geographic information for each IP Address by making a HTTP request to geolocation-db.com"""
    information_dict = {}

    if not raw_ip_address_list:
        return information_dict

    for ip_address in raw_ip_address_list:
        # Skip any empty ip_address if it occurs:
        if not ip_address:
            logging.debug("retrieve_geographic_ip_information(): Skipping Empty IP Addresses.")
            continue

        raw_json = find_ip_geography_info(ip_address)
        json_object = json.loads(raw_json)

        information_dict.update({ip_address: json_object})

    return information_dict


def display_ip_address_list(ip_address_dict: dict):
    """Display each currently banned IP along with its geographic information."""
    if not ip_address_list:
        print("No Banned IP Addresses were detected :(")
        return

    print("The following IP Addresses attempted to brute force an SSH login into this machine:")
    for ip_address, json_object in ip_address_dict.items():
        country_name = "Unknown Country" if not json_object['country_name'] else json_object['country_name']
        city = "Unknown City" if not json_object["city"] else json_object["city"]
        state = "Unknown State" if not json_object["state"] else json_object["state"]
        latitude = json_object["latitude"]
        longitude = json_object["longitude"]

        info_string = f"{ip_address}\t Address: {city}, {state}, {country_name}    Lat/Long: {latitude}, {longitude}"
        print(info_string)


def create_connection(hostname, username, user_password, database_name):
    """Create a database connection."""
    connection = None
    logging.debug("create_connection: Attempting to connect using passed credentials...")
    try:
        connection = mysql.connector.connect(host=hostname, user=username, passwd=user_password, database=database_name)

    except mysql.connector.Error as error:
        print(f"Error: Could not create connection. Here's the error message : {error}")
        exit(EXIT_FAILURE)

    logging.debug("create_connection: Connection Success! Now returning a connection object.")
    return connection


def insert_new_ip_address_entry(connection, cursor, ip_address, json_object: dict):
    """Insert a new IP Address Entry."""
    insert_query = """
    REPLACE INTO sshd_banned_ip_database (ip_address, city, state, country, latitude, longitude)
    VALUES(%s, %s, %s, %s, %s, %s)
    """

    parameter_list = []

    country_name = "Unknown Country" if not json_object['country_name'] else json_object['country_name']
    city = "Unknown City" if not json_object["city"] else json_object["city"]
    state = "Unknown State" if not json_object["state"] else json_object["state"]

    latitude = json_object["latitude"]
    latitude = 0.0 if (not latitude or latitude == "Not found") else latitude

    longitude = json_object["longitude"]
    longitude = 0.0 if (not longitude or longitude == "Not found") else longitude

    temp_tuple = (ip_address, city, state, country_name, latitude, longitude)
    parameter_list.append(temp_tuple)

    logging.debug(f"insert_ip_addresses_into_database(): Generated Replace Query:\n{insert_query}")
    logging.debug(f"insert_ip_addresses_into_database(): Parameter list: {parameter_list}")

    try:
        cursor.executemany(insert_query, parameter_list)
        connection.commit()
        logging.debug(f"insert_ip_addresses_into_database(): Inserted {ip_address} into the database.")

    except mysql.connector.Error as error:
        print(f"Error: Could not insert {ip_address} into the database. Here's the error: {error}")
        exit(EXIT_FAILURE)


def update_ip_address_entry(connection, cursor, ip_address, json_object: dict):
    """Update the IP Address Entry."""
    update_query = """
    UPDATE sshd_banned_ip_database
    SET last_ban_timestamp = NOW()
    WHERE ip_address = %s
    """
    specified_value = (ip_address,)

    logging.debug(f"insert_ip_addresses_into_database(): Generated Update Query:\n{update_query}")

    try:
        cursor.execute(update_query, specified_value)
        connection.commit()
        logging.debug(f"insert_ip_address_into_database(): Updated last ban timestamp for {ip_address}")

    except mysql.connector.Error as error:
        print(f"insert_ip_address_into_database(): Could not update the last ban timestamp for {ip_address} "
              f"Here's the error:\n{error}")
        exit(EXIT_FAILURE)


def add_ip_address_to_database(connection, ip_address, json_object: dict):
    """Insert an ip address into the database."""
    result_list = None
    cursor = connection.cursor(prepared=True)

    # First, check if the ip_address has been logged before.
    select_query = """SELECT ip_address from sshd_banned_ip_database where ip_address = %s"""

    # PROTIP: You need a comma for every parameter you pass to execute, even it's
    # a single parameter.
    specified_value = (ip_address,)

    logging.debug(f"insert_ip_address_into_database(): Checking if IP Address {ip_address} has been logged before...")
    try:
        cursor.execute(select_query, specified_value)
        result_list = cursor.fetchall()
        connection.commit()
        logging.debug("insert_ip_address_into_database(): Results of select query was stored in result_list.")

    except mysql.connector.Error as error:
        print(f"insert_ip_address_into_database(): Could not check if {ip_address} has been logged before. "
              f"Here's the error:\n{error}")
        exit(EXIT_FAILURE)

    if not result_list:
        # If not, then insert it into the database
        insert_new_ip_address_entry(connection, cursor, ip_address, json_object)
    else:
        # Otherwise, just update the last time it was seen.
        update_ip_address_entry(connection, cursor, ip_address, json_object)


def insert_ip_addresses_into_database(ip_address_dict: dict):
    """Insert the list of IP Addresses into the database."""
    if not ip_address_list:
        print("Warning: No banned IP addresses were detected.")
        return

    hostname = "[REDACTED]"
    username = "[REDACTED]"
    password = "[REDACTED]"
    database = "[REDACTED]"

    connection = create_connection(hostname, username, password, database)

    for ip_address, json_object in ip_address_dict.items():
        add_ip_address_to_database(connection, ip_address, json_object)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ip_address_list = retrieve_current_banned_sshd_ips()
    discovered_ip_address_dict = identify_all_ip_addresses(ip_address_list)
    insert_ip_addresses_into_database(discovered_ip_address_dict)
    display_ip_address_list(discovered_ip_address_dict)
