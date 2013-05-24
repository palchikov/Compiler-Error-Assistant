Compiler-Error-Assistant
========================
Helper script for automated search and retrieval information about compilation errors and messages from Stack Overflow and Google.

FEATURES:
---------
* Display colorized  error list
* Issuance of references to Stack Overflow for the specific error
* Open a link directly from the console
* Search error message in Google (if stack overflow results are not sufficient)

FILES:
------
* stwf.py - the main script, parses compiler messages.
* wrapper.sh - helper script to run the main script from wrapper scripts.
* sclang - wrapper script to run the clang
* sclang++ - scriptwrapper to run clang++
* sg++ - wrapper script to run g++
* sgcc - wrapper script to run the gcc

USAGE:
------
`./sg++ -- main.cpp`

Start the g++ compiler on the file main.cpp and redirect stderr output to the stwf.py.

`./sg++ -- -Wall main.cpp`

Start the g++ compiler with options.

`./sg++ -v -- main.cpp`

Option to the main script.

`g++ -Wall main.cpp 2>&1 | ./stwf.py`

Redirect stderr to the main script compiler normally.

stwf.py USAGE:
--------------
`stfw.py [-h] [-v] [-s] [-o OPEN_WITH]`

`-h, --help` show help and quit

`-v, --verbose` show the full output of the compiler

`-s, --system-open` use default browser

`-o OPEN_WITH, --open-with OPEN_WITH` use external programm to open links
