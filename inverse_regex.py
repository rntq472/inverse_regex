

import regex
from itertools import groupby
from functools import singledispatch


@singledispatch
def inverse_regex(x, **args):
    raise TypeError()

@inverse_regex.register(bool)
def _(x, **args):
    return(x)

@inverse_regex.register(int)
def _(x, **args):
    return(inverse_regex(str(x), **args))

@inverse_regex.register(float)
def _(x, **args):
    return(inverse_regex(str(x), **args))

@inverse_regex.register(complex)
def _(x, **args):
    return(inverse_regex(str(x), **args))

@inverse_regex.register(str)
def _(x, **args):
    return(inverse_regex([x], **args)[0])

@inverse_regex.register(tuple)
def _(x, **args):
    return(tuple(inverse_regex(list(x), **args)))

try:
    import pandas as pd
    @inverse_regex.register(pd.DataFrame)
    def _(x, **args):
        pass ## TODO
except ImportError as err:
    print('Cannot process input:', err)

try:
    import numpy as np
    @inverse_regex.register(np.ndarray)
    def _(x, **args):
        pass ## TODO
except ImportError as err:
    print('Cannot process input:', err)

@inverse_regex.register(list)
def _(x,
      numbers_to_keep = (2, 3, 4, 5, 10),
      combine_cases = False,
      combine_alphanumeric = False,
      combine_punctuation = False,
      combine_space = False,
      sep = '',
      escape_punctuation = False,
      enclose = False):
    
    if isinstance(numbers_to_keep, (int)):
        numbers_to_keep = (numbers_to_keep,)
    
    out = ['']*len(x)
    
    lower = regex.compile('[[:lower:]]')
    upper = regex.compile('[[:upper:]]')
    alpha = regex.compile('[[:alpha:]]')
    digit = regex.compile('[[:digit:]]')
    alnum = regex.compile('[[:alnum:]]')
    punct = regex.compile('[[:punct:]]')
    space = regex.compile('[[:space:]]')
    
    for index, item in enumerate(x):
        
        if item is None:
            continue
        
        if not combine_punctuation and escape_punctuation:
            pass ## TODO
        
        if isinstance(item, (int, float, complex)):
            item = str(item)
        
        out[index] = list(item)
        
        if combine_alphanumeric:
            iterator = alnum.finditer(item)
            for match in iterator:
                out[index][match.span()[0]] = r"[[:alnum:]]"
        else:
            if combine_cases:
                iterator = alpha.finditer(item)
                for match in iterator:
                    out[index][match.span()[0]] = r"[[:alpha:]]"
                
                iterator = digit.finditer(item)
                for match in iterator:
                    out[index][match.span()[0]] = r"[[:digit:]]"
            else:
                iterator = upper.finditer(item)
                for match in iterator:
                    out[index][match.span()[0]] = r"[[:upper:]]"
                
                iterator = lower.finditer(item)
                for match in iterator:
                    out[index][match.span()[0]] = r"[[:lower:]]"
                
                iterator = digit.finditer(item)
                for match in iterator:
                    out[index][match.span()[0]] = r"[[:digit:]]"
        
        if combine_space:
            iterator = space.finditer(item)
            for match in iterator:
                out[index][match.span()[0]] = r"[[:space:]]"
        
        if combine_punctuation:
            iterator = punct.finditer(item)
            for match in iterator:
                out[index][match.span()[0]] = r"[[:punct:]]"
        
        ## https://stackoverflow.com/questions/43424729/how-to-find-run-length-encoding-in-python
        rle = [[k, sum(1 for i in g)] for k,g in groupby(out[index])]
        
        for ii, rr in enumerate(rle):
            if rr[1] in numbers_to_keep:
                rle[ii][1] = "{" + str(rr[1]) + "}"
            elif rr[1] == 1:
                rle[ii][1] = ""
            else:
                rle[ii][1] = "+"
        
        out[index] = sep.join([i + j for i,j in rle])
    
    return(out)
