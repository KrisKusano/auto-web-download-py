#auto-web-download-py
check if local copy of a file is newer than a web file, then downloads the file if it is new

Useful for scheduling a task to go check if a file has changed and download
a newest version.

#usage
From Windows cmd, with python 3.3 or greater:
```
py auto-web-download-py "http://www.url.to.file" "C:\Path\to\download\destination.txt"
```

#check for newer files
Before downloading the file, the program checks for HTTP header items `last-modified` 
or `Date`. If the HTTP header date is older than the copy that is stored locally,
no download occurs.

#logging
Creates a log file (`download.log`) in the same directory as the destination file. 
The log records the local time that the download was initiated and the status
(a new file was downloaded or no file was downloaded).

#TODO
* some files do not have a `last-modified` or `Date` header property. 
  For these, we should then download the file and check if the contents of the file has changed
* the exceptions should print to the log file, not the interpreter