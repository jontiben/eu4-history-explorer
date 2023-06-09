import re


def get_data(line: str) -> str:
    return line.split('=')[-1].replace("\"", '')


def get_tag(line: str) -> str:
    return line.split('=')[0].replace('	', '')


def define_bracket_block(file_lines: list, start_point: int) -> list:
    # Returns a list of lines between the first bracket and the last bracket
    bracket_count = 0
    for check_bracket_num in range(start_point, len(file_lines)):
        if '{' in file_lines[check_bracket_num]:
            bracket_count += 1
        if '}' in file_lines[check_bracket_num]:
            bracket_count -= 1
        if bracket_count == 0 and check_bracket_num > start_point:
            return file_lines[start_point + 1:check_bracket_num]
    return []  # Error, no end


def is_date(line: str) -> bool:
    line = line.split('=')[0].replace('	', '')+'='
    # Determines if the tag in a given line is a properly-formatted date
    if re.fullmatch(r"\d{1,4}.\d\d?.\d\d?=", line) is not None:
        return True
    return False



def is_province_id(line: str) -> bool:
    # Determines if the data in a given line is a properly-formatted province ID
    line = get_tag(line)
    if re.fullmatch(r"-\d{1,4}", line) is not None:
        return True
    return False



def is_tag(line: str) -> bool:
    # Determines if the data in a given line is a properly-formatted tag
    line = get_tag(line)
    if re.fullmatch(r"[A-Z][A-Z0-9]{2}", line) is not None:
        return True
    return False



def is_created_nation(tag: str) -> bool:
    # Returns True if the tag is dynamically generated (client state (K), colonial nation (C),
    # trade city (T), federation (F), or custom nation (D)). False if it is anything else.
    if re.fullmatch(r"([CDFKT])\d\d", tag) is not None:
        return True
    return False


def parse_interval(argument: str) -> int | None:
    if argument == "w" or argument == "week":
        return 7
    elif argument == "m" or argument == "month":
        return 30 # Should make this better honestly, not all months are 30 days
    elif argument == "y" or argument == "year":
        return 365

    if re.search(r"w$", argument) is not None or re.search(r"week$", argument) is not None:
        return int(argument.replace("week", "").replace("w", "")) * 7
    elif re.search(r"m$", argument) is not None or re.search(r"month$", argument) is not None:
        return int(argument.replace("month", "").replace("m", "")) * 30 # Same here
    elif re.search(r"y$", argument) is not None or re.search(r"year$", argument) is not None:
        return int(argument.replace("year", "").replace("y", "")) * 365
    else:
        number_string = ""
        for char in argument:
            try:
                temp_int = int(char)
                number_string += char
            except:
                break
        return int(number_string) # Days

