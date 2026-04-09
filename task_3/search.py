class Search:
    def __init__(self, index) -> None:
        self.index = index

    def evaluate(self, rpn_tokens: list) -> set:
        stack = []

        for token in rpn_tokens:
            if token not in ("AND", "OR", "NOT"):
                docs = self.index.get_docs(token.lower())
                stack.append(docs)

            elif token == "NOT":
                operand = stack.pop()
                result = self.index.documents - operand
                stack.append(result)

            else:
                right = stack.pop()
                left = stack.pop()

                if token == "AND":
                    stack.append(left & right)
                elif token == "OR":
                    stack.append(left | right)

        return stack.pop() if stack else set()