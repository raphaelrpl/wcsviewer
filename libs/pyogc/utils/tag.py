def remove_attrs_in_dict(obj, bad_value='@', limit=None):
    if isinstance(obj, dict):
        for key in obj.keys():
            if isinstance(key, basestring) and key.startswith(bad_value):
                del obj[key]
            else:
                return remove_attrs_in_dict(obj[key], bad_value)
    return