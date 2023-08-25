# Logic IC Tester
![IC Tester](doc/ictester.jpg)

Main goal of this project was to make a logic IC tester that allows adding new tests and support for new ICs easily.

## Features

* fully programmable (client-side, in python)
* designed for 5V TTL logic, but other 5V logic families can be tested too
* 2.2us (<=16-pin ICs) and ?.?us (>16-pin ICs) per single test cycle
* built-in tests for 4164 and 41256 memories (MARCH C- test in read+write, read/write and page access modes)
* built-in tests for 74121, 74122 and 74123 univibrators
* small and USB powered

## Components

Project is split into three parts:

* [hardware](hw) - KiCad project files (see also [this pdf](doc/ictester.pdf) for schematic)
* [firmware](fw) - IC tester firmware
* [tool](tool) - software that controls the tester

