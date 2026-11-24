import tkinter as tk

NODE_W = 70
NODE_H = 38
X_GAP = 27
Y_GAP = 150    
COLORS = {"MAX": "lightgreen", "MIN": "pink", "CHANCE": "lightblue", "LEAF": "lightgray"}


class TreeGui:
    def __init__(self, parent, root_node, levels=2):
        self.window = tk.Toplevel(parent)
        self.window.title("Search tree")
        self.levels = levels          

        self.window.state("zoomed")              
        

        self.canvas = tk.Canvas(self.window, bg="white")
        x_bar = tk.Scrollbar(self.window, orient="horizontal", command=self.canvas.xview)
        y_bar = tk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=x_bar.set, yscrollcommand=y_bar.set)
        x_bar.pack(side="bottom", fill="x")
        y_bar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        if root_node is None:
            self.canvas.create_text(20, 20, anchor="nw", text="No tree yet - let the AI play first.")
            return

        self.next_x = 50                       
        self.draw(root_node, 0)
        x1, y1, x2, y2 = self.canvas.bbox("all")
        self.canvas.configure(scrollregion=(x1 - 20, y1 - 20, x2 + 20, y2 + 20))

    def draw(self, node, depth):
        y = 40 + depth * (NODE_H + Y_GAP)
        children = node.children if depth < self.levels else []

        if not children:
            x = self.next_x
            self.next_x += NODE_W + X_GAP
        else:
            child_xs = [self.draw(child, depth + 1) for child in children]
            x = (child_xs[0] + child_xs[-1]) / 2
            child_y = y + NODE_H + Y_GAP
            for child, cx in zip(children, child_xs):
                self.canvas.create_line(x, y + NODE_H / 2, cx, child_y - NODE_H / 2, fill="gray")
                label = f"c{child.move}"
                if getattr(child, "prob", None) is not None:
                    label += f" p={child.prob}"
                self.canvas.create_text((x + cx) / 2, (y + child_y) / 2, text=label, font=("Arial", 8))

        self.canvas.create_rectangle(x - NODE_W / 2, y - NODE_H / 2, x + NODE_W / 2, y + NODE_H / 2,
                                    fill=COLORS.get(node.kind, "white"))
        self.canvas.create_text(x, y - 14, text=node.kind, font=("Arial", 8, "bold"))
        self.canvas.create_text(x, y, text=str(round(node.value, 2)), font=("Arial", 9))
        if getattr(node, "alpha", None) is not None:
            self.canvas.create_text(x, y + 14, text=f"a={node.alpha}  b={node.beta}", font=("Arial", 7))

        if getattr(node, "pruned", None):
            x_end = x + NODE_W / 2
            y_end = y + NODE_H / 2 + Y_GAP / 2
            self.canvas.create_line(x, y + NODE_H / 2, x_end, y_end, fill="red", dash=(4, 2))
            self.canvas.create_text(x_end + 3, y_end, text="pruned", anchor="w",
                                    font=("Arial", 8, "bold"), fill="red")
        return x