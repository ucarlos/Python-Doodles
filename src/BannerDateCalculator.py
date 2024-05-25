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


class DateDifference(object):
    """Create the child function"""
    def __init__(self, start_date, end_date, fill_length=ZFILL_LENGTH):
        """Create the child function"""
        self._start_date = start_date
        self._end_date = end_date
        self._relativedelta_date_difference: relativedelta = relativedelta(end_date, start_date)
        self._date_difference = end_date - start_date

    def __str__(self):
        """Print the function."""
        difference_string = (f"{self._relativedelta_date_difference.years} Years "
                             f"{str(self._relativedelta_date_difference.months).zfill(ZFILL_LENGTH)} Months "
                             f"{str(self._relativedelta_date_difference.days).zfill(ZFILL_LENGTH)} "
                             f"Days {str(self._relativedelta_date_difference.hours).zfill(ZFILL_LENGTH)}:"
                             f"{str(self._relativedelta_date_difference.minutes).zfill(ZFILL_LENGTH)}:"
                             f"{str(self._relativedelta_date_difference.seconds).zfill(ZFILL_LENGTH)} "
                             f"({self._date_difference})")
        return difference_string


if __name__ == "__main__":
    current_date = datetime.today()
    current_birthday = datetime(current_date.year, 2, 15, 22, 5)
    new_years_date = datetime(current_date.year, 1, 1, 0, 0)
    departure_date = datetime(2022, 11, 1, 1)
    graduation_date = datetime(2020, 12, 18, 14, 7)
    exercise_date = datetime(2023, 9, 16)

    if current_birthday > current_date:
        # Decrement the birthday year
        current_birthday.replace(year=current_date.year - 1)

    # Now, provide the difference for the months:
    relative_birthday_difference: relativedelta = relativedelta(current_date, current_birthday)
    relative_new_years_date_difference: relativedelta = relativedelta(current_date, new_years_date)
    relative_departure_date_difference: relativedelta = relativedelta(current_date, departure_date)
    relative_graduation_date_difference: relativedelta = relativedelta(current_date, graduation_date)
    relative_exercise_date_difference: relativedelta = relativedelta(current_date, exercise_date)

    # Now use normal delta
    birthday_difference = current_date - current_birthday
    new_years_date_difference = current_date - new_years_date
    departure_date_difference = current_date - departure_date
    graudation_departure_date_difference = current_date - graduation_date
    exercise_date_difference = current_date - exercise_date

    birthday_difference_string = (f"{str(relative_birthday_difference.months).zfill(ZFILL_LENGTH)} Months "
                                  f"{str(relative_birthday_difference.days).zfill(ZFILL_LENGTH)} "
                                  f"Days {str(relative_birthday_difference.hours).zfill(ZFILL_LENGTH)}:"
                                  f"{str(relative_birthday_difference.minutes).zfill(ZFILL_LENGTH)}:"
                                  f"{str(relative_birthday_difference.seconds).zfill(ZFILL_LENGTH)} "
                                  f"({birthday_difference})")

    current_year_to_date_string = (f"{str(relative_new_years_date_difference.months).zfill(ZFILL_LENGTH)} Months "
                                   f"{str(relative_new_years_date_difference.days).zfill(ZFILL_LENGTH)} Days "
                                   f"{str(relative_new_years_date_difference.hours).zfill(ZFILL_LENGTH)}:"
                                   f"{str(relative_new_years_date_difference.minutes).zfill(ZFILL_LENGTH)}:"
                                   f"{str(relative_new_years_date_difference.seconds).zfill(ZFILL_LENGTH)} "
                                   f"({new_years_date_difference})")

    departure_date_string = (f"{relative_departure_date_difference.years} Years "
                             f"{str(relative_departure_date_difference.months).zfill(ZFILL_LENGTH)} Months "
                             f"{str(relative_departure_date_difference.days).zfill(ZFILL_LENGTH)} Days "
                             f"{str(relative_departure_date_difference.hours).zfill(ZFILL_LENGTH)}:"
                             f"{str(relative_departure_date_difference.minutes).zfill(ZFILL_LENGTH)}:"
                             f"{str(relative_departure_date_difference.seconds).zfill(ZFILL_LENGTH)} "
                             f"({departure_date_difference})")

    graduation_departure_date_string = (f"{relative_graduation_date_difference.years} Years "
                                        f"{str(relative_graduation_date_difference.months).zfill(ZFILL_LENGTH)} Months "
                                        f"{str(relative_graduation_date_difference.days).zfill(ZFILL_LENGTH)} Days "
                                        f"{str(relative_graduation_date_difference.hours).zfill(ZFILL_LENGTH)}:"
                                        f"{str(relative_graduation_date_difference.minutes).zfill(ZFILL_LENGTH)}:"
                                        f"{str(relative_graduation_date_difference.seconds).zfill(ZFILL_LENGTH)} "
                                        f"({graudation_departure_date_difference})")

    graduation_departure_date_string = (f"{relative_exercise_date_difference.years} Years "
                                        f"{str(relative_exercise_date_difference.months).zfill(ZFILL_LENGTH)} Months "
                                        f"{str(relative_exercise_date_difference.days).zfill(ZFILL_LENGTH)} Days "
                                        f"{str(relative_exercise_date_difference.hours).zfill(ZFILL_LENGTH)}:"
                                        f"{str(relative_exercise_date_difference.minutes).zfill(ZFILL_LENGTH)}:"
                                        f"{str(relative_exercise_date_difference.seconds).zfill(ZFILL_LENGTH)} "
                                        f"({exercise_date_difference})")

    formatted_new_years_string = new_years_date.strftime("%Y-%m-%d")
    formatted_birthday_string = current_birthday.strftime("%Y-%m-%d")
    formatted_departure_string = departure_date.strftime("%Y-%m-%d")
    formatted_graduation_string = graduation_date.strftime("%Y-%m-%d")
    formatted_exercise_string = graduation_date.strftime("%Y-%m-%d")

    print(f"Days since College Graduation ({formatted_graduation_string}): {graduation_departure_date_string}")
    print(f"Days since Dad's Departure    ({formatted_departure_string}): {departure_date_string}\n")

    print(f"Days since New Years Day ({formatted_new_years_string}): {current_year_to_date_string}")
    print(f"Days since Last Birthday ({formatted_birthday_string}): {birthday_difference_string}")
