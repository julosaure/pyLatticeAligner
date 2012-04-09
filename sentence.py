#!/usr/bin/python

from functools import total_ordering
from alignment import *

class Sentence(list):

    def __init__(self, text, stemmer, tokenizer, tagger=None):
        self.text = text
        
        tokens = tokenizer.tokenize(self.text)
        if tagger is not None:
            taggedTokens = tagger.tag(tokens)
        else:
            taggedTokens = zip(tokens, ['' for x in tokens])
        stemmedTaggedTokens = map(lambda (tok, tag): Token(tok, stemmer.stem(tok), tag), taggedTokens)
        self.extend(stemmedTaggedTokens)

    def __str__(self):
        return str(map(str, self.__iter__()))
        

    def pp(self):
        return str([tok.pp() for tok in self])

    def __eq__(self, other):
        equals = True
        if not isinstance(other, Sentence) or len(self) != len(other):
            equals = False
        else:
            for tok1, tok2  in zip(self, other):
                if tok1 != tok2:
                    equals = False
                    break
        return equals

            
@total_ordering
class Token:
    
    def __init__(self, text, stem=None, tag=None):
        self.text = text
        self.stem = stem
        self.comp = self.stem if self.stem is not None else self.text
        self.tag = tag

    def __str__(self):
        return self.text.encode("utf8")

    def pp(self):
        return str((str(self), self.tag))

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
