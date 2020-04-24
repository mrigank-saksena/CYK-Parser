def main():
    # Let's first read in the file so we can pre-process the data.
    filename = input("Please enter the name of the text file specifying a CFG in CNF: ")
    rules = open(filename, "r").read().splitlines()

    # Now let's aggregate all the rules into a list
    all_rules = []
    for rule in rules:
        rule = rule.split()
        rule.remove('-->')  # We'll ignore the "-->" in each rule
        all_rules.append(rule)

    while True:
        # Next, we'll prompt the user to input a sentence and tokenize the sentence if they don't input "quit"
        sentence = input("Please either input a sentence or type 'quit' to exit: ")
        if sentence == "quit":
            exit(0)
        else:
            tokens = sentence.split()

        parse_table = [[[] for i in range(len(tokens) - j)] for j in range(len(tokens))]  # Initial CYK Parse Table

        # Here we'll start populating the parse table
        i = 0
        for token in tokens:
            for rule in all_rules:
                if token == rule[1]:
                    # [A --> w] in the form [A --> B C] is [A --> w None] which in list notation is [A, w, None].
                    parse_table[0][i].append([rule[0], token, None])  # We'll include terminals first
            i += 1

        #  Now we'll implement CYK Algorithm. Visit en.wikipedia.org/wiki/CYK_algorithm for more information/pseudocode.
        for l in range(2, len(tokens) + 1):
            for s in range(0, (len(tokens) - l) + 1):
                for p in range(1, l):

                    t1 = parse_table[p - 1][s]
                    t2 = parse_table[l - p - 1][s + p]

                    for rule in all_rules:
                        r1, r2 = [], []
                        for a in t1:
                            if a[0] == rule[1]:
                                r1.append(a)
                        if r1 is not None:
                            for b in t2:
                                if len(rule) == 3 and b[0] == rule[2]:  # For rules in the form A --> B C
                                    r2.append(b)
                            for ln in r1:
                                for rn in r2:
                                    parse_table[l - 1][s].append([rule[0], ln, rn])

        # Now we'll reverse the parse table (we populated the parse table with terminals first).
        nodes = []
        for node in parse_table[-1][0]:
            if node[0] == "S":
                nodes.append(node)

        # Here we'll print the parse.
        if nodes is not None:
            for node in nodes:
                print(output(node))
        else:
            print("NO VALID PARSES")  # If the node list is empty, no valid parses exist.


# This function will be used to output the result in bracketed notation.
def output(node):
    if node[2] is None:
        return "[" + node[0] + " " + node[1] + "]"
    else:
        return "[" + node[0] + " " + output(node[1]) + " " + output(node[2]) + "]"


if __name__ == "__main__":
    main()
