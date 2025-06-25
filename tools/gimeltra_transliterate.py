#!/usr/bin/env python3
""" """

import copy
import html
from collections import OrderedDict
from pathlib import Path

import notodata.db as db
from lxml import etree

from gimeltra import gimeltra

in_folder = Path("..", "data", "udhr")
out_folder = Path("..", "data", "udhr-translit")

directions = {
    "[unspecified]": "ltr",
    "boustrophedon": "ltr",
    "LTR": "ltr",
    "other": "ltr",
    "RTL bidirectional": "rtl",
    "RTL": "ltr",
    "vertical (LTR) and horizontal (LTR)": "ltr",
    "vertical (LTR)": "ltr",
    "vertical (RTL) and horizontal (LTR)": "rtl",
    "vertical (RTL)": "rtl",
}

langs = ["aii"]

in_docs = {
    "udhr_aii.xml": {"script": "Syrc"},
}

do_scripts = [
    "Armi",
    "Brah",
    "Chrs",
    "Egyp",
    "Elym",
    "Hatr",
    "Mani",
    "Narb",
    "Nbat",
    "Palm",
    "Phli",
    "Phlp",
    "Phnx",
    "Prti",
    "Samr",
    "Sarb",
    "Sogd",
    "Sogo",
    "Ugar",
]


class UDHRTransliterator:
    def __init__(self):
        self.in_path = None
        self.oldtree = None
        self.tree = None
        self.oldroot = None
        self.root = None
        self.lang = None
        self.script = None
        self.ak_scripts = OrderedDict()
        self.index = []
        self.tr = gimeltra.Transliterator()
        self.init_ak()

    def init_ak(self):
        # print(db.norm_scripts)
        for k in do_scripts:
            v = db.norm_scripts[k]
            script_name = v["name"]
            self.ak_scripts[k] = OrderedDict()
            self.ak_scripts[k]["script"] = k
            self.ak_scripts[k]["script_name"] = script_name
            self.ak_scripts[k]["language_system"] = script_name.replace(
                "(", "/ "
            ).replace(")", "")
            self.ak_scripts[k]["direction"] = directions[v["direction"]]
            for lang in langs:
                lang_i = db.lang_lookup.get(lang, -1)
                if lang_i > -1:
                    lang_name = db.langs_list[lang_i]["name"]
                    self.ak_scripts[k]["lang_name"] = lang_name
                    self.ak_scripts[k]["language_system"] += f", {lang_name} convention"

    def convert_docs(self):
        for k, v in in_docs.items():
            self.convert_doc(k, v["script"])
        indexes_txt = "\n".join(self.index)
        index_txt = f"""<?xml version="1.0" encoding="UTF-8"?>

<udhrs>
{indexes_txt}
</udhrs>"""
        with open(
            Path(out_folder, "index_gimeltra.xml"), "w", encoding="utf-8"
        ) as index_file:
            index_file.write(index_txt)

    def convert_doc(self, in_file_name, in_script):
        self.open(in_file_name)
        for out_script, ak in self.ak_scripts.items():
            self.convert_xml(in_script, out_script, ak)
            self.save()

    def convert_el(self, text, in_script, out_script):
        return self.tr.tr(html.unescape(text.strip()), sc=in_script, to_sc=out_script)

    def convert_xml(self, in_script, out_script, ak):
        self.tree = copy.deepcopy(self.oldtree)
        self.root = self.tree.getroot()
        to_script = out_script
        self.udhr_key = f"{self.lang}_{to_script.lower()}"
        self.out_file_name = f"udhr_{self.udhr_key}.xml"
        self.udhr_bcp47 = f"{self.xml_lang_base}-{to_script}"
        self.root.attrib["{http://www.w3.org/XML/1998/namespace}lang"] = self.udhr_bcp47
        self.root.attrib["key"] = self.udhr_key
        self.udhr_name = f"{self.lang_name} ({ak['language_system']})"
        self.root.attrib["n"] = self.udhr_name
        self.root.attrib["dir"] = ak["direction"]
        self.root.attrib["iso15924"] = ak["script"]
        for el in self.root.iter():
            el.text = self.convert_el(el.text, in_script, out_script)
        index_rec = f"""
  <udhr f='{self.udhr_key}'                iso639-3='{self.lang}' iso15924='{ak["script"]}'  bcp47='{self.udhr_bcp47}'            dir='{ak["direction"]}' ohchr=''        stage='4' notes='n' loc=''       demo='y' n='{self.udhr_name}'/>
        """
        self.index.append(index_rec)

    def save(self):
        self.tree.write(
            str(Path(out_folder, self.out_file_name)),
            encoding="utf-8",
            xml_declaration=True,
            pretty_print=True,
        )

    def open(self, in_file_name):
        self.in_path = Path(in_folder, in_file_name)
        parser = etree.XMLParser(ns_clean=True)
        with open(self.in_path, encoding="utf-8") as f:
            self.oldtree = etree.parse(f, parser)
        self.oldroot = self.oldtree.getroot()
        self.xml_lang_base = self.oldroot.attrib[
            "{http://www.w3.org/XML/1998/namespace}lang"
        ].split("-")[0]
        self.lang_name = self.oldroot.attrib["n"].split("(")[0].strip()
        self.lang = self.oldroot.attrib.get("iso639-3", None)
        self.script = self.oldroot.attrib.get("iso15924", None)


def main():
    ut = UDHRTransliterator()
    ut.convert_docs()


if __name__ == "__main__":
    main()
