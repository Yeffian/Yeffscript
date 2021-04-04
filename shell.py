from ys_lexer import Lexer
from ys_parser import Parser
from ys_tokentypes import TokenType
from ys_replutils import *

import sys

def main():
    while True:
        text = input(">> ")

        if text == 'exit':
            abort()
        if text == 'run':
            filepath = input("Enter a path for the file which you want to run: ")
            with open(filepath, 'r') as inputFile:
                text = inputFile.read()

        lexer = Lexer(text)
        parser = Parser(lexer)
        
        parser.program()

if __name__ == '__main__':
    main()
