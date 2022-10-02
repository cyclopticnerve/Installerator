#!/usr/bin/env python3

# list in a not b: OK
# list in a and b
#   item in a not b: OK

# dict in a not b: OK
# dict in a and b
#   kv in a not b:
#       recurse

import json

dict_a = {
    "general": {
        "prog_name": ""
    }
}

dict_b = {
    "general": {
        "prog_name": "spaceoddity"
    }
}


def merge(dict_src, dict_dst, path=None):

    if path is None:
        path = ''

    if type(dict_src) == type(dict_dst):
        if isinstance(dict_src, dict):

            for key in dict_src.keys():

                if key not in dict_dst.keys():
                    dict_dst[key] = dict_src[key]
                else:
                    path += '/' + key
                    merge(dict_src[key], dict_dst[key], path)

        elif isinstance(dict_src, list):

            for item in dict_src:

                if item not in dict_dst:
                    dict_dst.append(item)

    else:
        raise Exception(f'Type mismatch: {path}')


if __name__ == '__main__':
    try:
        merge(dict_a, dict_b)
        string = json.dumps(dict_b)
        dict_c = json.loads(string)
        print(json.dumps(dict_c, indent=4))
    except Exception as error:
        print(error)
