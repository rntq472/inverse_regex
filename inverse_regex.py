

import regex
from itertools import groupby
from functools import singledispatch


@singledispatch
def inverse_regex(x, **args):
    raise TypeError('Type not supported')

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

@inverse_regex.register(tuple)
def _(x, **args):
    return(tuple(inverse_regex(list(x), **args)))

## If the user doesn't have numpy installed they don't need methods for those types.
try:
    import numpy as np
    
    @inverse_regex.register(np.bool_)
    def _(x, **args):
        return(x)
    
    @inverse_regex.register(np.int_)
    @inverse_regex.register(np.intc)
    @inverse_regex.register(np.intp)
    @inverse_regex.register(np.int8)
    @inverse_regex.register(np.int16)
    @inverse_regex.register(np.int32)
    @inverse_regex.register(np.int64)
    @inverse_regex.register(np.uint8)
    @inverse_regex.register(np.uint16)
    @inverse_regex.register(np.uint32)
    @inverse_regex.register(np.uint64)
    @inverse_regex.register(np.float_)
    @inverse_regex.register(np.float16)
    @inverse_regex.register(np.float32)
    @inverse_regex.register(np.float64)
    def _(x, **args):
        return(inverse_regex(str(x), **args))
    
    @inverse_regex.register(np.ndarray)
    def _(x, **args):
        if x.ndim <= 2:
            return(np.array([inverse_regex(y, **args) for y in x]))
        else:
            raise AttributeError('No more than two dimensions accepted')
except:
    pass

## If the user doesn't have pandas installed they don't need methods for those types.
try:
    import pandas as pd
    
    @inverse_regex.register(pd.Series)
    def _(x, **args):
        return(pd.Series([inverse_regex(y, **args) for y in x], index = x.index))
    
    @inverse_regex.register(pd.DataFrame)
    def _(x, **args):
        out = pd.DataFrame(x.apply(inverse_regex, axis = 1, **args))
        out.columns = x.columns
        return(out)
except:
    pass

@inverse_regex.register(list)
def _(x, **args):
    return([inverse_regex(y, **args) for y in x])

@inverse_regex.register(str)
def _(x,
      numbers_to_keep = (2, 3, 4, 5, 10),
      combine_cases = False,
      combine_alphanumeric = False,
      combine_punctuation = False,
      combine_space = False,
      sep = '',
      escape = False,
      enclose = False):
    
    if numbers_to_keep is None:
        numbers_to_keep = ()
    
    if isinstance(numbers_to_keep, (int)):
        numbers_to_keep = (numbers_to_keep,)
    
    out = list(x)
    
    lower = regex.compile('[[:lower:]]')
    upper = regex.compile('[[:upper:]]')
    alpha = regex.compile('[[:alpha:]]')
    digit = regex.compile('[[:digit:]]')
    alnum = regex.compile('[[:alnum:]]')
    punct = regex.compile('[[:punct:]]')
    space = regex.compile('[[:space:]]')
    
    if combine_alphanumeric:
        iterator = alnum.finditer(x)
        for match in iterator:
            out[match.span()[0]] = r"[[:alnum:]]"
    else:
        if combine_cases:
            iterator = alpha.finditer(x)
            for match in iterator:
                out[match.span()[0]] = r"[[:alpha:]]"
            
            iterator = digit.finditer(x)
            for match in iterator:
                out[match.span()[0]] = r"[[:digit:]]"
        else:
            iterator = upper.finditer(x)
            for match in iterator:
                out[match.span()[0]] = r"[[:upper:]]"
            
            iterator = lower.finditer(x)
            for match in iterator:
                out[match.span()[0]] = r"[[:lower:]]"
                
            iterator = digit.finditer(x)
            for match in iterator:
                out[match.span()[0]] = r"[[:digit:]]"
    
    iterator = space.finditer(x)
    for match in iterator:
        if combine_space:
            out[match.span()[0]] = r"[[:space:]]"
    
    iterator = punct.finditer(x)
    for match in iterator:
        if combine_punctuation:
            out[match.span()[0]] = r"[[:punct:]]"
    
    ## https://stackoverflow.com/questions/43424729/how-to-find-run-length-encoding-in-python
    rle = [[k, sum(1 for i in g)] for k,g in groupby(out)]
    
    for ii, rr in enumerate(rle):
        if rr[1] in numbers_to_keep:
            rle[ii][1] = "{" + str(rr[1]) + "}"
        elif rr[1] == 1:
            rle[ii][1] = ""
        else:
            rle[ii][1] = "+"
    
    joined = sep.join([i + j for i,j in rle])
    
    if escape:
        joined = regex.escape(joined)
    
    if enclose:
        joined = '^' + joined + '$'
    
    return(joined)
