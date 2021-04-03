from ys_lexer import Lexer
from ys_tokentypes import TokenType
from ys_replutils import abort

def main():
    while True:
        text = input(">> ")
        lexer = Lexer(text)

        if text == 'exit':
            abort()

        token = lexer.get_token()

        while token.kind != TokenType.EOF:
            if(token.kind == TokenType.NEWLINE):
                print(f'[{token.kind}]')
            else: 
             print(f'[{token.kind} : {token.text}]')

            token = lexer.get_token()

if __name__ == '__main__':
    main()
