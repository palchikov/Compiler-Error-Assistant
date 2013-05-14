Compiler-Error-Assistant
========================
Скрипт-помощник разработчика, автоматизирующий поиск информации об ошибках компиляции на Stack Overflow и в Google.

FEATURES:
---------
* Представление списка ошибок
* Выдача ссылок на Stack Overflow по конкретной ошибке
* Открытие ссылки прямо из консоли
* Ссылка с поисковым запросом в Google (если не устраивают ссылки на Stack Overflow, или там ничего не найдено)

FILES:
------
* stwf.py - основной скрипт, принмающий stderr компилятора.
* wrapper.sh - вспомогательный скрипт для запуска основного скрипта из скриптов-оберток.
* clang - скрипт-обертка для запуска clang
* clang++ - скрипт-обертка для запуска clang++
* sg++ - скрипт-обертка для запуска g++
* sgcc - скрипт-обертка для запуска gcc

USAGE:
------
`./sg++ -- main.cpp`

Запустить компилятор g++ на файле main.cpp и перенаправить вывод stderr в stwf.py.

`./sg++ -- -Wall main.cpp`

Запустить компилятор g++ с указанными опциями.

`./sg++ -v -- main.cpp`

Передать опции основному скрипту.

`g++ -Wall main.cpp 2>&1 | ./stwf.py`

Перенаправить stderr компилятора в основной скрипт обычным образом.

stwf.py USAGE:
--------------
`stfw.py [-h] [-v] [-s] [-o OPEN_WITH]`

`-h, --help` show this help message and exit

`-v, --verbose` show verbose output

`-s, --system-open` use system URL open command

`-o OPEN_WITH, --open-with OPEN_WITH` use custom URL open command
