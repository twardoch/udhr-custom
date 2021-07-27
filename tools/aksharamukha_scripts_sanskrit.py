#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from yaplon import reader
with open('aksharamukha-scripts.yml', 'r', encoding='utf-8') as f:
    aksh = reader.yaml(f)

for k, v in aksh.items():
    if not v.get('sanskrit', False):
        if not v.get('skip', False):
            print(v['script'])
