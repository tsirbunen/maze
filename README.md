# THE MAZE
**THE MAZE** is a program that creates mazes, allows you to try to solve them, 
solves the mazes using different algorithms. Optionally you can choose to view the
maze generation and solving processes live in a GUI.

## How to run the program?
* Download the [PyCharm IDE](https://www.jetbrains.com/pycharm/download/#section=mac) if you don't have it already. 
* Download this repository.
* Open this project in PyCharm. 
* Find the file src/main.py in the source file tree.
* Click once with left mouse button so that the file becomes selected.
* Click once with right button to see the context menu (see the image below).
* Select option Run 'main'.
* A console program will start and print out the use instructions.
* Answer the questions asked by the console.
* A GUI will open up. Follow the instructions within the GUI.
* Have fun!

![how_to_run](images/how_to_run.png)

**NOTE:**
If you get the below warning (and the GUI does not open up properly),
switch to using python version 3.10.2 as the interpreter in PyCharm. 
This python version should enable the Turtle graphics (that the graphical UI is based on).
```
DEPRECATION WARNING: The system version of Tk is deprecated and may be removed in a future release. 
Please don't rely on it. Set TK_SILENCE_DEPRECATION=1 to suppress this warning.
```

## Tests
Files containing tests have been placed into the same folder with the code that they test.
To run all tests, open a separate Terminal (macOS) at root level and run
```python3 -m pytest```
To run a single test file, run (change the folder and file names as necessary)
```python3 -m pytest src/maze_parameters/parameters_test.py```
To get test coverage data, run
```coverage run -m pytest``` 
and then print the test coverage data to console with
```
coverage report -m
```
or create an HTML-file with
```
coverage html
```
followed by opening the generated [html file in path htmlcov/index.html](htmlcov/index.html) with your browser.