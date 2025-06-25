#!/usr/bin/env python3

from collections import OrderedDict

from yaplon import reader

with open("udhr-art1-omniglot7.yaml", encoding="utf-8") as f:
    data = reader.yaml(f)

dupes = OrderedDict()
for text, v in data.items():
    code = v.get("lang_opt", v.get("lang_full", None))
    if code:
        dupes[code] = dupes.get(code, 0) + 1

for code, v in dupes.items():
    if v > 1:
        print(code)

print(len(data.keys()))
