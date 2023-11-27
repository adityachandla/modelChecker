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

def parse_query(filepath: str) -> Formula:
    with open(filepath, 'r') as formula_file:
        formula_string = formula_file.read().strip()
    parser = Parser(formula_string)
    return parser.parse(formula_string)

class Parser:
    def __init__(self, formula_str: str):
        self.formula_str = formula_str
        self.index = 0

    def get_char(self) -> str:
        return self.formula_str[self.index]
    
    def expect(s: str):
        self.index += len(s)

    def skip_whitespace(self):
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

    def parse_false_literal(self) -> TrueLiteral:
        self.expect("true")
        self.skip_whitespace()
        return FalseLiteral()

    def parse_recursion_variable(self) -> RecursionVariable:
        name = get_char()
        self.expect(name)
        var = RecursionVariable(name)
        self.skip_whitespace()
        return var

    def parse_logic_formula(self) -> LogicFormula:
        """
        This method deviates from the provided algorithm.
        """
        self.expect("(")
        self.skip_whitespace()
        first = self.parse()
        self.skip_whitespace()
        andOperator = self.get_char() == '&'
        self.expect("&&") # Or ||
        self.skip_whitespace()
        second = self.parse()
        self.skip_whitespace()
        self.expect(")")
        self.skip_whitespace()
        return LogicFormula(first, second, andOperator)

    ## TODO
    def parse_mu_formula(self) -> MuFormula:
        pass

    def parse_nu_formula(self) -> MuFormula:
        pass

    def parse_box_formula(self) -> MuFormula:
        pass

    def parse_diamond_formula(self) -> MuFormula:
        pass

