#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Created by Ulysses Carlos on 01/25/2021 at 08:32 PM
#
# Convert_WAV_To_Flac.py
# Requires ffmpeg to be installed on the system.
# ------------------------------------------------------------------------------
from pydub import AudioSegment
from pathlib import Path

root_directory = Path().cwd()
accepted_formats = [".wav"]


def convert_file(wav_path):
    """
    Convert WAV file located in wav_path to flac, keeping the file name.
    """
    original_file = None
    if wav_path.suffix == accepted_formats[0]:
        original_file = AudioSegment.from_file(str(wav_path), format='wav')
    # else:
    #     original_file = AudioSegment.from_file(str(wav_path), format='pcm')
    # original_file = AudioSegment.from_file(str(wav_path), format='wav')

    filename = str(wav_path.name)[: -4]
    original_file.export(f"{filename}.flac", format='flac')
    # print(f"{filename}")


def directory_convert():
    pathlist = root_directory.glob("*")
    for file in pathlist:

        if file.suffix in accepted_formats:
            convert_file(file)
            # print(f"{file.name} is an accepted format")
        else:
            print(f"{file.name} is not an accepted format. Skipping.")
            continue


if __name__ == "__main__":
    directory_convert()
