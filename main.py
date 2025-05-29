from Grammar import Grammar
if __name__ == "__main__":
    grammar = Grammar()
    grammar.load_from_file("grammar.txt")
    grammar.display()
