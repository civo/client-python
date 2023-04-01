"""
File to handle all utils
"""
from __future__ import print_function
import sys


def print_err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def filter_list(data: dict, filter_by: str) -> list:
    """
    Filter a list of items by a key:value pair also the search value can be a partial match
    :param data: The data to filter
    :param filter_by: The key:value pair to filter by
    :return: The filtered list
    """

    return_list = []

    try:
        filter_split = filter_by.split(':')
        search_in = filter_split[0]
        search = filter_split[1]
    except IndexError:
        raise ValueError('Invalid filter format')

    try:
        search = int(search)
    except ValueError:
        pass

    try:
        data_search = data['items']
    except TypeError:
        data_search = data

    try:
        for element in data_search:
            # we check if the search value is a partial match or not, check if search is a string or int
            try:
                if search in element[search_in]:
                    return_list.append(element)
            except TypeError:
                if search == element[search_in]:
                    return_list.append(element)
        return return_list
    except KeyError:
        raise KeyError('Invalid filter')