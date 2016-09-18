#!/usr/bin/env python3
from decimal import Decimal

cash = 0

with open('cash.md') as f:
    state = "begin"
    for line in f:
        fields = line.split('|')
        if state == "begin":
            if len(fields) == 8:
                state = "head"
        elif state == "head":
            if line.startswith('-'):
                state = "head"
            else:
                state = "body"
        elif state == "body":
            if fields[4].strip() == '现金':
                cash += Decimal(fields[6].strip())
            elif fields[3].strip() == '现金':
                cash -= Decimal(fields[6].strip())

print("剩余现金: {:.2f}".format(cash))

# vim: ts=4 sw=4 sts=4 expandtab
