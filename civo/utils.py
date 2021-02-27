"""
File to handle all utils
"""
from __future__ import print_function
import sys


def print_err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def filter_list(data: dict, filter_by: str) -> list:
    """
    Function to handle filter in all list of the api
    :param data: object json
    :param filter_by: the filter in this format (label:Home, id:6224cd2b-d416-4e92-bdbb-db60521c8eb9)
    :return: the found object in json format
    """
    filter_split = filter_by.split(':')
    search_in = filter_split[0]
    search = filter_split[1]

    try:
        search = int(search)
    except ValueError:
        pass

    try:
        data_search = data['items']
    except TypeError:
        data_search = data

    return [element for element in data_search if element[search_in] == search]
