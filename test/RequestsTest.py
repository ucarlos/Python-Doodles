#!/usr/bin/env python3
# -------------------------------------------------------------------------------
# Created by Ulysses Carlos on 01/16/2024 at 05:05 PM
#
# RequestsTest.py
#
# -------------------------------------------------------------------------------
from src import IPGeolocator

if __name__ == "__main__":
    print(IPGeolocator.find_ip_geography_info("36.255.159.130"))
