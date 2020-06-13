import os
import uuid
import random
import math
import re

from django.utils.html import strip_tags


"""
Basic utility module that includes helper functions listed below in order:
    - get_file_ext(file_path)
    - upload_path(instance, filename)
    - count_words(html_string)
    - read_time(html_string)
"""


def get_file_ext(file_path):
    """
    Return the name and extension of a file as a tuple
    :param file_path:
    :return:
    """
    file_base = os.path.basename(file_path)
    name, ext = os.path.splitext(file_base)
    return name, ext


def upload_path(instance, filename):
    """
    Returns upload file path (randomized)
    :param instance:
    :param filename:
    :return:
    """
    name, ext = get_file_ext(filename)
    new_filename = random.randint(1, 9999999999)
    final_filename = f"{new_filename}-{name}.{ext}"
    return f"uploads/{uuid.uuid4().hex}{final_filename}"


def count_words(html_string):
    """
    Return an integer indicating the number of words in a blog post
    :param html_string:
    :return:
    """
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words)
    return count


def read_time(html_string):
    """
    Return an integer indicating the duration(time) in minutes a blog
    post will be read.
    Assumption made is that 200wpm reading
    :param html_string:
    :return:
    """
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.0)
    return read_time_min
