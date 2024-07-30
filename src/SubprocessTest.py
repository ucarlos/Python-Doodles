#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Created by Ulysses Carlos on 07/29/2024 at 08:59 PM
#
# SubprocessTest.py
# A simple program to illustrate the usage of piped subprocess calls in
# Python. The main reason I wrote this was to hopefully make it easier to write
# the next time I have to run a piped command in Python.
# ------------------------------------------------------------------------------

from subprocess import run, PIPE, CompletedProcess
from shlex import split
from random import randint
MAX_SIZE = 500


def run_simple_command(number_list: list[str]):
    """Run a simple command to demonstrate a piped subprocess call."""
    concatenated_string = "\n".join(number_list)
    initial_command = f"printf \"{concatenated_string}\""
    secondary_command = "sort"
    final_command = "uniq"

    split_initial_command = split(initial_command)
    split_secondary_command = split(secondary_command)
    split_final_command = split(final_command)

    # NOTE: In the `subprocess.run` function in Python 3, the `input` and `stdin` options are used to provide input
    # data to the subprocess being executed.
    #
    # - The `input` option allows you to pass a bytes-like object or a string as input to the subprocess. This option
    # is convenient when you want to provide input directly as a parameter to the `subprocess.run` function.
    #
    # - The `stdin` option allows you to specify a file object from which the subprocess will read its input. You can
    # pass a file object opened in read mode or a file descriptor. This option is useful when you want to provide input
    # from a file or an existing stream.
    #
    # In summary:
    # - Use the `input` option when you want to directly provide input data as a parameter.
    # - Use the `stdin` option when you want the subprocess to read input from a file object or an existing stream.

    initial_process: CompletedProcess = run(split_initial_command, stdout=PIPE, stderr=PIPE,
                                            universal_newlines=True)
    secondary_process: CompletedProcess = run(split_secondary_command, input=initial_process.stdout, stdout=PIPE,
                                              universal_newlines=True)
    final_process: CompletedProcess = run(split_final_command, input=secondary_process.stdout, stdout=PIPE,
                                          universal_newlines=True)

    result = str(final_process.stdout)

    return result


if __name__ == "__main__":
    number_list = []
    for i in range(0, MAX_SIZE):
        random_number = randint(0, MAX_SIZE)
        random_number_string = f"{random_number: 05d}"
        number_list.append(random_number_string)

    # Now run the function:
    print(run_simple_command(number_list))
