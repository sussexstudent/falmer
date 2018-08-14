import re

camel_case_pattern = re.compile(r'([A-Z])')
under_score_pattern = re.compile(r'_([a-z])')


def camel_to_underscore(name):
    """
    Convert a name from camel case convention to underscore lower case convention.
    Args:
        name (str): name in camel case convention.
    Returns:
        name in underscore lowercase convention.
    """
    return camel_case_pattern.sub(lambda x: '_' + x.group(1).lower(), name)


def underscore_to_camel(name):
    """
    Convert a name from underscore lower case convention to camel case convention.
    Args:
        name (str): name in underscore lowercase convention.
    Returns:
        Name in camel case convention.
    """
    return under_score_pattern.sub(lambda x: x.group(1).upper(), name)


def change_dict_naming_convention(d, convert_function):
    """
    Convert a nested dictionary from one convention to another.
    Args:
        d (dict): dictionary (nested or not) to be converted.
        convert_function (func): function that takes the string in one convention and returns it in the other one.
    Returns:
        Dictionary with the new keys.
    """
    if isinstance(d, dict):
        new = {}
        for k, v in d.items():
            new_v = v
            if isinstance(v, dict):
                new_v = change_dict_naming_convention(v, convert_function)
            elif isinstance(v, list):
                new_v = list()
                for x in v:
                    new_v.append(change_dict_naming_convention(x, convert_function))
            new[convert_function(k)] = new_v
        return new
    elif isinstance(d, list):
        return [change_dict_naming_convention(item, convert_function) for item in d]

    return d
