#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Created by Ulysses Carlos on 07/25/2020 at 11:00 PM
#
# Move_Doujinishi.py
# Python version of Move_Doujinishi.sh, which sorts doujins by artist name
# and then places them into the directory located in {dummy_directory}.
# ------------------------------------------------------------------------------

# Modules
from pathlib import Path
from shutil import move
from shutil import rmtree
from time import sleep
from textwrap import fill
from shlex import split
from subprocess import run
import re
import logging

# Global variables
accepted_formats = ['.zip', '.rar', '.cbz']
panda_directory = Path.home() / "Pictures" / ".sadpanda"
current_directory = Path.cwd()
dummy_directory = Path.cwd() / "dummy_directory"
doujinshi_directory = current_directory.parent / "Doujins by Author"


# variables to handle color:
class TermColor:
    """Small class made to display color in print statements."""

    RED = "\033[91m"
    CLEAR = "\033[0m"
    BLUE = "\033[94m"
    BOLD = '\033[1m'


def capitalize_each_string_word(string):
    """."""
    string_list = string.split(" ")
    for i in range(len(string_list)):
        string_list[i] = string_list[i].capitalize()

    return " ".join(string_list)


def print_line(char, length):
    """."""
    print(f"{char}" * length)


def strip_artist_name(filename):
    """Given an string containing a filename in the form (Convention Name) [Artist_Name] Doujin Name*,
    Strip the Artist name using regular expressions."""
    # First confirm that the filename follows the following formats:
    # (CONVENTION) [Group Name (Artist_Name)] Title
    # [Group Name (Artist_Name)] Title
    # [Artist Name] Title
    initial_pattern = r"^(\(.+\))?\s*\[.+(\(.+\))?\].+$"
    initial_match = re.search(initial_pattern, filename)

    if initial_match is None:
        return "UNKNOWN ARTIST"

    # Extract the string containing the group name (if found)
    # print(f"Initial pattern matches for {filename}...")
    second_pattern = r"\[[^\]\(]*(\([^\)]*\))?[^\]]*"

    result_string = re.search(second_pattern, filename).group(0)[1:]

    # Check if the string contains a group name
    third_pattern = r"\([^\)]*"
    third_match = re.search(third_pattern, result_string)

    if (third_match is None):
        # artist = result_string[1:]
        return result_string
    else:
        # Determine if the name in the () is a list of authors.
        # If so, simply use the group name instead.
        artist = third_match.group(0)[1:]

        search_comma = artist.find(",")
        if (search_comma != -1):
            fourth_pattern = r"[^\(]*"
            fourth_match = re.search(fourth_pattern, result_string)
            return fourth_match.group(0)
        else:
            return artist


def contains_eastern_characters(directory_name):
    """Check if a directory name contains Japanese/Chinese/Korean characters."""
    japanese_pattern = r"[一-龠]+|[ぁ-ゔ]+|[ァ-ヴー]+|[々〆〤ヶ]+"
    korean_pattern = r"[\u1100-\u11FF\u3130-\u318F\uA960-\uA97F\uAC00-\uD7AF\uD7B0-\uD7FF]"
    chinese_pattern = r"[\u4e00-\u9fff]+"

    complete_pattern = f"({japanese_pattern})|({korean_pattern})|({chinese_pattern})"

    match = re.search(complete_pattern, directory_name)

    return True if match else False


def contains_japanese_characters(directory_name):
    """Check if a directory name contains Japanese characters."""
    japanese_pattern = r"[一-龠]+|[ぁ-ゔ]+|[ァ-ヴー]+|[々〆〤ヶ]+"

    match = re.search(japanese_pattern, directory_name)

    return True if match else False


def contains_korean_characters(directory_name):
    """Check if a directory name contains Korean characters."""
    korean_pattern = r"[\u1100-\u11FF\u3130-\u318F\uA960-\uA97F\uAC00-\uD7AF\uD7B0-\uD7FF]"

    match = re.search(korean_pattern, directory_name)

    return True if match else False


