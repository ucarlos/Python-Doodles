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
import re
import logging

# Global variables
accepted_formats = ['.zip', '.rar', '.cbz']
panda_directory = Path.home() / "Pictures" / ".sadpanda"
current_directory = Path.cwd()
dummy_directory = Path.cwd() / "dummy_directory"


def capitalize_each_string_word(string):
    string_list = string.split(" ")
    for i in range(len(string_list)):
        string_list[i] = string_list[i].capitalize()

    return " ".join(string_list)


def print_line(char, length):
    print(f"{char}" * length)


def strip_artist_name(filename):
    """
    Given an string containing a filename in the form
    (Convention Name) [Artist_Name] Doujin Name*,
    Strip the Artist name using regular expressions.
    """

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


def organize_doujins_by_artist():
    """
    Organize Doujinishi by Artist Name by parsing their filename and placing
    the file into a directory with name {Artist_Name}.
    """
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
                artist_name = capitalize_each_string_word(artist_name)
                artist_directory = current_directory / artist_name
                artist_directory.mkdir(exist_ok=True)
                move(str(file), str(artist_directory))
            else:
                print(fill(f"SKIPPING {file.name}...") + "\n")
    print_line("-", 80)
    print("")


def move_to_dummy_directory():
    """
    Place all the Artist directories into single-letter directories
    in {dummy_directory}.
    """
    print_line("-", 80)
    print(fill(f"Now placing directories into {dummy_directory} ...\n") + "\n")
    sleep(1)

    for sub_dir in current_directory.iterdir():
        logging.debug(f"move_to_dummy_directory(): Testing {str(sub_dir)}")
        if not sub_dir.is_dir() or sub_dir == dummy_directory:
            continue

        # check if the directory name is ASCII or not.
        try:
            dir_name = sub_dir.name
            dir_name.encode("latin1")
        except UnicodeEncodeError:
            # Directory name has Japanese Characters, so place it in
            # Japanese.

            ja_folder = dummy_directory / "[Japanese]"
            print(fill(f"Moving {sub_dir.name} to {ja_folder}...") + "\n")
            ja_folder.mkdir(exist_ok=True)
            move(str(sub_dir), str(ja_folder))
            continue

        # Otherwise, place it in a folder with the first
        # character of the artist.
        new_folder_name = str(sub_dir.name)
        new_folder_name = new_folder_name[:1].upper()

        new_folder = dummy_directory / new_folder_name
        print(fill(f"Moving {sub_dir.name} to {new_folder}...") + "\n")
        new_folder.mkdir(exist_ok=True)

        # If the folder exists, simply move the contents of the subdirectory to the new folder.
        possible_path = new_folder / sub_dir.name

        logging.debug(f"move_to_dummy_directory(): Possible Path: {str(possible_path)}")
        if possible_path.exists():
            for doujin in sub_dir.iterdir():
                logging.debug(f"move_to_dummy_directory(): Doujin Path: {str(doujin)}")
                if doujin.is_file():
                    # Handle duplicates:
                    if Path(possible_path / doujin.name).exists():
                        print(f"Warning: \"{doujin.name}\" already exists, deleting...")
                        doujin.unlink()
                    else:
                        move(str(doujin), str(possible_path))

            # Now delete the sub_dir:
            logging.debug(f"move_to_dummy_directory(): Deleting {str(sub_dir)}")
            rmtree(sub_dir)
        else:
            move(str(sub_dir), str(new_folder))

    print_line("-", 80)


def main():
    # First, check if directory has formats
    # in accepted_formats list.
    # If so, then run the sort.
    logging.basicConfig(level=logging.DEBUG)
    dummy_directory.mkdir(exist_ok=True)
    organize_doujins_by_artist()
    move_to_dummy_directory()


# Run the program.
if __name__ == "__main__":
    main()
