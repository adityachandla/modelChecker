from fixpoint_tree import *
import query

def nested(formula: query.Formula) -> int:
    "computes the nested depth"
    match formula:
        case query.TrueLiteral() | query.FalseLiteral():
            return 0
        case query.LogicFormula(left, right, _):
            l_depth = nested(left)
            r_depth = nested(right)
            return max(l_depth, r_depth)
        case query.DiamondFormula(l, f) | query.BoxFormula(l, f):
            return nested(f)
        case query.MuFormula(var, f) | query.NuFormula(var, f):
            return 1 + nested(f)
        case query.RecursionVariable(name):
            return 0

def alternation_depth(formula: query.Formula) -> int:
    match formula:
        case query.TrueLiteral() | query.FalseLiteral():
            return 0
        case query.LogicFormula(left, right, _):
            l_depth = alternation_depth(left)
            r_depth = alternation_depth(right)
            return max(l_depth, r_depth)
        case query.DiamondFormula(l, f) | query.BoxFormula(l, f):
            return alternation_depth(f)
        case query.MuFormula(var, formula):
            depth = max(1, alternation_depth(formula))
            subformulas = enumerate_subformulas_of_type(formula, "max")
            # It is not strictly necessary to check all as the first one
            # will have the greatest height but we would have to write
            # another function to find the largest nu.
            for f in subformulas:
                depth = max(depth, alternation_depth(f)+1)
            return depth
        case query.NuFormula(var, formula):
            depth = max(1, alternation_depth(formula))
            subformulas = enumerate_subformulas_of_type(formula, "min")
            for f in subformulas:
                depth = max(depth, alternation_depth(f)+1)
            return depth
        case query.RecursionVariable(name):
            return 0

def dependent_alternation_depth(formula: query.Formula) -> int:
    "Another try at computing dependent alternation depth"
    "Based on formula on slide 19"
    match formula:
        case query.TrueLiteral() | query.FalseLiteral():
            return 0
        case query.LogicFormula(left, right, _):
            l_depth = dependent_alternation_depth(left)
            r_depth = dependent_alternation_depth(right)
            return max(l_depth, r_depth)
        case query.DiamondFormula(l, f) | query.BoxFormula(l, f):
            return dependent_alternation_depth(f)
        case query.MuFormula(var, formula):
            depth = dependent_alternation_depth(formula)
            subformulas = enumerate_subformulas_of_type(formula, "max")
            for f in subformulas:
                if formula_contains_variable(f, var):
                    depth = max(depth, dependent_alternation_depth(f)+1)
            return depth
        case query.NuFormula(var, formula):
            depth = max(1, dependent_alternation_depth(formula))
            subformulas = enumerate_subformulas_of_type(formula, "min")
            for f in subformulas:
                if formula_contains_variable(f, var):
                    depth = max(depth, dependent_alternation_depth(f)+1)
            return depth
        case query.RecursionVariable(name):
            return 0

def formula_contains_variable(f: query.Formula, var: query.RecursionVariable) -> bool:
    "Checks if a formula contains a particular variable"
    match f:
        case query.TrueLiteral() | query.FalseLiteral():
            return False
        case query.LogicFormula(left, right, _):
            return formula_contains_variable(left, var) or \
                    formula_contains_variable(right,var)
        case query.DiamondFormula(l, formula) | query.BoxFormula(l, formula):
            return formula_contains_variable(formula, var)
        case query.MuFormula(var, formula) | query.NuFormula(var, formula):
            return formula_contains_variable(formula, var)
        case query.RecursionVariable(name):
            return name == var.name

def enumerate_subformulas_of_type(formula: query.Formula, fp_type: str) -> list[query.Formula]:
    "Returns a list of all subformulas of type type min/max in the main formula"
    match formula:
        case query.TrueLiteral() | query.FalseLiteral():
            return []
        case query.LogicFormula(left, right, _):
            l = enumerate_subformulas_of_type(left, fp_type)
            r = enumerate_subformulas_of_type(right, fp_type)
            return [*l,*r]
        case query.DiamondFormula(l, f) | query.BoxFormula(l, f):
            return enumerate_subformulas_of_type(f, fp_type)
        case query.MuFormula(var, formula):
            l = []
            if fp_type == "min":
                l.append(query.MuFormula(var, formula))
            l.extend(enumerate_subformulas_of_type(formula, fp_type))
            return l
        case query.NuFormula(var, formula):
            l = []
            if fp_type == "max":
                l.append(query.NuFormula(var,formula))
            l.extend(enumerate_subformulas_of_type(formula, fp_type))
            return l
        case query.RecursionVariable(name):
            return []
    
# Test case 1 from slides
formula = "(mu X. nu Y. (X || Y) && mu A. mu B. (A && mu C. C))"
parser = query.Parser(formula)
res = parser.parse()
print("Nested: ", nested(res))
print("Alternation: ", alternation_depth(res))
print("Dependent: ", dependent_alternation_depth(res))

print()
# Test case 1 modified from slides
formula = "(mu X. nu Y. (X || Y) && mu A. mu B. (A && mu C. mu K. C))"
parser = query.Parser(formula)
res = parser.parse()
print("Nested: ", nested(res))
print("Alternation: ", alternation_depth(res))
print("Dependent: ", dependent_alternation_depth(res))

print()

# Test case 2 from slides
formula = "(mu X. nu Y. (X || Y) && mu A. nu B. (A && mu C. C))"
parser = query.Parser(formula)
res = parser.parse()
print("Nested: ", nested(res))
print("Alternation: ", alternation_depth(res))
print("Dependent: ", dependent_alternation_depth(res))
