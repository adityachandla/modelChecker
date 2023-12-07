from __future__ import annotations
from typing import TypeAlias, Union
from dataclasses import dataclass


class TrueLiteral:
    pass


class FalseLiteral:
    pass


@dataclass
class RecursionVariable:
    name: str


@dataclass
class LogicFormula:
    "left && right or left || right"
    left: Formula
    right: Formula
    is_and: bool


@dataclass
class NuFormula:
    variable: RecursionVariable
    formula: Formula


@dataclass
class MuFormula:
    variable: RecursionVariable
    formula: Formula


@dataclass
class DiamondFormula:
    label: str
    formula: Formula


@dataclass
class BoxFormula:
    label: str
    formula: Formula


Formula: TypeAlias = Union[TrueLiteral, FalseLiteral, RecursionVariable,
                           LogicFormula, NuFormula, MuFormula,
                           DiamondFormula, BoxFormula]

## There are a lot of spaces in the files with new lines
## This function removes as many as possible.
def make_pretty(input_string: str) -> str:
    c = []
    i = 0
    while i < len(input_string)-1:
        if input_string[i] == ' ' and input_string[i+1] == ' ':
            i += 1
        else:
            c.append(input_string[i])
            i += 1
    if input_string[-1] != ' ':
        c.append(input_string[-1])
    return ''.join(c)

def parse_query(filepath: str) -> (Formula, set[str], str):
    with open(filepath, 'r') as formula_file:
        formula_lines = formula_file.read().split("\n")
        valid_line = lambda line: len(line) > 0 and not line.startswith("%")
        formula_lines = [l for l in formula_lines if valid_line(l)]
        formula_string = " ".join(formula_lines)
        formula_string = make_pretty(formula_string)
        formula_string = formula_string.strip()
    parser = Parser(formula_string)
    formula = parser.parse()
    variables = parser.get_variables()
    return (formula, variables, formula_string)


class Parser:
    def __init__(self, formula_str: str):
        self.formula_str = formula_str
        self.variables = set()
        self.index = 0

    def get_char(self) -> str:
        return self.formula_str[self.index]

    def expect(self, s: str):
        self.index += len(s)

    def get_variables(self):
        return self.variables

    def skip_whitespace(self):
        if self.index == len(self.formula_str):
            return
        while self.get_char() == ' ':
            self.index += 1

    def parse(self) -> Formula:
        if self.get_char() == 't':
            return self.parse_true_literal()
        elif self.get_char() == 'f':
            return self.parse_false_literal()
        elif self.get_char().isupper():
            return self.parse_recursion_variable()
        elif self.get_char() == '(':
            return self.parse_logic_formula()
        elif self.get_char() == 'm':
            return self.parse_mu_formula()
        elif self.get_char() == 'n':
            return self.parse_nu_formula()
        elif self.get_char() == '[':
            return self.parse_box_formula()
        elif self.get_char() == '<':
            return self.parse_diamond_formula()

    def parse_true_literal(self) -> TrueLiteral:
        self.expect("true")
        self.skip_whitespace()
        return TrueLiteral()

    def parse_false_literal(self) -> FalseLiteral:
        self.expect("false")
        self.skip_whitespace()
        return FalseLiteral()

    def parse_recursion_variable(self) -> RecursionVariable:
        name = self.get_char()
        # We assume no free variables
        self.variables.add(name)
        self.expect(name)
        var = RecursionVariable(name)
        self.skip_whitespace()
        return var

    def parse_logic_formula(self) -> LogicFormula:
        """
        This method deviates from the provided algorithm.
        Here we just do all the work in a single function.
        If something breaks, it is more likely to be because of this function.
        """
        self.expect("(")
        self.skip_whitespace()
        first = self.parse()
        self.skip_whitespace()
        andOperator = self.get_char() == '&'
        # Expect does not really check anything, it just advances the pointer
        # therefore, this should also take care of || case.
        self.expect("&&")
        self.skip_whitespace()
        second = self.parse()
        self.skip_whitespace()
        self.expect(")")
        self.skip_whitespace()
        return LogicFormula(first, second, andOperator)

    def parse_mu_formula(self) -> MuFormula:
        self.expect("mu")
        self.skip_whitespace()
        rec_var = self.parse_recursion_variable()
        self.expect(".")
        self.skip_whitespace()
        remaining = self.parse()
        return MuFormula(rec_var, remaining)

    def parse_nu_formula(self) -> NuFormula:
        self.expect("nu")
        self.skip_whitespace()
        rec_var = self.parse_recursion_variable()
        self.expect(".")
        self.skip_whitespace()
        remaining = self.parse()
        return NuFormula(rec_var, remaining)

    def parse_box_formula(self) -> BoxFormula:
        self.expect("[")
        label = ""
        while self.get_char() != ']':
            label += self.get_char()
            self.index += 1
        self.expect("]")
        self.skip_whitespace()
        remaining = self.parse()
        return BoxFormula(label, remaining)

    def parse_diamond_formula(self) -> DiamondFormula:
        self.expect("<")
        label = ""
        while self.get_char() != '>':
            label += self.get_char()
            self.index += 1
        self.expect(">")
        self.skip_whitespace()
        remaining = self.parse()
        return DiamondFormula(label, remaining)
