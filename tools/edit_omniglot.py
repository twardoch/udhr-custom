#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

__version__ = '0.0.1'

from collections import OrderedDict
import langcodes
from yaplon import reader, writer
with open('udhr-omniglot-codes.yaml', 'r', encoding='utf-8') as f:
    udhrs_omni = reader.yaml(f)

udhrs_omni_reversed = {}

for lang_name_omni, udhr_omni in udhrs_omni.items():
    udhr_text = udhr_omni.get('udhr', '')
    udhr_translit = udhr_omni.get('translit', None)
    udhr_ipa = udhr_omni.get('ipa', None)
    key = udhr_text.strip()
    udhrs_omni_reversed[key] = OrderedDict()
    u = udhrs_omni_reversed[key]
    u['lang'] = lang_name_omni
    u['source'] = 'https://omniglot.com/udhr/'
    if udhr_translit:
        u['translit'] = udhr_translit
    if udhr_ipa:
        u['ipa'] = udhr_ipa

with open('udhr_official_scripts.yaml', 'r', encoding='utf-8') as f:
    udhrs_off = reader.yaml(f)

for udhr_off_key, udhr_off in udhrs_off.items():
    udhr_off_text = udhr_off.get('art1', None)
    udhr_off_code = udhr_off['code']
    if udhr_off_text:
        if udhr_off_text not in udhrs_omni_reversed.keys():
            udhrs_omni_reversed[udhr_off_text] = OrderedDict()
        u = udhrs_omni_reversed[udhr_off_text]
        u['lang'] = udhr_off_code
        u['source'] = 'https://unicode.org/udhr/'
        u['udhr_key'] = udhr_off_key

udhrs_omni_reversed = OrderedDict(sorted(udhrs_omni_reversed.items()))

print(len(udhrs_omni_reversed.keys()))

with open('udhr-art1-omniglot2.yaml', 'w', encoding='utf-8') as f:
    writer.yaml(udhrs_omni_reversed, f, mini=False)
