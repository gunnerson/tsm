def has_group(user, group_name):
    # Check if the user belongs to a certain group
    return user.groups.filter(name=group_name).exists()


def not_empty(param):
    return param != '' and param is not None
