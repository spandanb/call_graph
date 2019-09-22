from call_graph import cgraph, print_cgraph

@cgraph
def fact(n):
    if n <= 1:
        return 1
    return n*fact(n-1)


fact(4)
print_cgraph()
