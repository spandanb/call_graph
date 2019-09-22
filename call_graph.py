import itertools
from ascii_tree import print_tree, transformed_tree
from copy import deepcopy
from functools import wraps
from typing import Generator

'''
1) Determine call graph
2) Print ascii-call graph
NB: Currently copies all function arguments
'''

class FNode:
    '''
    Represents a function call node
    '''
    def __init__(self, func, args, kwargs):
        self.func = func
        self._func_name = func.__name__
        self.args = args
        self.kwargs = kwargs
        self.retval = None
        self.children = []

    def fmt_kwargs(self)->Generator:
        '''
        format kwargs like: car=3, tar=4
        '''
        if not self.kwargs:
           return ()
        return (f'{k}={v}' for k, v in self.kwargs.items())

    def fmt_args(self)->Generator:
        if not self.args:
            return ()
        return (str(a) for a in self.args)

    def __str__(self):
        tokens = [self._func_name, '(']
        args = itertools.chain(self.fmt_args(), self.fmt_kwargs())
        args = ', '.join(args)  # comma separated string
        tokens.extend(args)
        tokens.append(')->')
        tokens.append(str(self.retval))
        return ''.join(tokens)


class CallForest:
    '''
    Represents the entire call forest
    '''
    def __init__(self):
        # unrelated call nodes
        self.roots = []
        # current tree being built
        self.callstack = []

    def call_start(self, call):
        if len(self.callstack) == 0:
            self.roots.append(call)
        else:
            self.callstack[-1].children.append(call)
        self.callstack.append(call)

    def call_end(self):
        self.callstack.pop()

    def __str__(self):
        return ' '.join(root.func.__name__ for root in self.roots)

    def print_tree(self):
        get_val = lambda fnode: fnode.__str__()
        get_children = lambda fnode: fnode.children
        for root in self.roots:
            transformed = transformed_tree(root, get_val, get_children)
            print_tree(transformed)


ctree = CallForest()

def cgraph(func):
    '''
    decorator that constructs call graph. Operates on a global call Tree
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        '''
        A function and its arguments uniquely define a
        node in the call graph. We track when a function is called
        and when the call is complete. A function call, A that begins
        immediately after a previous function call B begins, but before
        B completes must be the child of B.
        '''
        callnode = FNode(func, deepcopy(args), deepcopy(kwargs))
        ctree.call_start(callnode)
        retval = func(*args, **kwargs)
        callnode.retval = retval
        ctree.call_end()
        return retval
    return wrapper


def print_cgraph():
    ctree.print_tree()


@cgraph
def fact(n):
    if n <= 1:
        return 1
    return n*fact(n-1)


@cgraph
def main_func(arg):
    some_other_fun(arg, cat='meow')

@cgraph
def some_other_fun(arg, cat=None, bar=None):
    return 3


if __name__ == '__main__':
    #print(fact(4))
    print(main_func('a'))
    print_call_tree()
