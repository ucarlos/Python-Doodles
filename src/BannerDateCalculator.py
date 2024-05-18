#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Created by Ulysses Carlos on 05/18/2024 at 12:52 PM
#
# BannerDateCalculator.py
#
# ------------------------------------------------------------------------------

from datetime import datetime
from dateutil.relativedelta import relativedelta

if __name__ == "__main__":
    current_date = datetime.today()
    current_birthday = datetime(current_date.year, 2, 15, 22, 5)
    new_years_date = datetime(current_date.year, 1, 1, 0, 0)

    if current_birthday > current_date:
        # Decrement the birthday year
        current_birthday.replace(year=current_date.year - 1)

    # Now, provide the difference for the months:
    relative_birthday_difference: relativedelta = relativedelta(current_date, current_birthday)
    relative_new_years_date_difference: relativedelta = relativedelta(current_date, new_years_date)

    # Now use normal delta
    birthday_difference = current_date - current_birthday
    new_years_date_difference = current_date - new_years_date

    birthday_difference_string = (f"{relative_birthday_difference.months} Months "
                                  f"{str(relative_birthday_difference.days).zfill(2)} "
                                  f"Days {str(relative_birthday_difference.hours).zfill(2)}:"
                                  f"{str(relative_birthday_difference.minutes).zfill(2)}:"
                                  f"{str(relative_birthday_difference.seconds).zfill(2)} "
                                  f"({birthday_difference})")

    current_year_to_date_string = (f"{relative_new_years_date_difference.months} Months "
                                   f"{str(relative_new_years_date_difference.days).zfill(2)} Days "
                                   f"{str(relative_new_years_date_difference.hours).zfill(2)}:"
                                   f"{str(relative_new_years_date_difference.minutes).zfill(2)}:"
                                   f"{str(relative_new_years_date_difference.seconds).zfill(2)} "
                                   f"({new_years_date_difference})")

    formatted_new_years_string = new_years_date.strftime("%Y-%m-%d")
    formatted_birthday_string = current_birthday.strftime("%Y-%m-%d")

    print(f"Time since New Years Day ({formatted_new_years_string}): {current_year_to_date_string}")
    print(f"Time since last Birthday ({formatted_birthday_string}): {birthday_difference_string}")
