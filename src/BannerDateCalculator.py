#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Created by Ulysses Carlos on 05/18/2024 at 12:52 PM
#
# BannerDateCalculator.py
#
# ------------------------------------------------------------------------------

from datetime import datetime
from dateutil.relativedelta import relativedelta

ZFILL_LENGTH = 2


class RelativeDateDifference(object):
    """Create the child function"""
    def __init__(self, start_date, end_date, fill_length=ZFILL_LENGTH):
        """Create the child function"""
        self._start_date = start_date
        self._end_date = end_date
        self._fill_length = fill_length
        self._relativedelta_date_difference: relativedelta = relativedelta(end_date, start_date)
        self._date_difference = end_date - start_date

    def __str__(self):
        """Print the function."""
        difference_string = (f"{self._relativedelta_date_difference.years} Years "
                             f"{str(self._relativedelta_date_difference.months).zfill(self._fill_length)} Months "
                             f"{str(self._relativedelta_date_difference.days).zfill(self._fill_length)} "
                             f"Days {str(self._relativedelta_date_difference.hours).zfill(self._fill_length)}:"
                             f"{str(self._relativedelta_date_difference.minutes).zfill(self._fill_length)}:"
                             f"{str(self._relativedelta_date_difference.seconds).zfill(self._fill_length)} "
                             f"({self._date_difference})")
        return difference_string


if __name__ == "__main__":
    current_date = datetime.today()
    current_birthday = datetime(current_date.year, 2, 15, 22, 5)
    new_years_date = datetime(current_date.year, 1, 1, 0, 0)
    departure_date = datetime(2022, 11, 1, 1)
    graduation_date = datetime(2020, 12, 18, 14, 7)
    exercise_date = datetime(2023, 9, 16)
    driving_date = datetime(2023, 10, 17)


    if current_birthday > current_date:
        # Decrement the birthday year
        current_birthday.replace(year=current_date.year - 1)

    # Now, provide the difference for the months:

    birthday_date_difference: RelativeDateDifference = RelativeDateDifference(current_birthday, current_date)
    new_years_date_difference: RelativeDateDifference = RelativeDateDifference(new_years_date, current_date)
    departure_date_difference: RelativeDateDifference = RelativeDateDifference(departure_date, current_date)
    graduation_date_difference: RelativeDateDifference = RelativeDateDifference(graduation_date, current_date)
    exercise_date_difference: RelativeDateDifference = RelativeDateDifference(exercise_date, current_date)
    driving_date_difference: RelativeDateDifference = RelativeDateDifference(driving_date, current_date)

    formatted_new_years_string = new_years_date.strftime("%Y-%m-%d")
    formatted_birthday_string = current_birthday.strftime("%Y-%m-%d")
    formatted_departure_string = departure_date.strftime("%Y-%m-%d")
    formatted_graduation_string = graduation_date.strftime("%Y-%m-%d")
    formatted_exercise_string = exercise_date.strftime("%Y-%m-%d")
    formatted_driving_string = driving_date.strftime("%Y-%m-%d")

    print(f"Days since College Graduation ({formatted_graduation_string}): {graduation_date_difference}")
    print(f"Days since Dad's Departure    ({formatted_departure_string}): {departure_date_difference}\n")

    print(f"Days since New Years Day ({formatted_new_years_string}): {new_years_date_difference}")
    print(f"Days since Last Birthday ({formatted_birthday_string}): {birthday_date_difference}\n")

    print(f"Days since I started exercising    ({formatted_exercise_string}): {exercise_date_difference}")
    print(f"Days since I started driving again ({formatted_driving_string}): {driving_date_difference}")

