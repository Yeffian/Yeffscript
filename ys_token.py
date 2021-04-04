from ys_tokentypes import TokenType

class Token():
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText   # The token's actual text. Used for identifiers, strings, and numbers.
        self.kind = tokenKind   # The TokenType that this token is classified as.

    @staticmethod
    def check_if_keyword(token_text):
        for kind in TokenType:
            if kind.name == token_text and 100 <= kind.value < 200:
                return kind
