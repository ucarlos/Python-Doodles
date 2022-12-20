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
    """."""
    string_list = string.split(" ")
    for i in range(len(string_list)):
        string_list[i] = string_list[i].capitalize()

    return " ".join(string_list)


def print_line(char, length):
    """."""
    print(f"{char}" * length)


def strip_artist_name(filename):
    """Given an string containing a filename in the form (Convention Name) [Artist_Name] Doujin Name*, Strip the Artist name using regular expressions."""
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
    """Check if a directory name contains characters from a specific language. If so, move it to a directory specified by the language directory name."""
    if contains_language_chraracter_callback(directory.name):
        language_folder = dummy_directory / language_directory_name
        print(fill(f"Moving {str(directory)} to {str(language_folder)}."))
        language_folder.mkdir(exist_ok=True)

        new_directory_path = language_folder / directory.name

        if new_directory_path.exists():
            # If for whatever reason, The folder already exists, simply move all of its children over.
            for directory_file in directory.iterdir():
                temp_file = new_directory_path / directory_file
                if temp_file.exists():
                    directory_file.unlink()
                else:
                    directory_file.rename(temp_file)
        # move(str(directory), str(language_folder))


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
                artist_name = capitalize_each_string_word(artist_name)
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

        subdirectory_name = sub_directory.name

        if contains_japanese_characters(subdirectory_name):
            pass
        elif contains_chinese_characters(subdirectory_name):
            pass
        elif contains_korean_characters(subdirectory_name):
            pass

        
        # check if the directory name is ASCII or not.
        try:
            dir_name = sub_directory.name
            dir_name.encode("latin1")
        except UnicodeEncodeError:
            # Directory name has Japanese Characters, so place it in
            # Japanese.

            ja_folder = dummy_directory / "[Japanese]"
            print(fill(f"Moving {sub_directory.name} to {ja_folder}...") + "\n")
            ja_folder.mkdir(exist_ok=True)
            move(str(sub_directory), str(ja_folder))
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