def contains_chinese_characters(directory_name):
    """Check if a directory name contains Chinese characters."""
    chinese_pattern = r"[\u4e00-\u9fff]+"
    match = re.search(chinese_pattern, directory_name)

    return True if match else False


def check_and_move_if_directory_name_has_language_chars(directory,
                                                        contains_language_chraracter_callback,
                                                        language_directory_name):
    """Check if a directory name contains characters from a specific language.
    If so, move it to a directory specified by the language directory name.

    Returns True if the directory contained the language characters. Otherwise, it returns False.
    """
    # Immediately fail if the directory doesn't exist.
    if not directory.exists():
        return False

    if contains_language_chraracter_callback(directory.name):
        language_folder = dummy_directory / language_directory_name
        print(fill(f"Moving {str(directory)} to {str(language_folder)}."))
        language_folder.mkdir(exist_ok=True)

        new_directory_path = language_folder / directory.name

        if new_directory_path.exists():
            # If for whatever reason, The folder already exists, simply move all of its children over.
            for directory_file in directory.iterdir():
                temp_file = new_directory_path / directory_file
                # If the file exists in the new directory, simply delete it.
                if temp_file.exists():
                    directory_file.unlink()
                else:
                    directory_file.rename(temp_file)
        else:
            directory.rename(new_directory_path)

        return True
        # move(str(directory), str(language_folder))
    else:
        return False


def organize_doujins_by_artist():
    """Organize Doujinishi by Artist Name by parsing their filename and placing the file into a directory with name {Artist_Name}."""
    print_line("-", 80)
    print("Organizing Doujins by Artist...\n")
    sleep(1)

    with open("output.txt", "w") as output_file:
        for file in current_directory.iterdir():
            # Skip any directories
            if file.is_dir():
                continue

            if file.suffix in accepted_formats:
                # Now handle lowercase artists:
                artist_name = strip_artist_name(file.stem).lower()
                print(fill(f"Placing {file.name} into {artist_name}/ ...") + "\n")
                output_file.write(f"Filename: \"{file.name}\"\n")
                output_file.write(f"Artist Name: {artist_name}\n\n")

                # Create a directory with name artist name and move the file to a directory.
                # Capitalize first character in each word:
                artist_name = capitalize_each_string_word(artist_name).strip()
                artist_directory = current_directory / artist_name
                artist_directory.mkdir(exist_ok=True)
                move(str(file), str(artist_directory))
            else:
                print(fill(f"SKIPPING {file.name}...") + "\n")
    print_line("-", 80)
    print("")


def move_to_dummy_directory():
    """Place all the Artist directories into single-letter directories in {dummy_directory}."""
    print_line("-", 80)
    print(fill(f"Now placing directories into {dummy_directory} ...\n") + "\n")
    sleep(1)

    for sub_directory in current_directory.iterdir():
        logging.debug(f"move_to_dummy_directory(): Testing {str(sub_directory)}")
        if not sub_directory.is_dir() or sub_directory == dummy_directory:
            continue

        # subdirectory_name = sub_directory.name
        if contains_eastern_characters(sub_directory.name):
            check_and_move_if_directory_name_has_language_chars(sub_directory,
                                                                contains_japanese_characters,
                                                                "[Japanese]")
            check_and_move_if_directory_name_has_language_chars(sub_directory,
                                                                contains_korean_characters,
                                                                "[Korean]")
            check_and_move_if_directory_name_has_language_chars(sub_directory,
                                                                contains_chinese_characters,
                                                                "[Chinese]")
            continue

        # check if the directory name is ASCII or not.
        try:
            dir_name = sub_directory.name
            dir_name.encode("latin1")
        except UnicodeEncodeError:
            # Directory name contains unknown characters, so place it in the [Unknown] directory.

            unknown_folder = dummy_directory / "[Unknown]"
            print(fill(f"Moving {sub_directory.name} to {unknown_folder}...") + "\n")
            unknown_folder.mkdir(exist_ok=True)
            move(str(sub_directory), str(unknown_folder))
            continue

        # Otherwise, place it in a folder with the first
        # character of the artist.
        new_folder_name = str(sub_directory.name)
        new_folder_name = new_folder_name[:1].upper()

        new_folder = dummy_directory / new_folder_name
        print(fill(f"Moving {sub_directory.name} to {new_folder}...") + "\n")
        new_folder.mkdir(exist_ok=True)

        # If the folder exists, simply move the contents of the subdirectory to the new folder.
        possible_path = new_folder / sub_directory.name

        logging.debug(f"move_to_dummy_directory(): Possible Path: {str(possible_path)}")
        if possible_path.exists():
            for doujin in sub_directory.iterdir():
                logging.debug(f"move_to_dummy_directory(): Doujin Path: {str(doujin)}")
                if doujin.is_file():
                    # Handle duplicates:
                    if Path(possible_path / doujin.name).exists():
                        print(f"Warning: \"{doujin.name}\" already exists, deleting...")
                        doujin.unlink()
                    else:
                        move(str(doujin), str(possible_path))

            # Now delete the sub_dir:
            logging.debug(f"move_to_dummy_directory(): Deleting {str(sub_directory)}")
            rmtree(sub_directory)
        else:
            move(str(sub_directory), str(new_folder))

    print_line("-", 80)
    print(f"{TermColor.BOLD}")
    option = input(f"Do you want to merge the subdirectories into {str(doujinshi_directory)}? [y/n] ")
    print(f"{TermColor.CLEAR}")

    if option.lower() == "y":
        merge_into_doujinshi_directory()
    else:
        print("Complete!")


