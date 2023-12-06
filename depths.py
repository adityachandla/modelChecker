from fixpoint_tree import *
import query

class ComputeDepths:
    def __init__(self, tree):
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

        # Start depth calculation from the root node
        root_node = self.tree.label
        root_label = min_max_dict[root_node]
        alternate_depth = dfs(root_node, 1, root_label)
        return alternate_depth

    def d_alternate(self):
        dependent_depth = 0

        return dependent_depth
    
formula = "nu X. (mu Y. Y && (mu Z. Z || nu Q. (nu V. Q && mu T. T)))"
parser = query.Parser(formula)
res = parser.parse()
tree = create_tree(res)

compute_depths = ComputeDepths(tree)
print(compute_depths.nested())
print(compute_depths.alternate())