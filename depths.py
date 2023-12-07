from fixpoint_tree import *
import query

class ComputeDepths:
    def __init__(self, formula, tree):
        self.formula = formula
        self.tree = tree
        
    def make_parent_to_child(self, child_to_parent):
        "Creates a reverse dictionary where we map a parent to its children"
        parent_to_child = {}
        for child, parent in child_to_parent.items():
            if parent not in parent_to_child:
                parent_to_child[parent] = []
            parent_to_child[parent].append(child)
        return parent_to_child

    def nested(self):
        "computes the nested depth"
        child_to_parent = create_parent_relation(self.tree) 
        parent_to_child = self.make_parent_to_child(child_to_parent)    
        
        max_depth = 0

        def dfs(node, depth):
        #depth first search
            nonlocal max_depth
            if node not in parent_to_child:
                # Reached leaf node
                max_depth = max(max_depth, depth)
                return
            for child in parent_to_child[node]:
                dfs(child, depth + 1)

        dfs(self.tree.label, 1)  # Start depth calculation from the root

        return max_depth

    def alternate(self):
        "computes the alternation depth"
        child_to_parent = create_parent_relation(self.tree) 
        min_max_dict = create_fixpoint_to_type_relation(self.tree)
        parent_to_child = self.make_parent_to_child(child_to_parent) 
        
        def dfs(node, depth, current_label):
            if node not in parent_to_child:
                # Leaf node reached
                return depth

            max_depth = depth
            children = parent_to_child[node]

            for child in children:
                child_label = min_max_dict[child]
                if child_label != current_label:
                    # Labels alternate, continue exploration
                    child_depth = dfs(child, depth + 1, child_label)
                    max_depth = max(max_depth, child_depth)

            return max_depth

        max_alternate_depth = 0
        
        #start compution of depth from every node, not just root node
        for node in min_max_dict:
            node_label = min_max_dict[node]
            alternate_depth = dfs(node, 1, node_label)
            max_alternate_depth = max(max_alternate_depth, alternate_depth)
        
        return max_alternate_depth

    def make_open_variables_dict(self, formula, dict):
        match formula:
            case query.TrueLiteral() | query.FalseLiteral():
                pass
            case query.LogicFormula(left, right, _):
                self.make_open_variables_dict(left, dict)
                self.make_open_variables_dict(right, dict)
            case query.DiamondFormula(l, f) | query.BoxFormula(l, f):
                self.make_open_variables_dict(f, dict)
            case query.MuFormula(var, formula):
                if var.name not in dict:
                    relation_creator = ResetRelationCreator(formula)
                    open_variables = relation_creator.find_open_variables(formula,{var.name})
                    dict[var.name] = open_variables
                    self.make_open_variables_dict(formula, dict)
            case query.NuFormula(var, formula):
                if var.name not in dict:
                    relation_creator = ResetRelationCreator(formula)
                    open_variables = relation_creator.find_open_variables(formula,{var.name})
                    dict[var.name] = open_variables
                    self.make_open_variables_dict(formula, dict)
            case query.RecursionVariable(name):
                pass
            case _:
                raise AssertionError()
        return dict
        
    def d_alternate(self):
        "computes the dependent alternation depth"
        open_variables_dict = self.make_open_variables_dict(self.formula, {})
        print("final result: ",open_variables_dict)
        child_to_parent = create_parent_relation(self.tree) 
        min_max_dict = create_fixpoint_to_type_relation(self.tree)
        parent_to_child = self.make_parent_to_child(child_to_parent) 
        
        def dfs(node, depth, current_label):
            if node not in parent_to_child:
                # Leaf node reached
                return depth

            max_depth = depth
            max_depth_with_dependency = 0
            children = parent_to_child[node]

            for child in children:
                child_label = min_max_dict[child]
                if child_label != current_label:
                    # Labels alternate, continue exploration
                    if node in open_variables_dict[child]:
                       #only update max depth if the dependency condition is met
                       max_depth_with_dependency = depth+1 
                    child_depth = dfs(child, depth + 1, child_label)
                    max_depth = max(max_depth, child_depth)
                    

            return max_depth_with_dependency

        max_dependent_alternate_depth = 0
        
        #start compution of depth from every node, not just root node
        for node in min_max_dict:
            node_label = min_max_dict[node]
            alternate_depth = dfs(node, 1, node_label)
            max_dependent_alternate_depth = max(max_dependent_alternate_depth, alternate_depth)
        
        return max_dependent_alternate_depth
    
formula = "mu X. (mu Y. (Y && X) && (mu Z. Z || mu Q. (nu V. Q && mu T. T)))"
parser = query.Parser(formula)
res = parser.parse()
tree = create_tree(res)

compute_depths = ComputeDepths(res, tree)
print(compute_depths.nested())
print(compute_depths.alternate())
print(compute_depths.d_alternate())
