# CS111-projects
Compilation of my CS111 projects at BYU


# Grade Calculator - Project 0
Overview
I built this Grade Calculator for CS 111 to figure out my current grade based on all my assignment scores and the course’s grading policy. It’s a simple Python program that was a great way to get comfortable with basic syntax, file handling, and some logic for crunching numbers. The tool reads a grade data file, processes scores for different assignment types, handles dropped grades, and spits out my overall percentage and letter grade based on the syllabus.
The program asks for a grade data file, does all the math, and shows a neat breakdown of my scores by category, plus the final grade. It even works if I’m missing some grades by tweaking the weights, so I’ve been using it to keep track of my progress all semester.
Features

Custom File Input: I made it prompt for the grade data file name, so I can use different files without changing the code. Super handy for testing or using new data.
Smart File Parsing: It reads a comma-separated file with grades, skipping comments (lines with #) and blank lines like a pro.
Category Score Breakdown:
Handles all the assignment types: Labs, Homework, Projects, Midterms, Final, and FreeCoding.
Sums up points earned and possible for each category, dropping the two lowest Lab scores and one lowest Homework score as per the rules.
Shows percentages for each category, rounded to one decimal place.


Flexible Grade Weighting:
Uses the syllabus weights (Labs: 10%, Homework: 15%, Projects: 25%, Midterms: 15% each, Final: 20%) to calculate my grade.
If I’m missing grades for some categories, it adjusts the final score by scaling based on the total weight of what’s available.


Clean Output:
Prints a tidy summary of each category with points (earned/possible) and percentage.
Shows the final grade like this: The overall grade in the class is: <letter> (<percentage>%)., with the percentage to two decimal places.
Only shows categories I have scores for, in the right order (Labs, Homework, Projects, Midterm 1, Midterm 2, Final).


Letter Grade Magic: Converts my final percentage to a letter grade based on the syllabus.
Test-Ready: I got it working with the provided test_grade_calculator.py pytest script to make sure everything checks out.
Clean Code: I refactored it a few times to keep things readable and organized, cutting out redundant code and making it easier to follow.

This was a fun first project, and now I’ve got a tool I can actually use to stay on top of my CS 111 grade!



# Image Processor - Project 1
Overview
I created this Image Processor for CS 111 to manipulate images in all sorts of cool ways using command-line arguments. It was a fun challenge that let me dive into Python’s command-line handling, external libraries, and array-based data processing. I built it from scratch, pulling in functions from Lab 8 and Homework 2, and added a bunch of new features to make it a versatile tool for touching up photos. The program takes commands to apply filters, add borders, flip or mirror images, create collages, or even do green screen composites, saving the results as new images.
It’s designed to validate user inputs upfront, process the requested operation, and handle errors gracefully. I got to practice breaking down complex tasks, reusing code, and keeping things clean with refactoring. This project was a great way to level up my Python skills while making something I could actually use to mess around with images!
Features

Command-Line Interface: I set it up to take all inputs as command-line arguments, like -d <image> or -k <input> <output> <percent>, making it easy to run different operations without changing the code.
Input Validation: Checks all command-line arguments before doing anything. If something’s off, it prints an error message instead of crashing.
Image Display: Lets me display an image using the system’s default viewer with the -d <image> command.
Filter Effects:
Grayscale (-g <input> <output>): Converts an image to grayscale using my Lab 8 function.
Sepia (-s <input> <output>): Applies a sepia tone for that vintage vibe, also from Lab 8.
Darken (-k <input> <output> <percent>): Darkens an image by a user-specified factor (0 to 1), reused from Lab 8.


Image Manipulations:
Borders (-b <input> <output> <thickness> <red> <green> <blue>): Adds colored borders of a specified thickness, using my Homework 2 function.
Vertical Flip (-f <input> <output>): Flips an image top-to-bottom, straight from Homework 2.
Horizontal Mirror (-m <input> <output>): Mirrors an image left-to-right. I wrote this one from scratch, tweaking my flip logic to work on the horizontal axis.


Collage Creation (-c <image1> <image2> <image3> <image4> <output> <border_thickness>): Combines four same-sized images into a 2x2 grid with black borders. I coded this to arrange images (1, 2 on top; 3, 4 on bottom) with user-defined border widths.
Green Screen Compositing (-y <foreground> <background> <output> <threshold> <factor>): Overlays a foreground image onto a background by removing “green enough” pixels based on a threshold and factor. I used the detect_green() function from class and wrote logic to copy non-green pixels.
Output Handling: Saves all processed images as .png files to ensure compatibility with the autograder.
Code Reusability: I refactored repetitive tasks (like loading images) into functions like load_image() to keep the code DRY and easy to maintain.
Testing Support: Works with the provided test_project1.py pytest suite to verify each operation. I made sure it handles both the test images and any generic images without hardcoding.
Error Handling: Gracefully handles invalid commands and ensures output files are correctly formatted.

This project was a blast to build, and now I’ve got a handy tool for playing with images while sharpening my coding chops!



# Falling Sand Simulation - Project 2
Overview
I built this Falling Sand Simulation for CS 111, and it’s been an awesome dive into Object-Oriented Programming and real-time application development. The project uses Python and Pygame to create a dynamic simulation where particles like sand, rocks, and bubbles interact on a grid, each following their own physics rules. I extended my work from Homework 4, reusing my Grid, Particle, and Sand classes, and added new Rock and Bubble classes to bring more variety to the simulation. The result is a cool, interactive visualization where I can add particles, watch them move, and see how they behave in real time.
The simulation handles particle updates carefully to avoid glitches, like ensuring bubbles move before sand to prevent unnatural gaps. I learned a ton about inheritance, managing complex object interactions, and keeping performance smooth. It’s been fun to play with, and I’ve even tinkered with some extra features to make the bubbles more whimsical!
Features

Object-Oriented Design:
Built using a class hierarchy with a base Particle class and derived Sand, Rock, and Bubble classes, all leveraging inheritance for shared behavior.
Organized particle logic in Grid_Objects.py for clean, modular code.


Particle Types:
Sand: Falls straight down, checking for clear spaces below or diagonally, reused from Homework 4.
Rock: Stays fixed in place with a physics() method that returns None, ensuring compatibility with the Particle class.
Bubble: Rises upward, checking for clear spaces above or diagonally, with logic mirroring Sand but inverted for upward movement.


Grid Management:
Uses a Grid class (from Homework 4) to store and manage particle positions.
Maintains an all_grid_objects list to track all particles for efficient updates.


Particle Addition and Removal:
add_object(): Adds a particle (Sand, Rock, or Bubble) to the grid and all_grid_objects list, ensuring the target location is empty.
remove_object(): Removes a particle from the grid and all_grid_objects list, handling cleanup without manual memory management (thanks, Python!).


Simulation Logic:
do_whole_grid(): Updates all particles in a single step, sorting and processing Bubble objects first, then reversing the list to process Sand objects, preventing movement gaps.
Ensures smooth, realistic particle interactions by controlling update order.


Real-Time Visualization: Integrates with Pygame (optional for submission) to render the simulation, showing particles moving dynamically on the grid.
Testing Support: Passes provided pytest suite (test_sand_simulation.py) to verify Rock and Bubble class functionality and simulation behavior.
Extensibility: Added a "Whimsical Bubbles" feature for extra credit, using randomization (random.randrange()) to make bubbles float side-to-side lazily with customizable movement probabilities.
Clean Code: Refactored code for clarity and efficiency, keeping particle logic modular and simulation steps well-organized.

This project was a blast to work on, and it’s super satisfying to watch sand fall, bubbles rise, and rocks hold steady in a real-time grid. It’s a solid foundation I could keep building on with more particle types or behaviors!



# Calculator Language Interpreter - Project 3
Overview
I built this Calculator Language Interpreter for CS 111, and it’s been a wild ride creating a fully functional interpreter from scratch! This Python project takes interactive user input in the form of Calculator language expressions, like (+ 5 6) or (* 5 (+ 4 2)), and evaluates them to produce results. It’s built to handle a simple but powerful syntax, parsing expressions into syntax trees, evaluating them recursively, and handling errors gracefully. I reused and refined code from Lab 16 and Homework 6, adding new functionality to make it a complete, interactive tool.
The interpreter runs in a loop, prompting for expressions, processing them, and displaying results until I type exit. It supports addition, subtraction, multiplication, and division with any number of operands, applying operations in a left-to-right order. I loved diving into recursive parsing and evaluation, and it’s super satisfying to see my code turn strings into meaningful calculations!
Features

Interactive Interface:
Greets users with Welcome to the CS 111 Calculator Interpreter..
Prompts with calc >> for input, reading expressions as strings.
Exits gracefully with Goodbye! when exit is entered.


Expression Parsing:
Tokenization: Uses tokenize() from Lab 16 to break input strings into tokens.
Syntax Tree Construction: Implements parse() to wrap parse_tokens() from Homework 6, converting token lists into Pair objects (syntax trees) while hiding index details.
Handles nested expressions like (* 5 (+ 4 2)) correctly.


Expression Evaluation:
reduce(): Processes a list of operands with a given operator (e.g., add, mul) from the operator module, applying it sequentially with an initial value.
apply(): Maps operator strings (+, -, *, /) to the correct reduce() call, handling initial values for subtraction and division specially.
eval(): Recursively evaluates syntax trees, processing primitives (ints/floats) or calling apply() for expressions, with support for nested operations.


Error Handling:
Catches exceptions during parsing and evaluation, printing clear error messages and returning to the prompt without crashing.
Validates operators in apply(), raising TypeError for invalid ones.
Checks expression types in eval(), ensuring only primitives or Pair objects are processed.


Flexible Operator Support: Handles operators with two or more operands, evaluating left-to-right (e.g., (+ 3 4 5 6) computes ((3+4)+5)+6 = 18).
Modular Design:
Uses function names (parse, reduce, apply, eval) as specified for autograder compatibility.
Organizes parsing and evaluation logic cleanly, with parse_tokens() as an inner or separate function for encapsulation.


Testing Support: Compatible with provided pytest suite to verify parse(), reduce(), apply(), and eval(), plus full program input/output tests.
Extensibility: Added extra operators (//, %, sqrt, pow) for fun, making the interpreter even more versatile.

This project was a fantastic challenge that tied together parsing, recursion, and error handling into a slick little interpreter. I’m proud of how it handles complex expressions and stays robust under bad input!



# Web Crawler - Project 4
Overview
I built this Web Crawler for CS 111, and it’s been an incredible capstone to the course! This Python project is a versatile tool that crawls web pages, extracts data, and manipulates images, all while respecting web etiquette. It handles three main tasks: counting links and plotting their frequency, extracting and plotting tabular data, and downloading and filtering images. I used the Requests, BeautifulSoup, and matplotlib libraries to make it happen, building on my RequestGuard class from Homework 7 and image processing code from Project 1. It’s been a great way to learn about web protocols, HTML parsing, and data visualization while designing a program mostly from scratch.
The crawler takes command-line arguments to specify tasks, validates inputs, and produces outputs like histograms, CSV files, and modified images. I had to think carefully about handling different URL formats, managing data structures, and keeping the code clean. It’s awesome to see it crawl a site, pull data, or transform images with just a single command!
Features

Command-Line Interface:
Supports three commands: -c (link counting), -p (data extraction/plotting), and -i (image manipulation).
Validates arguments, printing errors with “invalid arguments” if they don’t meet requirements.
Example commands: 
-c <url> <plot.png> <data.csv> for link counting.
-p <url> <plot.png> <data.csv> for data plotting.
-i <url> <prefix> <filter> for image processing.




Link Counting (-c):
Crawls a website starting from a given URL, respecting robots.txt using RequestGuard from Homework 7.
Tracks all links in a list and counts occurrences in a dictionary, handling absolute, relative, and fragment URLs.
Generates a histogram with matplotlib.pyplot.hist() showing link frequency (e.g., how many pages were linked 1, 2, 3 times).
Saves the histogram as a PNG and raw data as a CSV (e.g., 1.0,3.0 for 3 pages linked once).


Data Extraction and Plotting (-p):
Loads a webpage and uses BeautifulSoup to find a table with ID CS111-Project4b.
Extracts x-values (first column) and y-values (subsequent columns) into lists, assuming float values.
Plots each y-value set against x-values using matplotlib.pyplot.plot(), with distinct colors (blue, green, red, black).
Saves the plot as a PNG and data as a CSV, with each line listing x-value and corresponding y-values.


Image Manipulation (-i):
Finds all <img> tags on a webpage, resolving absolute and relative URLs for image sources.
Downloads images using Requests and saves them locally with their original filenames.
Applies filters from Project 1 (sepia, grayscale, vertical flip, horizontal mirror) based on the filter flag.
Saves modified images with a user-specified prefix (e.g., grey_image1.png).


Web Etiquette:
Uses RequestGuard to check robots.txt and limit crawling to the specified domain, ensuring responsible behavior.
Handles various URL formats (full, relative, fragments) using urljoin and custom logic for accurate link resolution.


Data Management:
Maintains a list for links to visit (processed via indexing, popping, or slicing) and a dictionary for link counts.
Efficiently stores table data in lists for plotting and CSV output.


Output Handling:
Produces PNG plots and CSV files for link counts and table data.
Saves modified images as PNGs with consistent naming.


Code Reusability:
Refactored common tasks (e.g., CSV writing, URL processing) into functions to reduce duplication.
Reuses image_processing.py from Project 1 for image filters, integrated via imports.


Testing Support:
Passes provided pytest suite (test_webcrawler.py) for link counting, data plotting, and image manipulation.
Works with test URLs and general cases, avoiding hardcoding for robustness.


Extensibility:
Added support for depth-limited crawling as an extra feature, allowing the crawler to stop after a specified number of link levels.
Explored extending image filters to handle additional parameters for more complex transformations.



This project was a thrilling way to tie together web crawling, data processing, and image manipulation. I’m stoked about how it handles real-world web tasks while staying polite and efficient!
