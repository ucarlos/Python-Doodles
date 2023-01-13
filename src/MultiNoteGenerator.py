#!/usr/bin/env python3
# -------------------------------------------------------------------------------
# Created by Ulysses Carlos on 06/11/2022 at 01:40 PM
#
# MultiNoteGenerator.py
#
# -------------------------------------------------------------------------------

# For Emacs debug test with realgud
# import ipdb
from copy import copy


def generate_multi_notes(single_note_list):
    """Generate Multi notes."""
    unique_note_list = copy(single_note_list)
    multi_note_list = []

    for note in single_note_list:
        # First remove the note from the unique_note_list
        unique_note_list.remove(note)

        # Now for each item in the unique_note, make the combination
        for unique_note in unique_note_list:
            multi_note = (f"{note[0]}.{unique_note[0]}", f"{note[1]} and {unique_note[1]}")
            multi_note_list.append(multi_note)

    return list(set(multi_note_list))


def main():
    single_note_list = [
        ("resultcode.example.zero", "Example Zero"),
        ("resultcode.example.one", "Example One"),
        ("resultcode.example.two", "Example Two"),
        ("resultcode.example.three", "Example Three")
        ]

    print(f"{single_note_list}\n")

    multi_note_list = generate_multi_notes(single_note_list)
    print("Size of Multi Note List: ", len(multi_note_list))

    output_list = []
    other_settings = [1, 1, 1, 0, 0, 0]

    for multi_note in multi_note_list:
        other_settings_string = ", ".join(map(str, other_settings))
        output_list.append(f"('{multi_note[0]}', '{multi_note[1]}',{other_settings_string}),\n")

    # Now remove the last comma on the last line:
    last_line = output_list.pop()
    last_line = last_line[:len(last_line) - 2] + ";\n"
    output_list.append(last_line)

    with open("Multi-Note-Ouput.txt", "w") as output_file:
        output_file.writelines(output_list)


if __name__ == "__main__":
    main()
