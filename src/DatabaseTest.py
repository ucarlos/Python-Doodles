#!/usr/bin/env python3
# -------------------------------------------------------------------------------
# Created by Ulysses Carlos on 02/03/2023 at 09:00 PM
#
# DatabaseTest.py
# A Simple program to help me learn how to use mysql.connector.
# -------------------------------------------------------------------------------

from enum import Enum
import logging
import mysql.connector
from mysql.connector import Error as MySQLError


class EXIT_CODE(Enum):
    """Simple Exit Code enum."""

    SUCCESS = 0,
    FAILURE = 1


def create_connection(hostname, username, user_password, database_name):
    """Create a connection."""
    connection = None
    logging.debug("create_connection: Attempting to connect using passed credentials...")
    try:
        connection = mysql.connector.connect(host=hostname, user=username, passwd=user_password, database=database_name)

    except MySQLError as error:
        print(f"Error: {error}")
        # logging.info(f"Error: {error}")

    logging.debug("create_connection: Connection Success! Now returning a connection object.")
    return connection


def create_dummy_table(connection):
    """Create a dummy table in the database."""
    cursor = connection.cursor(prepared=True)
    query = """
    CREATE table IF NOT EXISTS dummy(
    id bigint NOT NULL AUTO_INCREMENT,
    firstname varchar(255) not null,
    lastname varchar(255) not null,
    constraint pk_dummy primary key (id, firstname, lastname),
    unique index index_name(firstname, lastname))
    """

    logging.debug("create_dummy_table: Attempting to create predefined dummy table.")
    try:
        cursor.execute(query)
        connection.commit()
        logging.info("create_dummy_table: Dummy table was created successfully.")
    except MySQLError as error:
        print(f"Error: {error}")
        exit(EXIT_CODE.FAILURE)


def insert_into_dummy_table(connection, row_list):
    """Insert into the dummy_table."""
    if not row_list:
        logging.debug("insert_into_dummy_table: Aborting since row_list is empty.")
        return

    cursor = connection.cursor(prepared=True)

    query = """INSERT IGNORE INTO dummy(firstname, lastname) VALUES (%s,%s)"""
    parameter_list = []

    for row in row_list:
        temp_tuple = (row["firstname"], row["lastname"])
        parameter_list.append(temp_tuple)

    # Now remove the last character:

    logging.debug(f"insert_into_dummy_table: Generated Query:\n{query}")
    logging.debug(f"insert_into_dummy_table: Parameter list: {parameter_list}")
    try:
        cursor.executemany(query, parameter_list)
        connection.commit()
        logging.info(f"insert_into_dummy_table: Data was inserted successfully.")

    except MySQLError as error:
        print(f"Error: {error}")
        exit(EXIT_CODE.FAILURE)


def select_from_dummy_table(connection):
    """Select rows from the dummy table."""
    result_list = None
    cursor = connection.cursor(prepared=True)

    query = """SELECT id, firstname, lastname from dummy where id > %s """

    # PROTIP: You need a comma for every parameter you pass to execute, even it's
    # a single parameter
    specified_value = (0,)

    logging.debug(f"select_from_dummy_table: Attempting to execute query {query} with {specified_value}")
    try:
        cursor.execute(query, specified_value)
        result_list = cursor.fetchall()
        connection.commit()
        logging.info("select_from_dummy_table: Results of select query was stored in result_list.")

    except MySQLError as error:
        print(f"Error: {error}")
        exit(EXIT_CODE.FAILURE)

    return result_list


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    options = {
               "hostname": "localhost",
               "username": "dummyuser",
               "password": "ExamplePassword.",
               "database": "test"
               }

    connection = create_connection(options['hostname'], options["username"], options["password"], options["database"])

    create_dummy_table(connection)
    row_list = [{"firstname": "John", "lastname": "Smith"},
                {"firstname": "Jane", "lastname": "Doe"}]

    insert_into_dummy_table(connection, row_list)
    result_list = select_from_dummy_table(connection)

    print(result_list)
    print("Now attempting to iterate through the result_list:")
    for row in result_list:
        print(row)
