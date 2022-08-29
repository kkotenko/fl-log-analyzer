# fl-log-analyzer
Processes a recording of interactions with the API of the browser game [Fallen London](https://www.fallenlondon.com/).
Such a recording can be created with e.g. the browser extension [FL Request Sounder](https://github.com/lensvol/fl-request-sounder).

## Installation
You need to install [Python 3](https://www.python.org/downloads/) to run this file. 

After you have installed Python, open a terminal, navigate to the folder where this file is located, and execute the file with Python, specifying 

* a quality the changes of which you wish to analyze
* the path to the log file 

The most comprehensive help is provided in the script help:

```
./analyze.py -h
```

Sample usage:
```
$ ./analyze.py "Airs of Passengers" ~/Downloads/fallen-london-helicon-house-20220822111623.log
Airs of Passengers changed from UNKNOWN to 4102
Associated text:
A volunteer from the crowd
```
*[part of output omitted]*
```
<p>In the crowd, a Tracklayer with a book of psalms applauds; a Rubbery man gurgles enthusiastically at this alternative way of modifying the person.</p>
<p>You offer to restore him at once. But the young man is in no hurry; and when you do return him to his ordinary size, he takes a new interest in clockwork, and paves his drawing room in moonpearls.</p>
-------
Airs of Passengers changed from 4102 to 4103
Associated text:
[title unchanged]
[description unchanged]
-------
```
