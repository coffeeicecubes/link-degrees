# link-degrees
Finds the shortest path between 2 webpages by traversing the links on each page

# Basic Setup
0) If you want, make a new folder somewhere in your file structure where you can put this project

1) Go to the main github project page (https://github.com/coffeeicecubes/link-degrees/ - should be the page you are on right now) and click the green button labelled 'Code'. A window will pop up with 'Clone' and 'HTTPS' - ignore those and click 'Download ZIP' at the bottom

2) The source code has been downloaded as link-degrees-main.zip. Go to your Downloads folder though File Explorer (Windows) or Files (Linux) or Finder (MacOs).
* On Windows:
	- Right-click the link-degrees-main.zip folder and then click 'Extract All'
	- Select a destination to extract to*
* On Linux:
	* Right-click the link-degrees-main.zip folder and then click 'Open with Archive Manager'
	* In the box labelled 'Location' put the location where you want to store the files\*
* On MacOs:
	* Double click the link-degrees-main.zip folder
	* There will now be an unzipped folder with the same name in your Downloads directory
	* Move that folder to a location\*

\*you can put the source files wherever you want, I recommend a 'Python/Projects' folder in Home or if you have a 'random_crap' folder you can put it there, or you can leave these in Downloads, whatever

### Download of source is complete!

3) Now open your terminal and navigate to the location where you saved your files. You can do this with cd: 'cd' once to go to your home directory and then ls to see all your folders and then 'cd \[foldername\]' and then 'ls' again and then if necessary 'cd \[foldername\]' again until you are in the folder that contains the files you recently extracted). If you know the absolute path from Home, you can just type 'cd ~/\[absolute_path\]\/link-degrees-main'

4) Once you are in the folder containing the files 'degs.py' and 'README.md'
	* Ensure you have python3 and pip3 installed
		* You can check this by typing 
		* python3 --version (output should be similar to 'Python 3.8.5'
		* pip3 --version (output should be similar to 'pip 20.0.2 from /usr/lib/python3/dist-packages/pip (python 3.8)')
	* Install dependencies (sorry about that, I just really enjoy webscraping projects which require a http handler and html parser)
		* To install: write or paste (ctrl+shift+v) 'pip3 install requests && pip3 install beautifulsoup4' into your terminal
	* Start a local server to test on
		* Enter 'python3 -m http.server 9999' into your terminal \[This starts an http server in the current folder so that the program can access 'www' folder of test files. The server is on 127.0.0.1 <- your local machine aka localhost, not on the internet. This basically reroutes packets to yourself, on port 9999 - 9999 is just a random port that isn't specifically used for anything\]
	* (open a new terminal window since the server is now outputting logs in the one you were in before) and run the program!
		* type 'python3 degs.py'

# Notes
- CTRL-C to stop the server you created
- Running degs.py creates a 'log.txt' file in the link-degrees-main folder which has notes follows the recursion and general proceduring
- Edit the links in the html files in www/ or change the 'source' and 'dest' variables in the source code if you wish to test the program further
- The source code is pretty heavily commented, so it should hopefully be easy to understand
- The main idea is that the links on each page are put in a queue as they are found, and then they are processed through Breadth First Search which finds the shortest path from source to target. Unfortunately this particular method doesn't lend itself to weighting the nodes (links), which is something I spent a few hours attempting to implement
- Email me with any questions
~ I learned a lot about search algorithms, recursion and classful programming, github markdown, and debugging through this project (Turns out the object oriented part of Python has interesting syntax, with unique dissimilarities to other languages) ~
Thanks!
