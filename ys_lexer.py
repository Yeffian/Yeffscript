from ys_token import Token
from ys_tokentypes import TokenType

from os import system, name
import sys


DIGITS = 123456789

class Lexer():
    def __init__(self, text):
        self.source = text + '\n' # The actual source code to lex
        self.curChar = '' # The current character the lexer is on
        self.curPos = -1 # The current position of the lexer
        self.advance()

    # Process the next character.
    def advance(self):
        self.curPos += 1

        if self.curPos >= len(self.source):
            self.curChar = '\0'  # EOF
        else:
            self.curChar = self.source[self.curPos]

    # Return the lookahead character.
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
            
        return self.source[self.curPos+1]

    # Invalid token found, print error message and exit.
    def abort(self, message, reason):
        sys.exit("Lexing error. " + message)
		
    # Skip whitespace except newlines, which we will use to indicate the end of a statement.
    def skip_whitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.advance()
		
    # Skip comments in the code.
    def skip_comment(self):
         if self.curChar == '#':
            while self.curChar != '\n':
                self.advance()

    # Return the next token.
    def get_token(self):
        self.skip_whitespace()
        self.skip_comment()

        token = None

        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == '=':
            # Check whether this token is = or ==
            if self.peek() == '=':
                lastChar = self.curChar
                self.advance()
                token = Token(lastChar + self.curChar, TokenType.DOUBLE_EQUALS)
            else:
                token = Token(self.curChar, TokenType.EQUALS)
        elif self.curChar == '>':
            # Check whether this is token is > or >=
            if self.peek() == '=':
                lastChar = self.curChar
                self.advance()
                token = Token(lastChar + self.curChar, TokenType.GREATER_THAN_OR_EQUAL_TO)
            else:
                token = Token(self.curChar, TokenType.GREATER_THAN)
        elif self.curChar == '<':
                # Check whether this is token is < or <=
                if self.peek() == '=':
                    lastChar = self.curChar
                    self.advance()
                    token = Token(lastChar + self.curChar, TokenType.LESS_THAN_OR_EQUAL_TO)
                else:
                    token = Token(self.curChar, TokenType.LESSER_THAN)
        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.advance()
                token = Token(lastChar + self.curChar, TokenType.NOT_EQUALS)
            else:
                self.abort("Expected != , got !" + self.peek(), None)
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == '\0':
            token = Token('', TokenType.EOF)
        else:
            self.abort("Unknown token: " + self.curChar, None)

        self.advance()
        return token
