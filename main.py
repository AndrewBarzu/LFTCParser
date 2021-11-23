# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Grammar import Grammar


# Press the green button in the gutter to run the script.
from Parser import RecursiveDescendantParser

if __name__ == '__main__':
    myGrammar = Grammar.readFromFile("g2.in")

    # parser = RecursiveDescendantParser(myGrammar)
    #
    # parser.parse(("b", "b", "a", "c"))
    # parser.parse(("b", "a", "c"))
    # parser.parse(("a",))
    # parser.parse(("b", "a"))
    # parser.parse(("c",))


    while True:
        cmd = int(input("> "))
        if cmd == 0:
            exit(0)
        elif cmd == 1:
            print(myGrammar.getNonterminalsString())
        elif cmd == 2:
            print(myGrammar.getTerminalsString())
        elif cmd == 3:
            print(myGrammar.getProductionsString())
        elif cmd == 4:
            LHS = input("LHS = ").split()
            key = tuple([keypart for keypart in LHS])
            print(myGrammar.getProductionsForKeyAsString(key))
        elif cmd == 5:
            print("CFG? " + str(myGrammar.CFG))
        elif cmd == 6:
            print("new grammar: ")
            print(Grammar.removeLeftRecursion(myGrammar).getProductionsString())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
