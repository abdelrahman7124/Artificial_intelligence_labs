class TreeNode:
    def __init__(self, kind, move=None):
        self.kind = kind        
        self.move = move        
        self.value = None
        self.children = []
        self.pruned = []        


def print_tree(node, prefix="", is_last=True, is_root=True):
    text = f"{node.kind}  value={node.value}"
    if node.move is not None:
        text = f"col {node.move}: " + text
    if node.pruned:
        text += f"  PRUNED {node.pruned}"

    if is_root:
        print(text)
    else:
        print(prefix + ("|__ " if is_last else "|-- ") + text)
        prefix += "    " if is_last else "|   "

    for i, child in enumerate(node.children):
        print_tree(child, prefix, i == len(node.children) - 1, False)