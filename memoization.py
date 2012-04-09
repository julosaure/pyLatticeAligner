#!/usr/bin/python

from functools import wraps
import cPickle

def memo(func):
    """ Memoize the wrapped function.
    
    The result  of each call of func is stored in memo.
    Subsequent calls with the same parameters make only a dictionary lookup.

    The string representation of the params of func is essential, 
    especially if params are mutables, such as list.
    Here we use it for Sentence and Alignment datastructures
    for which we have a string representation.

    If we cannot easily have such representation, using cPickle.dump 
    can rather be used, but it's slow.
    """
    memo = {}
    @wraps(func)
    def wrapper(*args, **kwds):
        # computes a hash with cPickle
        # works but very slow
        #keystr = cPickle.dumps(args, 1) + cPickle.dumps(kwds, 1)

        keystr = str(map(str, args)) + str(map(str, kwds))

        # check if the function was previously computed with these args
        if not memo.has_key(keystr):
            memo[keystr] = func(*args, **kwds)
                    
        return memo[keystr]
    return wrapper
            
