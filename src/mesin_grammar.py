# Global variabel (kamus rule) untuk menyimpan semua rule
KAMUS_RULE = {}


def baca_grammar(grammar_file):
    with open(grammar_file) as cfg:
        lines = cfg.readlines()
    return [x.replace("->", "").split() for x in lines]


def tambah_rule(rule):

    global KAMUS_RULE

    if rule[0] not in KAMUS_RULE:
        KAMUS_RULE[rule[0]] = []
    KAMUS_RULE[rule[0]].append(rule[1:])


def konversi_grammar(grammar):

    global KAMUS_RULE
    unit_productions, hasil = [], []
    hasil_append = hasil.append
    index = 0

    for rule in grammar:
        rule_baru = []
        if len(rule) == 2 and rule[1][0] != "'":
            unit_productions.append(rule)
            tambah_rule(rule)
            continue
        elif len(rule) > 2:
            terminals = [(item, i) for i, item in enumerate(rule) if item[0] == "'"]
            if terminals:
                for item in terminals:
                    rule[item[1]] = f"{rule[0]}{str(index)}"
                    rule_baru += [f"{rule[0]}{str(index)}", item[0]]
                index += 1
            while len(rule) > 3:
                rule_baru += [f"{rule[0]}{str(index)}", rule[1], rule[2]]
                rule = [rule[0]] + [f"{rule[0]}{str(index)}"] + rule[3:]
                index += 1
        tambah_rule(rule)
        hasil_append(rule)
        if rule_baru:
            hasil_append(rule_baru)
    while unit_productions:
        rule = unit_productions.pop()
        if rule[1] in KAMUS_RULE:
            for item in KAMUS_RULE[rule[1]]:
                rule_baru = [rule[0]] + item
                if len(rule_baru) > 2 or rule_baru[1][0] == "'":
                    hasil_append(rule_baru)
                else:
                    unit_productions.append(rule_baru)
                tambah_rule(rule_baru)
    return hasil
