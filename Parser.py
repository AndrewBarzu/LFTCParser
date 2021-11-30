from collections import deque
from typing import Tuple, List

from Grammar import Grammar


class RecursiveDescendantParser:
    def __init__(self, grammar: Grammar):
        self._grammar = grammar

    def parse(self, word: Tuple) -> List[str]:
        config = RecursiveDescendantConfiguration(self._grammar)
        while config.s not in {'f', 'e'}:
            if config.s == 'q':
                if config.i == len(word) and len(config.inputStack) == 0:
                    config.success()
                else:
                    if len(config.inputStack) > 0 and config.inputStack[-1] in self._grammar.N:
                        config.expand()
                    else:
                        if config.i < len(word) and len(config.inputStack) > 0 and config.inputStack[-1] == word[config.i]:
                            config.advance()
                        else:
                            config.momentaryInsuccess()
            else:
                if config.s == 'b':
                    if len(config.workingStack) > 0 and config.workingStack[-1] in self._grammar.Sigma:
                        config.back()
                    elif len(config.workingStack) > 0:
                        config.anotherTry()

        if config.s == 'e':
            print('Error')
            return []
        print('Sequence accepted')
        return self._makeTreeFromDerivationSeq(config.workingStack)

    def _makeTreeFromDerivationSeq(self, derivationString: List[str]) -> List:
        result = [(derivationString[0].split('$')[0], -1, -1)]
        i = 0
        j = 0
        while j < len(derivationString) and i < len(result):
            top = result[i]
            if top[0] not in self._grammar.N:
                i += 1
                continue
            expandWith = None
            while True:
                if '$' not in derivationString[j]:
                    j += 1
                    continue
                nonterminal, productionNumber = derivationString[j].split('$')
                if nonterminal == top[0]:
                    expandWith = (nonterminal, productionNumber)
                    break
                j += 1

            nonterminal, productionNumber = expandWith
            productionNumber = int(productionNumber)
            production = self._grammar.P[(nonterminal, )][productionNumber]
            for symbol in production:
                result.append((symbol, i, len(result) + 1))
            result[-1] = (*result[-1][:-1], -1)
            i += 1
        return result


class RecursiveDescendantConfiguration:
    def __init__(self, grammar: Grammar):
        self._grammar = grammar
        self.s = 'q'
        self.i = 0
        self.workingStack: List[str] = []
        self.inputStack: List[str] = [grammar.S]

    def expand(self):
        currentSymbol = self.inputStack.pop()
        production = self._grammar.getProds((currentSymbol, ))
        if production[0] != ('Epsilon', ):
            self.inputStack += reversed(production[0])
        self.workingStack.append(currentSymbol[0] + "$0")

    def advance(self):
        self.i += 1
        terminal = self.inputStack.pop()
        self.workingStack.append(terminal)

    def momentaryInsuccess(self):
        self.s = 'b'

    def back(self):
        self.i -= 1
        terminal = self.workingStack.pop()
        self.inputStack.append(terminal)

    def anotherTry(self):
        annotatedSymbol = self.workingStack.pop()
        nonterminal, productionNumber = annotatedSymbol.split("$")
        productionNumber = int(productionNumber)
        productions = self._grammar.getProds((nonterminal, ))

        currentProduction = productions[productionNumber]
        for _ in currentProduction:
            _ = self.inputStack.pop()

        if productionNumber < len(productions) - 1:
            newProd = productions[productionNumber + 1]
            if newProd != ('Epsilon', ):
                self.inputStack += reversed(newProd)
            self.workingStack.append(nonterminal + "${0}".format(productionNumber + 1))
            self.s = 'q'
            return

        if self.i == 0 and nonterminal == self._grammar.S:
            self.s = 'e'
            return

        self.inputStack.append(nonterminal)

    def success(self):
        self.s = 'f'