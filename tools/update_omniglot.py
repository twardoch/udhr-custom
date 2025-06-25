#!/usr/bin/env python3
""" """

__version__ = "0.0.1"

from collections import OrderedDict

import notodata.db as db

from yaplon import reader, writer

with open("udhr-omniglot.yaml", encoding="utf-8") as f:
    udhrs_omni = reader.yaml(f)
udhrs = OrderedDict()


def get_code(name):
    code = None
    rec = db.lang_name_lookup.get(name)
    if rec:
        code = db.langs_list[rec]["full"]
    print(name, code)
    return code


for k, v in udhrs_omni.items():
    code = None
    names = k.split()
    code = get_code(names[0])
    if not code:
        if len(names) > 1:
            code = get_code(names[0])
            if not code:
                code = get_code(names[1].lstrip("(").rstrip(")"))
    if code:
        udhrs[code + " /// " + k] = v
    else:
        udhrs["_ " + k] = v

with open("udhr-omniglot-codes.yaml", "w", encoding="utf-8") as f:
    writer.yaml(udhrs, f, mini=False)
