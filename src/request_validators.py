def signup_validator(user_json):
    
    if len(user_json) is not 3:
        return False 
    if ('username' not in user_json) or ('password' not in user_json) or ('email' not in user_json):
        return False

    return True

def login_validator(user_json):

    if len(user_json) is not 2:
        return False 
    if ('username' not in user_json) or ('password' not in user_json):
        return False

    return True

def add_link_validator(link_json):

    if len(link_json) is not 3:
        return False 
    if ('title' not in link_json) or ('url' not in link_json) or ('description' not in link_json):
        return False

    return True


def delete_link_validator(link_json):

    if len(link_json) is not 1:
        return False 
    if ('title' not in link_json):
        return False

    return True


