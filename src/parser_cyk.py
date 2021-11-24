import mesin_grammar

class Node:
    def __init__(self, symbol, child1, child2=None):
        self.symbol = symbol
        self.child1 = child1
        self.child2 = child2

    def __repr__(self):
        return self.symbol


class Parser:

    def __init__(self, fileInput):
        self.tabel_parsing = None
        self.prods = {}
        self.lines = []
        self.grammar = mesin_grammar.konversi_grammar(mesin_grammar.read_grammar("src/grammar/CFG.txt"))

        with open('src/grammar/CNF.txt', 'w') as cnf:
            for item in self.grammar:
                cnf.write("%s\n" % item)

        with open(fileInput, 'r') as inp:
	        self.inputline = [line.strip() for line in inp if line.strip()]
        
        
    def parse(self):
        length = len(self.input)
        self.tabel_parsing = [[[] for x in range(length - y)] for y in range(length)]

        for i, word in enumerate(self.input):
            for rule in self.grammar:
                if f"'{word}'" == rule[1]:
                    self.tabel_parsing[0][i].append(Node(rule[0], word))
        for words_to_consider in range(2, length + 1):
            for starting_cell in range(0, length - words_to_consider + 1):
                for left_size in range(1, words_to_consider):
                    right_size = words_to_consider - left_size

                    left_cell = self.tabel_parsing[left_size - 1][starting_cell]
                    right_cell = self.tabel_parsing[right_size - 1][starting_cell + left_size]

                    for rule in self.grammar:
                        left_nodes = [n for n in left_cell if n.symbol == rule[1]]
                        if left_nodes:
                            right_nodes = [n for n in right_cell if n.symbol == rule[2]]
                            self.tabel_parsing[words_to_consider - 1][starting_cell].extend(
                                [Node(rule[0], left, right) for left in left_nodes for right in right_nodes]
                            )
    
    
    def analisa_syntax(self, fileName):
        with open(fileName, 'r') as inp:
            self.lines = [line.strip() for line in inp if line.strip()]

        incorrect = False
        for i in range(len(self.inputline)):
            self.input = self.inputline[i].split()
            self.parse()
            start_symbol = self.grammar[0][0]
            final_nodes = [n for n in self.tabel_parsing[-1][0] if n.symbol == start_symbol]
            if not final_nodes:
            	print("Syntax error")
            	print (f"  pada line {i+1}\n    {self.lines[i]}")
            	incorrect = True
        if not incorrect:
            print("Accepted")

