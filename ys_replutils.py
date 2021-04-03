import sys
import colorama as colour

from subprocess import call
from os import system, name

colour.init()

def abort():
    print_red("Exiting repl...")
    sys.exit()

def print_red(msg):
    print(colour.Fore.RED + msg)

def print_green(msg):
    print(colour.Fore.GREEN + msg)
