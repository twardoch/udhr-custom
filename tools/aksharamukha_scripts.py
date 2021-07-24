#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from yaplon import reader, writer
from collections import OrderedDict

akshara_scripts = sorted(["LaoTham", "LueTham", "KhuenTham", "Mongolian", "TamilExtended", "Mro", "Wancho", "Marchen", "HanifiRohingya", "MasaramGondi", "GunjalaGondi", "Soyombo", "Dogra", "KhomThai", "Ariyaka", "Shan", "KhamtiShan", "Mon", "TaiLaing", "Ahom","Assamese","Avestan","Balinese","BatakKaro","BatakManda","BatakPakpak","BatakToba","BatakSima","Bengali","Brahmi","Bhaiksuki","Buginese","Buhid","Burmese","Chakma","Cham","Devanagari","Grantha","GranthaPandya","Gujarati","Hanunoo","Javanese","Kaithi","Kannada","Kharoshthi","Khmer","Khojki","Khudawadi","Lao","LaoPali","Lepcha","Limbu","Malayalam","Mahajani","MeeteiMayek","Modi","Multani","Newa","OldPersian","Oriya","PhagsPa","Gurmukhi","Ranjana","Rejang","Santali","Saurashtra","Siddham","Sharada","Sinhala","SoraSompeng","Sundanese","SylotiNagri","Tagbanwa","Tagalog","TaiTham","Takri","Tamil","TamilGrantha","TamilBrahmi","Telugu","Thaana","Thai","Tibetan","Tirhuta","Urdu","Vatteluttu","WarangCiti","ZanabazarSquare"])

with open('aksharamukha-scripts.yml', 'r', encoding='utf-8') as f:
    akshara_script_data = reader.yaml(f)

for script in akshara_scripts:
    if script not in akshara_script_data:
        akshara_script_data[script] = OrderedDict()
        akshara_script_data[script]['script'] = 'Zzzz'

with open('aksharamukha-scripts2.yml', 'w', encoding='utf-8') as f:
    writer.yaml(akshara_script_data, f)
