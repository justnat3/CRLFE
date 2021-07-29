#!/usr/bin/python3

"""
NAME
    crlfe - Control Return Line Feed Eliminator.
SYNOPSIS
    ./crlfe <file_path>
OPTIONS
    NULL
DESCRIPTION
    Takes windows-formated files & converts them to LF (unix formats)
    Exit Status:
    Returns success unless the file could not be found/openned or an invalid option is given.
IMPLEMENTATION
    Nathan Reed <nreed@linux.com>
"""

from dataclasses import dataclass
import subprocess
import sys
import os

# safe immutable path type for the static paths
@dataclass(init=True, frozen=True)
class Path:
    
    # path intended to be asserted
    path: str

    def __post_init__(self):
        try:
            
            # if the path exists
            assert os.path.exists(self.path)

            # check if it is a file
            assert os.path.isfile(self.path)

            # redundent isdir() check
            assert not os.path.isdir(self.path)

            # check if it is a symbolic link
            assert not os.path.islink(self.path)
            
            # check if it contains a os correct path seperator
            assert self.path.__contains__(os.path.sep)

        # hit if there is something wrong with the path given
        except AssertionError:
            print("Could not read path")

    # handle cast to str()
    def __str__(self):
        return str(self.path)


def print_help() -> None:
    print("""NAME
    crlfe - Control Return Line Feed Eliminator.
SYNOPSIS
    ./crlfe <file_path>
OPTIONS
    NULL
DESCRIPTION
    Takes windows-formated files & converts them to LF (unix formats)
    Exit Status:
    Returns success unless the file could not be found/openned or an invalid option is given.
IMPLEMENTATION
    Nathan Reed <nreed@webcotube.com>
""")


# error text
def error(text: str) -> None:
    assert isinstance(text, str)
    print(f"\33[91m{text}\033[0m")

# error text
def warning(text: str) -> None:
    assert isinstance(text, str)
    print(f"\33[93m{text}\033[0m")

# helper function to read out the data of a file and defer its closing.
def _get_content(p: str) -> str:
    # ensure path is safe to use
    p = str( Path(p) )    

    # open a file descriptor and return the buffer 
    with open(p, 'rb') as fd:
        return fd.read()

# constants for line endings
WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'

def _find_eleminate_line_endings(file_t: str) -> int:
    
    # check_line_ending flag
    cle = False
    
    try:
        # the file buffer in the form of a string
        content: str = _get_content(file_t)
        
        # checking if the buffer contains a incorrect line ending for unix
        if content.__contains__(WINDOWS_LINE_ENDING):

            # set the cle flag to tell the program that the file given contains CRLF line-endings
            cle = True
    
    # hit if we can't read the file
    except Exception as err:
        error("--FAILURE--")
        error("Unable to write file {file_t}")
            sys.exit(1)

    # after we've told the program about the line-ending we are going to replace(DESTROY) them
    if cle is True:
        
        # replace the bad line endings with unix line endings
        content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)

        try:        
            
            # write the content with unix line endings back to the file
            with open(p, 'wb') as fd:
                fd.write(content)

        # hit if we can't access the file
        except Exception:
        error("--FAILURE--")
        error("Unable to write file {file_t}")
            sys.exit(1)

        # read the content into a buffer one more time
        content = _get_content(file_t)

        # fail if it still has bad line endings
        # FIXME: does not write the original buffer back to the file - uses a little more memory
        if content.__contains__(WINDOWS_LINE_ENDING):
            error("FAILURE")
            error("file @ path still contains CRLF")
            error("could not convert CRLF to LF")
            sys.exit(1)

        # exit 0 to confirm the line endings do not exist anymore
        return 0
    
    # exit 1 if hit the end of the function 
    return 1

if __name__ == "__main__":

    # check the bounds of the sysargv array
    if len(sys.argv) <= 1:
        print_help()
        sys.exit(1)
    
    # get the file path for our program
    p = sys.argv[1]

    # check if its a file path initally
    if not p.__contains__(os.path.sep):
        print_help()
        sys.exit(1)
        
    # use this function to eleminate shit line endings
    _find_eleminate_line_endings()
