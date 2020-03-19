#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI


class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def my_error(self, val):
        try:
            raise MyError(val)
        except MyError as e:
            raise e
