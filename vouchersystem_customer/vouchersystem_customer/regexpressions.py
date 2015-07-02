import re;

def check_names(first, last):
    correct_first = re.match('^[a-z]{5,100}$', first, re.I)
    correct_last = re.match("^[a-z']{5,100}$", last, re.I)

    if correct_first and correct_last:
        return True
    else:
        return False