def merge_into_doujinshi_directory():
    """Merge the subdirectories found in the dummy directory into the doujinshi directory."""
    print(f"Now merging subdirectories into {str(doujinshi_directory)}...")
    for directory in dummy_directory.iterdir():
        if not directory.is_dir():
            logging.debug(f"merge_into_doujinshi_directory(): Skipping {directory.name} since it is not a directory.")
            continue

        # Generate a rsync call to merge the directory:
        rsync_command = f"rsync -avLP --ignore-existing --remove-source-files \"{directory}\" \"{doujinshi_directory}\""
        logging.debug(f"merge_into_doujinshi_directory(): Running the following Rsync Command: {rsync_command}")
        split_rsync_command = split(rsync_command)
        logging.debug(f"merge_into_doujinshi_directory(): Split Rsync Command: {split_rsync_command}")

        # Now run the damn thing:
        run(split_rsync_command)
        # Now make sure that the directory and its contents are deleted:
        subdirectory_contents = directory.rglob("*")
        existing_doujinshi_file_list = []
        for file in subdirectory_contents:
            if (file.suffix in accepted_formats):
                existing_doujinshi_file_list.append(file)

        if existing_doujinshi_file_list:
            print(f"{TermColor.RED}Unmoved Doujinshi have been detected in {str(directory)}{TermColor.CLEAR}")
            # print(f"{TermColor.RED}These are most likely duplicates.{TermColor.CLEAR}")

            for existing_doujinshi in existing_doujinshi_file_list:
                print(f"{TermColor.RED}    * {existing_doujinshi.name}{TermColor.CLEAR}")
            user_input = input("These are most likely duplicates, so would you like to delete them? [y/n] ").lower()
            if user_input == "y":
                for existing_doujinshi in existing_doujinshi_file_list:
                    existing_doujinshi.unlink()

                # Also delete the whole directory as well:
                rmtree(str(directory))
                print(f"{TermColor.BLUE}Files and directory have been deleted. :){TermColor.CLEAR}")
            else:
                print(f"{TermColor.BLUE}Alright, I hope you know what you're doing then.{TermColor.CLEAR}")
        else:
            # Delete fucking everything:
            logging.debug(f"merge_into_doujinshi_directory(): Clearing out everything in {str(directory)}")
            rmtree(str(directory))

    print_line("-", 80)
    print("Complete!")


# Run the program.
if __name__ == "__main__":
    # First, check if directory has formats
    # in accepted_formats list.
    # If so, then run the sort.
    logging.basicConfig(level=logging.INFO)
    dummy_directory.mkdir(exist_ok=True)
    organize_doujins_by_artist()
    move_to_dummy_directory()
