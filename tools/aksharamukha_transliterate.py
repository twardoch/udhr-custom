#!/usr/bin/env python3
""" """

import copy
import html
from collections import OrderedDict
from pathlib import Path

import notodata.db as db
from aksharamukha import transliterate
from lxml import etree

from yaplon import reader

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

in_docs = {
    "udhr_san.xml": {"parent": "Deva", "aks": "Devanagari"},
    "udhr_mar.xml": {"parent": "Deva", "aks": "Devanagari", "to": ["Modi"]},
}

skip_scripts = [
    "Adlm",
    "Arab",
    "Armn",
    "Beng",
    "Cakm",
    "Cans",
    "Cher",
    "Cyrl",
    "Deva",
    "Ethi",
    "Gran",
    "Grek",
    "Gujr",
    "Guru",
    "Hang",
    "Hani",
    "Hans",
    "Hant",
    "Hebr",
    "Java",
    "Jpan",
    "Khmr",
    "Knda",
    "Kore",
    "Lana",
    "Laoo",
    "Latn",
    "Mlym",
    "Mymr",
    "Sylo",
    "Syrc",
    "Taml",
    "Tavt",
    "Telu",
    "Tfng",
    "Thaa",
    "Thai",
    "Tibt",
    "Vaii",
    "Yiii",
    "Zzzz",
    "Hira",
    "Kana",
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
        self.init_ak()

    def init_ak(self):
        with open("aksharamukha-scripts.yml") as f:
            self.ak_scripts_all = reader.yaml(f)
        for k, v in self.ak_scripts_all.items():
            if v["script"] not in skip_scripts:
                self.ak_scripts[k] = v
        for k, v in self.ak_scripts.items():
            script_name = db.norm_scripts[v["script"]]["name"]
            self.ak_scripts[k]["script_name"] = script_name
            self.ak_scripts[k]["language_system"] = script_name.replace(
                "(", "/ "
            ).replace(")", "")
            self.ak_scripts[k]["direction"] = directions[
                db.norm_scripts[v["script"]]["direction"]
            ]
            if "post_options" not in self.ak_scripts[k].keys():
                self.ak_scripts[k]["post_options"] = []
            # if 'parent' not in self.ak_scripts[k].keys():
            if True:  # For now, always use Devanagari because there is a problem in the san_gran UDHR
                self.ak_scripts[k]["parent"] = "Deva"
            if "lang" in self.ak_scripts[k].keys():
                lang_i = db.lang_lookup.get(self.ak_scripts[k]["lang"], -1)
                if lang_i > -1:
                    lang_name = db.langs_list[lang_i]["name"]
                    self.ak_scripts[k]["lang_name"] = lang_name
                    self.ak_scripts[k]["language_system"] += f", {lang_name} convention"

    def convert_docs(self):
        for k, v in in_docs.items():
            self.convert_doc(k, v["parent"], v["aks"], v.get("to", None))
        indexes_txt = "\n".join(self.index)
        index_txt = f"""<?xml version="1.0" encoding="UTF-8"?>

<udhrs>
{indexes_txt}
</udhrs>"""
        with open(
            Path(out_folder, "index_aksharamukha.xml"), "w", encoding="utf-8"
        ) as index_file:
            index_file.write(index_txt)

    def convert_doc(self, in_file_name, parent, from_aks, to_akss=None):
        self.open(in_file_name)
        do_convert = False
        for to_aks, ak in self.ak_scripts.items():
            if ak.get("parent", None) == parent:
                do_convert = True
            if to_akss and to_aks not in to_akss:
                do_convert = False
            if ak.get("skip"):
                do_convert = False
            if do_convert:
                self.convert_xml(from_aks, to_aks, ak)
                self.save()

    def convert_el(self, text, from_aks, to_aks, ak):
        return transliterate.process(
            from_aks,
            to_aks,
            html.unescape(text.strip()),
            nativize=ak.get("nativize", True),
            pre_options=[],
            post_options=ak["post_options"],
        )

    def convert_xml(self, from_aks, to_aks, ak):
        self.tree = copy.deepcopy(self.oldtree)
        self.root = self.tree.getroot()
        ws = ak.get("lang", None)
        ws_suf = ""
        if ws:
            ws_suf = f"_{ws}"
        to_script = ak["script"]
        self.udhr_key = f"{self.lang}_{to_script.lower()}{ws_suf}"
        self.out_file_name = f"udhr_{self.udhr_key}.xml"
        self.udhr_bcp47 = f"{self.xml_lang_base}-{to_script}"
        self.root.attrib["{http://www.w3.org/XML/1998/namespace}lang"] = self.udhr_bcp47
        self.root.attrib["key"] = self.udhr_key
        self.udhr_name = f"{self.lang_name} ({ak['language_system']})"
        self.root.attrib["n"] = self.udhr_name
        self.root.attrib["dir"] = ak["direction"]
        self.root.attrib["iso15924"] = ak["script"]
        for el in self.root.iter():
            el.text = self.convert_el(el.text, from_aks, to_aks, ak)
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
