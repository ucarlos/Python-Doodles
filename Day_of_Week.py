# ------------------------------------------------------------------------------
# Created by Ulysses Carlos on 10/24/2020 at 01:21 AM
#
# Day_of_Week.py
# Calculate the name of the day given a date in year/month/day format.
# ------------------------------------------------------------------------------

from math import floor


# def shifted_month(month):
#     """
#     Calculate the shifted month given a month
#     """
#     if (month == 1 or month == 5):
#         return 1
#     elif (month == 2 or month == 6):
#         return 4
#     elif (month == 3 or month == 11):
#         return 3
#     elif (month == 4 or month == 7):
#         return 6
#     elif (month == 8):
#         return 2
#     elif (month == 9 or month == 12):
#         return 5
#     elif (month == 10):
#         return 0
#     else:
#         return -1  # Should never happen

def shifted_month(month):
    if (month == 1 or month == 2):
        return 12 + month
    else:
        return month


def calculate_day(year, month, day):
    """
    Given an day, month, and year, calculate the day of the week.
    """
    year = (year - 1) if (month == 1 or month == 2) else year

    result = (day
              + floor((13 * (shifted_month(month) + 1)) / 5)
              + (year % 100)  # K
              + floor((year % 100) / 4)  # floor(K / 4)
              + floor(floor(year / 100) / 4)  # floor(J / 4)
              - 2 * floor(year / 100)  # 2J
              )

    return result % 7


def day_to_string(result):
    if (result == 0):
        return "Saturday"
    elif (result == 1):
        return "Sunday"
    elif (result == 2):
        return "Monday"
    elif (result == 3):
        return "Tuesday"
    elif (result == 4):
        return "Wednesday"
    elif (result == 5):
        return "Thursday"
    else:
        return "Friday"


def main():
    year = int(input("Please input a year.\n"))
    month = int(input("Please input a month.\n"))
    day = int(input("Please input a day.\n"))

    result = calculate_day(year, month, day)

    print(day_to_string(result))


if __name__ == "__main__":
    main()
