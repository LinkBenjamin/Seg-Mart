import re

def is_valid_email(email):
    if not email:
        return False
    
    regex = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,6}$'
    if not re.match(regex, email):
        return False
    
    return True