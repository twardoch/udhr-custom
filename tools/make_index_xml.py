#!/usr/bin/env python3
""" """

from collections import OrderedDict
from pathlib import Path

from lxml import etree

in_folder = Path(Path(__file__).parent, "..", "data", "udhr-manual")
out_folder = Path(Path(__file__).parent, "..", "data", "udhr-manual")


class UDHRIndexer:
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
        self.in_docs = Path(in_folder).glob("**/udhr_*.xml")

    def index_all(self):
        for p in self.in_docs:
            self.open(p)
        indexes_txt = "\n".join(self.index)
        index_txt = f"""<?xml version="1.0" encoding="UTF-8"?>

<udhrs>
{indexes_txt}
</udhrs>"""
        with open(Path(out_folder, "index.xml"), "w", encoding="utf-8") as index_file:
            index_file.write(index_txt)

    def open(self, in_file_name):
        self.in_path = Path(in_folder, in_file_name)
        parser = etree.XMLParser(ns_clean=True)
        with open(self.in_path, encoding="utf-8") as f:
            self.tree = etree.parse(f, parser)
        self.root = self.tree.getroot()
        at = self.root.attrib
        index_rec = f"""
  <udhr f='{at["key"]}' iso639-3='{at["iso639-3"]}' iso15924='{at["iso15924"]}'  bcp47='{at["{http://www.w3.org/XML/1998/namespace}lang"]}'   dir='{at["dir"]}' ohchr=''  stage='4' notes='n' loc=''       demo='y' n='{at["n"]}'/>"""
        self.index.append(index_rec)


def main():
    ut = UDHRIndexer()
    ut.index_all()


if __name__ == "__main__":
    main()
