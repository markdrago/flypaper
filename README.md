Flypaper
========
Flypaper detects buggy files in your code base.

The original idea for this project came from:  
http://google-engtools.blogspot.com/2011/12/bug-prediction-at-google.html

How It Works
------------
Flypaper's underlying principle is that if a file has required frequent
modification to fix bugs in the past, then there's probably something about
that file which makes it more likely to generate bugs.  If you know which files
in your code base tend to attract the most bugs you can treat them differently,
by soliciting more code reviews, generally being more careful while editing
them, or even refactoring them entirely.

In order to use Flypaper, you must have done a few things first:
1. Kept track of bugs with some bug tracking system where bugs have IDs.
2. Made commits to your version control system with the bug IDs mentioned in the
   commit message.
3. You must be able to get a list of the bug IDs from your bug tracking system.

You invoke flypaper like this:
    ./flypaper.py --buglist <filename> --repo <repository directory> --startdate 2011-01-01

Flypaper will then output a list of filenames with corresponding bugginess
scores sorted by bugginess.  The bugginess of a file is determined by the number
and recency of bugs that were fixed by modifying the given file.  The formula
used is:  
    bugginess = sum(1/1+e^(-3t+3))
Where t is the timestamp of the bug-fixing commit.  The timestamp used in the
equation is normalized from 0 to 1, where 0 is the startdate and 1 is now
(where now is when the algorithm was run).  For more explanation about this
formula, take a look at the article which inspired this project here:
http://google-engtools.blogspot.com/2011/12/bug-prediction-at-google.html

