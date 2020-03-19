import random


# data base of image location
# we can add a or multiple account in it, like this '{'x': 'xxxxxxxxxxx', 'y': 'yyyyyyyy'},'

_VALID_IMAGE = (
    {'x': '144', 'y': '256.25'},
    {'x': '144', 'y': '548.75'},
    {'x': '144', 'y': '841.25'},
    {'x': '144', 'y': '1133.75'},

    {'x': '432', 'y': '256.25'},
    {'x': '432', 'y': '548.25'},
    {'x': '432', 'y': '841.25'},
    {'x': '432', 'y': '1133.75'},
)


class Image:
    def __init__(self):
        self.valid_account = _VALID_IMAGE[random.randint(0, len(_VALID_IMAGE)) - 1]

    def location_x(self):
        return self.valid_account['x']

    def location_y(self):
        return self.valid_account['y']


# global variable
# a instance of image location
# it can be used in any place via 'from App.student.user_center.test_data.image import VALID_IMAGE'
VALID_IMAGE = Image()
VALID_IMAGE.location_x()
VALID_IMAGE.location_y()
