from call_graph import cgraph, print_cgraph

@cgraph
def main_func(arg):
    some_other_fun(arg, cat='meow')


@cgraph
def some_other_fun(arg, cat=None, bar=None):
    return 3


main_func('a')
print_cgraph()
