from ys_lexer import Lexer
from ys_tokentypes import TokenType
from ys_replutils import abort

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
        token = lexer.get_token()

        print('TOKEN TREE')
        while token.kind != TokenType.EOF:
            if(token.kind == TokenType.NEWLINE):
                print(f'├─{token.kind}')
            else: 
             print(f'├─{token.kind} : {token.text}')

            token = lexer.get_token()

if __name__ == '__main__':
    main()
