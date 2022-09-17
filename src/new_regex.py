import re
# sad

def list_tostring(s):
    # initialize an empty string
    str1 = " "
    # return string
    return (str1.join(s))



list = ['""Hello""', '"Shouji Moroto"', "(Flipper's gituar)",
        "\"'('sa')\"", "lamp", "Flipper's Guitar",
        "Shouji Morots", "Los Planetas", "Shoujo de Pokemo",
        "['Hea']", "[\"sad\"]", "([\'noah'\]", "([asa])",
        "\"'yeah'\"", "\"Jogn\"", "Rui's Roeas", "['Phantom']",
        "['Escape-Arrest']"]

primary_filter = "^[\w]+[\w\s\']+$"
second_filter = "[^\w]+"

for result in list:
    print(f"Checking {result}")
    check = re.search(primary_filter, result)
    if check:
        # Everything went well
        print(f"{result} is OK\n")
    else:
        second_check = re.search(second_filter, result)
        if second_check:
            remove_str = second_check.group()
            print(f"Need to remove {remove_str}")
            find_begin = result.find(remove_str)
            find_end = result.rfind(remove_str[::-1])

            print(f"find_begin: {find_begin}")
            print(f"find_end: {find_end}")
            if find_begin == -1 and find_end == -1:
                print(f"Warning: Couldn't filtre {result}!")
                continue
            elif find_begin == find_end:  # Remove it once
                result = result[find_begin + len(remove_str):]
            elif find_begin != -1 and find_end == -1:
                # If the reverse string is not a mirror of remove_str
                # Just remove it: (ex. '[ is reverse of [' )
                result = result[find_begin + len(remove_str):
                                -len(remove_str)]
            else:
                result = result[find_begin + len(remove_str): find_end]
            print(f"Changed to {result}\n")
        else:
            print(f"Warning: {result} failed second check!"
                  "Something is wrong!")
            continue           
