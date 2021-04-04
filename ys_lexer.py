from ys_token import Token
from ys_tokentypes import TokenType

from os import system, name
import sys

class Lexer():
    def __init__(self, code):
        self.source = code + '\n'
        self.cur_char = ''
        self.cur_pos = -1
        self.next_char()

    def next_char(self):
        self.cur_pos += 1
        if self.cur_pos >= len(self.source):
            self.cur_char = '\0'
        else:
            self.cur_char = self.source[self.cur_pos]

    def peek(self):
        if self.cur_pos + 1 >= len(self.source):
            return '\0'
        return self.source[self.cur_pos + 1]

    def abort(self, message):
        sys.exit("Lexer error: " + message)

    def skip_white_space(self):
        while self.cur_char == ' ' or self.cur_char == '\t' or self.cur_char == '\r':
            self.next_char()

    def skip_comment(self):
        if self.cur_char == '#':
            while self.cur_char != '\n':
                self.next_char()

    def get_token(self):
        self.skip_white_space()
        self.skip_comment()
        token = None

        if self.cur_char == '+':
            token = Token(self.cur_char, TokenType.PLUS)
        elif self.cur_char == '-':
            token = Token(self.cur_char, TokenType.MINUS)
        elif self.cur_char == '*':
            token = Token(self.cur_char, TokenType.ASTERISK)
        elif self.cur_char == '/':
            token = Token(self.cur_char, TokenType.SLASH)

        elif self.cur_char == '=':
            if self.peek() == '=':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char + self.cur_char, TokenType.NOT_EQUALS)
            else:
                token = Token(self.cur_char, TokenType.EQUALS)
        elif self.cur_char == '>':
            if self.peek() == '=':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char + self.cur_char, TokenType.GREATER_THAN_OR_EQUAL_TO)
            else:
                token = Token(self.cur_char, TokenType.GREATER_THAN)
        elif self.cur_char == '<':
            if self.peek() == '=':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char + self.cur_char, TokenType.LESS_THAN_OR_EQUAL_TO)
            else:
                token = Token(self.cur_char, TokenType.LESS_THAN)
        elif self.cur_char == '!':
            if self.peek() == '=':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char + self.cur_char, TokenType.NOT_EQUALS)
            else:
                self.abort("Expected '!=', got '!'" + self.peek())

        elif self.cur_char == '\"':
            self.next_char()
            start_pos = self.cur_pos

            while self.cur_char != '\"':
                if (self.cur_char == '\r' or
                        self.cur_char == '\n' or self.cur_char == '\t' or
                        self.cur_char == '\\' or self.cur_char == '%'):
                    self.abort("Illegal character in string.")
                self.next_char()

            token_text = self.source[start_pos: self.cur_pos]
            token = Token(token_text, TokenType.STRING)
        elif self.cur_char.isdigit():
            start_pos = self.cur_pos
            while self.peek().isdigit():
                self.next_char()
            if self.peek() == '.':
                self.next_char()

                if not self.peek().isdigit():
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.next_char()
            token_text = self.source[start_pos: self.cur_pos + 1]
            token = Token(token_text, TokenType.NUMBER)
        elif self.cur_char.isalpha():
            start_pos = self.cur_pos
            while self.peek().isalnum():
                self.next_char()

            token_text = self.source[start_pos: self.cur_pos + 1]
            keyword = Token.check_if_keyword(token_text)
            if keyword is None:
                token = Token(token_text, TokenType.IDENT)
            else:
                token = Token(token_text, keyword)

        elif self.cur_char == '\n':
            token = Token(self.cur_char, TokenType.NEWLINE)
        elif self.cur_char == '\0':
            token = Token(self.cur_char, TokenType.EOF)
        else:
            self.abort("Unknown token: " + self.cur_char)
        self.next_char()
        return token