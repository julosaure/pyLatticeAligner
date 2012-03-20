#!/usr/bin/python

from functools import total_ordering

class Sentence(list):

    def __init__(self, text, stemmer):
        self.text = text
        
        self.extend(map(lambda t: Token(t, stemmer.stem(t)), text.split(' ')))

    def __str__(self):
        return str(map(str, self.__iter__()))
        

@total_ordering
class Token:
    
    def __init__(self, text, stem=None):
        self.text = text
        self.stem = stem
        self.comp = self.stem if self.stem is not None else self.text

    def __str__(self):
        return self.text

    def __eq__(self, other):
        assert isinstance(other, Token)
        return self.comp.lower().__eq__(other.comp.lower())

    def __lt__(self, other):
        return self.comp.__lt__(other.comp)

    def __hash__(self):
        return self.comp.__hash__()

class NullToken(Token):

    def __init__(self):
        Token.__init__(self, "X")
