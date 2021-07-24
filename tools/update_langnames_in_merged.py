#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from yaplon import reader, writer
import sys
from collections import OrderedDict
import langcodes
from pathlib import Path


inpath = Path(Path(__file__).parent, '..', 'merged', 'udhr-art1-omniglot6.yaml')
outpath = Path(Path(__file__).parent, '..', 'merged', 'udhr-art1-omniglot7.yaml')
updatepath = Path(Path(__file__).parent, 'udhr_art1_r12a.yaml')

with open(inpath, 'r', encoding='utf-8') as f:
    art1 = reader.yaml(f)

lang_scripts = OrderedDict()
langs = OrderedDict()

for text, rec in art1.items():
    if not 'lang_full' in rec.keys():
        rec['lang_full'] = rec['lang']
    lobj = langcodes.Language.get(rec['lang_full'])
    lang = vars(lobj).get('language', None)
    if lang:
        rec['lang'] = lang
    try:
        iso3 = lobj.to_alpha3()
    except LookupError:
        iso3 = db.lang_to_iso_639_3(lang)
    rec['lang_639_3'] = iso3
    script = vars(lobj).get('script', None)
    if script:
        rec['script'] = script
    territory = vars(lobj).get('territory', None)
    if territory:
        rec['territory'] = territory
    variant = vars(lobj).get('private', None)
    if variant:
        rec['variant'] = variant
    lang_scripts[f"{lang}-{script}"] = lang_scripts.get(f"{lang}-{script}", 0) + 1

ambi = set()
for text, rec in art1.items():
    lang = rec.get('lang', '')
    script = rec.get('script', '')
    ambiguous = lang_scripts.get(f"{lang}-{script}", 99)
    if ambiguous > 1:
        rec['lang_opt'] = rec['lang_full']
        ambi.add(rec['lang_full'])
    else:
        rec['lang_opt'] = f"{lang}-{script}"
    lobj = langcodes.Language.get(rec['lang_opt'])
    rec['name_lang'] = lobj.display_name()
    autonym = lobj.autonym()
    if autonym != rec['name_lang']:
        rec['name_autonym'] = autonym

if updatepath:
    with open(updatepath, 'r', encoding='utf-8') as f:
        update = reader.yaml(f)

    for key in update.keys():
        if key in art1:
            update[key].update(art1[key])
        art1[key] = update[key]

for a in sorted(list(ambi)):
    print(a)
with open(outpath, 'w', encoding='utf-8') as f:
    writer.yaml(art1, f)

