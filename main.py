# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Grammar import Grammar


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    myGrammar = Grammar.readFromFile("g1.txt")

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

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
