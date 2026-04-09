import re


class QueryParser:
    def __init__(self) -> None:
        self.precedence = {
            "NOT": 3,
            "AND": 2,
            "OR": 1
        }

    def tokenize(self, query: str) -> list:
        return re.findall(r"\(|\)|AND|OR|NOT|[a-zA-Z]+", query)
    
    def to_rpn(self, tokens: list) -> list:
        output = []
        stack = []

        for token in tokens:
            token = token.upper()

            if token.isalpha() and token not in self.precedence:
                output.append(token)

            elif token in self.precedence:
                while (stack and stack[-1] != "(" and self.precedence.get(stack[-1], 0) >= self.precedence[token]):
                    output.append(stack.pop())
                stack.append(token)

            elif token == "(":
                stack.append(token)

            elif token == ")":
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
                stack.pop()

        while stack:
            output.append(stack.pop())

        return output