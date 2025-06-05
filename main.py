import sys
import networkx as nx
import matplotlib.pyplot as plt

from Grammar import Grammar
from LL1Parser import LL1Parser

def tokenize(input_str, terminals):
    tokens = []
    i = 0
    length = len(input_str)
    sorted_terms = sorted(terminals, key=lambda s: -len(s))
    while i < length:
        if input_str[i].isspace():
            i += 1
            continue
        matched = False
        for t in sorted_terms:
            t_len = len(t)
            if i + t_len <= length and input_str[i:i + t_len] == t:
                tokens.append(t)
                i += t_len
                matched = True
                break
        if not matched:
            print(f"⚠️ نمادِ ناشناس در موقعیت {i} («{input_str[i]}») نادیده گرفته شد.")
            i += 1
    return tokens

class Node:
    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []

    def add_children(self, child_nodes):
        self.children = child_nodes

def draw_parse_tree(root_node):
    G = nx.DiGraph()
    pos = {}

    def add_to_graph(node, parent_key=None, x=0.0, y=0.0, dx=1.0):
        node_key = f"{node.symbol}_{id(node)}"
        G.add_node(node_key)
        pos[node_key] = (x, y)
        if parent_key is not None:
            G.add_edge(parent_key, node_key)
        n_children = len(node.children)
        if n_children > 0:
            total_width = dx * (n_children - 1)
            start_x = x - total_width / 2
            for i, child in enumerate(node.children):
                child_x = start_x + i * dx
                child_y = y - 1
                add_to_graph(child, node_key, child_x, child_y, dx / 2)

    add_to_graph(root_node)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=False, arrows=False)
    for node_key, (x, y) in pos.items():
        symbol = node_key.rsplit("_", 1)[0]
        plt.text(x, y, s=symbol,
                 horizontalalignment='center',
                 verticalalignment='center',
                 bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'),
                 fontsize=10)
    plt.axis('off')
    plt.title("Parse Tree")
    plt.show()

if __name__ == "__main__":
    grammar = Grammar()
    grammar.load_from_file("grammar.txt")
    print("=== گرامر بارگذاری شده ===")
    grammar.display()

    parser = LL1Parser(grammar)
    parser.build_parse_table()
    print("\n=== LL(1) Parse Table ===")
    parser.display_parse_table()

    dpda = parser.build_dpda_transitions()
    print("\n=== نمایش DPDA ساخته‌شده ===")
    dpda.display()

    if len(sys.argv) > 1:
        raw_input = sys.argv[1]
    else:
        raw_input = input("\nعبارت را وارد کنید: ")

    tokens = tokenize(raw_input, grammar.terminals)
    print(f"\nTokens: {tokens}")

    accepted, root_node = dpda.process_input(tokens)
    if accepted:
        print(f"\n✅ رشته‌ی '{raw_input}' پذیرفته شد.")
        dpda.parse_tree_root = root_node
        draw_parse_tree(root_node)

        choice = input("\nآیا می‌خواهید یک نماد را تغییر نام دهید؟ (yes/no): ").strip().lower()
        if choice == "yes":
            old = input("نماد فعلی: ").strip()
            new = input("نام جدید: ").strip()
            dpda.rename_symbol_in_tree(old, new)
            print("\n📌 درخت تغییرنام‌یافته:")
            draw_parse_tree(dpda.parse_tree_root)
    else:
        print(f"❌ رشته‌ی '{raw_input}' پذیرفته نشد.")