from collections import defaultdict
from typing import Set, Dict, Tuple, Iterable, List, Union, Optional
from functools import reduce

# Recursive Descendant

class NonterminalNotDefined(Exception):
    pass

class SymbolNotDefined(Exception):
    pass

class NotCFG(Exception):
    pass

class UnproductiveGrammar(Exception):
    pass

class Grammar:
    def __init__(self, N: Set[str], Sigma: Set[str], P: Dict[Tuple[str], List[Tuple[str]]], S: str):
        self.N = N
        self.Sigma = Sigma
        self.P = P
        self.S = S
        self.CFG = True

    def getNonterminalsString(self) -> str:
        return reduce(lambda x, y: x + ", " + y if x != "" else y, self.N, "")

    def getTerminalsString(self) -> str:
        return reduce(lambda x, y: x + ", " + y if x != "" else y, self.Sigma, "")

    @staticmethod
    def _singleProductionToString(prod: Iterable[str]) -> str:
        return reduce(lambda x, y: x + " " + y if x != "" else y, prod, "")

    @staticmethod
    def _prodToString(productions: Tuple[Tuple[str], List[Tuple[str]]]) -> str:
        res = productions[0]

        productionsAsStrings = map(Grammar._singleProductionToString, productions[1])

        return Grammar._singleProductionToString(res) + " -> " + reduce(lambda x, y: x + " | " + y if x != "" else y, productionsAsStrings, "")

    def getProductionsString(self) -> str:

        productionsAsStrings = map(lambda entry: Grammar._prodToString(entry), self.P.items())

        return reduce(lambda x, y: x + "\n" + y if x != "" else y, productionsAsStrings, "")

    def getProds(self, nonTerminal: Tuple[str]) -> List[Tuple[str]]:
        if nonTerminal not in self.P.keys():
            return list()
        return self.P[nonTerminal]

    def getProductionsForKeyAsString(self, key: Tuple[str]) -> str:
        return Grammar._prodToString((key, self.getProds(key)))

    @staticmethod
    def removeLeftRecursion(grammar: 'Grammar') -> 'Grammar':
        if not grammar.CFG:
            raise NotCFG
        newGrammar = Grammar(grammar.N.copy(), grammar.Sigma.copy(), grammar.P.copy(), grammar.S)
        predicate = lambda rhs, lhs: rhs[0] == lhs
        LHSs = list(newGrammar.P.keys())
        for i, LHS in enumerate(LHSs):
            changed = True
            while changed:
                changed = False
                RHS = set(newGrammar.P[LHS])
                newRHS = set()
                for alphai in RHS:
                    leadingSymbol = alphai[0]
                    if leadingSymbol not in newGrammar.N or (leadingSymbol,) not in LHSs[:i]:
                        newRHS.add(alphai)
                        continue
                    betai = alphai[1:]
                    for alphaj in newGrammar.P[(leadingSymbol, )]:
                        newRHS.add(alphaj + betai)
                if newRHS != RHS:
                    changed = True
                newGrammar.P[LHS] = list(newRHS)


            RHS = newGrammar.P[LHS][:]
            newRHS = []
            recursiveRHSIndices = [i for i, e in enumerate(RHS) if predicate(e, LHS[0])]
            nonRecursiveRHSIndidces = [i for i, e in enumerate(RHS) if not predicate(e, LHS[0])]
            if len(recursiveRHSIndices) > 0 and len(nonRecursiveRHSIndidces) > 0:
                newSymbol = LHS[0] + "'"
                newGrammar.N.add(newSymbol)
                newSymbol = (newSymbol,)
                for idx in nonRecursiveRHSIndidces:
                    newProd = RHS[idx] + newSymbol
                    newRHS.append(newProd)

                newProds = {('Epsilon',)}
                for idx in recursiveRHSIndices:
                    newProd = RHS[idx][1:] + newSymbol
                    newProds.add(newProd)
                newGrammar.P[newSymbol] = list(newProds)
            elif len(recursiveRHSIndices) > 0 and len(nonRecursiveRHSIndidces) == 0:
                raise UnproductiveGrammar()
            else:
                newRHS = RHS.copy()

            newGrammar.P[LHS] = list(newRHS)

        return newGrammar

    @staticmethod
    def readFromFile(filename: str) -> 'Grammar':
        g = Grammar(set(), set(), {}, "")
        with open(filename, "r") as f:
            g.S = f.readline().split()[0]
            g.N.add(g.S)
            for nonterminal in f.readline().split():
                g.N.add(nonterminal)

            for terminal in f.readline().split():
                g.Sigma.add(terminal)

            for line in f:
                production = line.split()
                i = 0
                key = []
                while production[i] != ":":
                    if production[i] not in g.Sigma and production[i] not in g.N:
                        raise SymbolNotDefined(production)
                    key.append(production[i])
                    i += 1

                if len(key) > 1:
                    g.CFG = False

                prod = []
                productions = set()
                for entry in production[i + 1:]:
                    if entry == "$":
                        productions.add(tuple(prod))
                        prod = []
                        continue
                    if entry not in g.Sigma and entry not in g.N and entry != "Epsilon":
                        raise SymbolNotDefined(entry)
                    prod.append(entry)
                productions.add(tuple(prod))
                g.P[tuple(key)] = list(productions)

        return g
