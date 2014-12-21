from os import path
import json

# We'll need this to check if something is a string later.
# This isn't great, but it's better than a dependency on six.
try:
    basestring
except NameError:
    basestring = str

class Wordfilter(object):

    """filter out bad words"""

    blacklist = []

    def __init__(self, blacklist=None, datafile=None):
        if isinstance(blacklist, list):
            self.blacklist = blacklist
            return

        if datafile:
            with open(datafile, 'r') as f:
                self.blacklist = f.read().splitlines()

        else:
            datafile = path.join(path.dirname(__file__), 'badwords.json')
            self.blacklist = json.load(open(datafile, 'r'))

    def blacklisted(self, string):
        string = string.lower().strip()
        self.blacklist = list(map(lambda s: s.lower(), self.blacklist))
        return any(word in string for word in self.blacklist)

    def add_words(self, lis):
        if isinstance(lis, basestring):
            lis = [lis]
        self.blacklist.extend(lis)

    def clear_list(self):
        self.blacklist = []

# instantiates instance so functions are available directly from module
_module_instance = Wordfilter()
blacklisted = _module_instance.blacklisted
add_words = _module_instance.add_words
clear_list = _module_instance.clear_list
