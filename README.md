Call Graph
==========
Generate a call_graph using a decorate to decorate
functions you want included in the call graph.

Installation
============
`git clone ...`

`cd ...`

`python3 setup.py install`

Usage
=====
This exposes two objects, the `cgraph` decorator
and `print_cgraph` to print the actual call_graph. Consider

```
>>> from call_graph import cgraph, print_cgraph
>>> @cgraph
... def facto(n):
...   if n == 0: return 1
...   return n*facto(n-1)
...

>>> print_cgraph()
page: 0
------------------
|                |
| facto(5)->120  |
|                |
------------------
        |
        |
        |
        |
        |
-----------------
|               |
| facto(4)->24  |
|               |
-----------------
       |
       |
       |
       |
       |
----------------
|              |
| facto(3)->6  |
|              |
----------------
       |
       |
       |
       |
       |
----------------
|              |
| facto(2)->2  |
|              |
----------------
       |
       |
       |
       |
       |
----------------
|              |
| facto(1)->1  |
|              |
----------------
       |
       |
       |
       |
       |
----------------
|              |
| facto(0)->1  |
|              |
----------------
```

Notes
=====
Uses [ascii_tree](https://github.com/spandanb/ascii_tree) to generate and print
call graph as a tree.
