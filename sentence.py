#!/usr/bin/python

from functools import total_ordering
from alignment import *

class Sentence(list):

    def __init__(self, text, stemmer, tokenizer):
        self.text = text
        
        tokens = tokenizer.tokenize(self.text)
        stemmedTokens = map(lambda t: Token(t, stemmer.stem(t)), tokens)
        self.extend(stemmedTokens)

    def __str__(self):
        return str(map(str, self.__iter__()))
        

@total_ordering
class Token:
    
    def __init__(self, text, stem=None):
        self.text = text
        self.stem = stem
        self.comp = self.stem if self.stem is not None else self.text

    def __str__(self):
        return self.text.encode("utf8")

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.comp.lower().__eq__(other.comp.lower())
        elif isinstance(other, AlignCell):
            return -other.__eq__(self)
        else:
            raise Exception("Invalid type, type(other)="+str(type(other)))

    def __lt__(self, other):
        return self.comp.__lt__(other.comp)

    def __hash__(self):
        return self.comp.__hash__()

class NullToken(Token):

    def __init__(self):
        Token.__init__(self, "X")
