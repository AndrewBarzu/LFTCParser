# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Grammar import Grammar
import pydot

# Press the green button in the gutter to run the script.
from Parser import RecursiveDescendantParser

if __name__ == '__main__':
    myGrammar = Grammar.readFromFile("g1.in")
    myGrammar = Grammar.removeLeftRecursion(myGrammar)

    parser = RecursiveDescendantParser(myGrammar)

    parser.parse(("b", "b", "a", "c")).plotParseTree("g1_1.png")
    parser.parse(("b", "a", "c")).plotParseTree("g1_2.png")
    parser.parse(("a",)).plotParseTree("g1_3.png")
    parser.parse(("b", "a")).plotParseTree("g1_4.png")
    parser.parse(("a", "c",)).plotParseTree("g1_5.png")

    # program = []
    # with open("test.in", "r") as f:
    #     for line in f:
    #         if line != "":
    #             program.append(line.strip())
    # program = tuple(program)
    # parse_tree = parser.parse(program)
    # parse_tree.plotParseTree("test.png")

    # digraph = pydot.Dot("my_graph", graph_type="digraph")
    # nodes = []
    # for i in range(len(parse_tree)):
    #     idx_as_str = str(i)
    #     elem = parse_tree[i]
    #     node = pydot.Node(idx_as_str, label='"' + elem[0] + '"')
    #     digraph.add_node(node)
    #     nodes.append(node)
    #     if elem[1] != -1:
    #         edge = pydot.Edge(str(elem[1]), idx_as_str)
    #         digraph.add_edge(edge)
    # digraph.write("test.png", format="png")



    # while True:
    #     cmd = int(input("> "))
    #     if cmd == 0:
    #         exit(0)
    #     elif cmd == 1:
    #         print(myGrammar.getNonterminalsString())
    #     elif cmd == 2:
    #         print(myGrammar.getTerminalsString())
    #     elif cmd == 3:
    #         print(myGrammar.getProductionsString())
    #     elif cmd == 4:
    #         LHS = input("LHS = ").split()
    #         key = tuple([keypart for keypart in LHS])
    #         print(myGrammar.getProductionsForKeyAsString(key))
    #     elif cmd == 5:
    #         print("CFG? " + str(myGrammar.CFG))
    #     elif cmd == 6:
    #         print("new grammar: ")
    #         print(Grammar.removeLeftRecursion(myGrammar).getProductionsString())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
