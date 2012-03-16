#!/usr/bin/python

from functools import total_ordering

class Sentence(list):

    def __init__(self, text):
        self.text = text
        self.extend(map(lambda t: Token(t), text.split(' ')))

    def __str__(self):
        return str(map(str, self.__iter__()))
        

@total_ordering
class Token:
    
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    def __eq__(self, other):
        assert isinstance(other, Token)
        return self.text.lower().__eq__(other.text.lower())

    def __lt__(self, other):
        return self.text.__lt__(other.text)
