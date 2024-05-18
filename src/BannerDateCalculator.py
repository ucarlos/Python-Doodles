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

if __name__ == "__main__":
    current_date = datetime.today()
    current_birthday = datetime(current_date.year, 2, 15, 22, 5)
    new_years_date = datetime(current_date.year, 1, 1, 0, 0)
    departure_date = datetime(2022, 11, 1, 1)

    if current_birthday > current_date:
        # Decrement the birthday year
        current_birthday.replace(year=current_date.year - 1)

    # Now, provide the difference for the months:
    relative_birthday_difference: relativedelta = relativedelta(current_date, current_birthday)
    relative_new_years_date_difference: relativedelta = relativedelta(current_date, new_years_date)
    relative_departure_date_difference: relativedelta = relativedelta(current_date, departure_date)

    # Now use normal delta
    birthday_difference = current_date - current_birthday
    new_years_date_difference = current_date - new_years_date
    departure_date_difference = current_date - relative_birthday_difference

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

    formatted_new_years_string = new_years_date.strftime("%Y-%m-%d")
    formatted_birthday_string = current_birthday.strftime("%Y-%m-%d")
    formatted_departure_string = departure_date.strftime("%Y-%m-%d")

    print(f"Days since the departure ({formatted_departure_string}): {departure_date_string}\n")

    print(f"Days since New Years Day ({formatted_new_years_string}): {current_year_to_date_string}")
    print(f"Days since last Birthday ({formatted_birthday_string}): {birthday_difference_string}")
