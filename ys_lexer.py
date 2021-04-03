from ys_token import Token
from ys_tokentypes import TokenType

from ys_replutils import print_red

from os import system, name
import sys

class Lexer():
    def __init__(self, text):
        self.source = text + '\n' # The actual source code to lex
        self.curChar = '' # The current character the lexer is on
        self.curPos = -1 # The current position of the lexer
        self.advance()

    
    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # Relies on all keyword enum values being 1XX.
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind

        return None


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
    def abort(self, message):
        print_red("Lexing error. " + message)
        sys.exit()
		
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
        elif self.curChar == ')':
            token = Token(self.curChar, TokenType.LPAREN)
        elif self.curChar == '(':
            token = Token(self.curChar, TokenType.RPAREN)
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
        elif self.curChar == '\"':
            # Get characters between quotations.
            self.advance()
            startPos = self.curPos

            while self.curChar != '\"':
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.advance()

            tokText = self.source[startPos : self.curPos] # Get the substring.
            token = Token(tokText, TokenType.STRING)
        elif self.curChar.isdigit():
            startPos = self.curPos
            while self.peek().isdigit():
                self.advance()
            if self.peek() == '.': # Decimal
                self.advance()

                # Must have at least one digit after decimal.
                if not self.peek().isdigit(): 
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.advance()

            tokText = self.source[startPos : self.curPos + 1] # Get the substring.
            token = Token(tokText, TokenType.NUMBER)
        elif self.curChar.isalpha():
            # Leading character is a letter, so this must be an identifier or a keyword.
            # Get all consecutive alpha numeric characters.
            startPos = self.curPos
            while self.peek().isalnum():
                self.advance()

            # Check if the token is in the list of keywords.
            tokText = self.source[startPos : self.curPos + 1] # Get the substring.
            keyword = self.checkIfKeyword(tokText)
            if keyword == None: # Identifier
                token = Token(tokText, TokenType.IDENT)
            else:   # Keyword
                token = Token(tokText, keyword)
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == '\0':
            token = Token('', TokenType.EOF)
        else:
            self.abort("Unknown token: " + self.curChar, None)

        self.advance()
        return token
