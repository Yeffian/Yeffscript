import sys
from ys_lexer import *
from ys_replutils import print_red, print_green

# Parser object keeps track of current token and checks if the code matches the grammar.
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.curToken = None
        self.peekToken = None
        self.next_token()
        self.next_token()    # Call this twice to initialize current and peek

    # Return true if the current token matches.
    def check_token(self, kind):
        return kind == self.curToken.kind

    # Return true if the next token matches.
    def check_peek(self, kind):
        pass

    # Try to match current token. If not, error. Advances the current token.
    def match(self, kind):
        pass

    # Advances the current token.
    def next_token(self):
         self.curToken = self.peekToken
         self.peekToken = self.lexer.get_token()
        # Lexer handles passing the EOF

    # Quit the program
    def abort(self, message):
        print_red('Error: ' + message)
        sys.exit()

    def program(self):
        print_green("YEFFSCRIPT COMPILER BETA")

        # Parse all the statements in the program.
        while not self.check_token(TokenType.EOF):
            self.statement()

    def statement(self):
        # Check the first token to see what kind of statement this is.

        # "PRINT" (expression | string)
        if self.check_token(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.next_token()

            if self.check_token(TokenType.STRING):
                # Simple string.
                self.next_token()

            else:
                # Expect an expression.
                self.expression()

        # "IF" comparison "THEN" {statement} "ENDIF"
        elif self.check_token(TokenType.IF):
            print("STATEMENT-IF")
            self.next_token()
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()

            # Zero or more statements in the body.
            while not self.check_token(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)

        # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.check_token(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.next_token()
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()

            # Zero or more statements in the loop body.
            while not self.check_token(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)

         # "LABEL" ident
        elif self.check_token(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.next_token()
            self.match(TokenType.IDENT)

            if self.check_token(TokenType.STRING):
                # Simple string.
                self.next_token()

            
        # "GOTO" ident
        elif self.check_token(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.next_token()
            self.match(TokenType.IDENT)

            if self.check_token(TokenType.STRING):
                # Simple string.
                self.next_token()

        # "LET" ident "=" expression
        elif self.check_token(TokenType.LET):
            print("STATEMENT-LET")
            self.next_token()
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()

        # "INPUT" ident
        elif self.check_token(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.next_token()
            self.match(TokenType.IDENT)

        # This is not a valid statement. Error!
        else:
            self.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")

        # Newline.
        self.nl()


    def nl(self):
        print("NEWLINE")
		
        # Require at least one newline.
        self.match(TokenType.NEWLINE)

        # But we will allow extra newlines too, of course.
        while self.check_token(TokenType.NEWLINE):
            self.next_token()

    