#!/bin/python3

# Runs standard input through a part-of-speech tagger, then
# translates to Shavian. This resolves most heteronyms, but
# do still check the output for @ signs and fix them by hand.

# Each line of the dictionary consists of an English word, a space,
# and the Shavian transcription thereof. Comments are not allowed.
# Special notations are:
#
# ^word		word is a prefix
# $word		word is a suffix
# Word		word must always receive a naming dot
# word.		word must never receive a naming dot
# word_VB	word must be shaved this way when tagged as a verb
#
# A period in the Shavian word means that it takes no affixes.
# Use this for foreign words that don't take English affixes.
# Scoring problems should be addressed by adding longer morphemes.
#
# Words are matched case-sensitive when possible, thereby
# distinguishing "WHO" from "who" and "Nice" from "nice".
#
# shaw.py does not care about the order of dictionary entries.
# shaw.c requires all prefixes, then all suffixes, then all roots
# sorted case-insensitive, with underscores sorted before letters.

import sys
from html.parser import HTMLParser

import nltk

apostrophe = "'"  # whatever you want for apostrophe, e.g. "’" or ""
htags = {}
tokens = []
script = 0


def notrans(str):
    global htags
    tok = len(tokens)
    if tok in htags:
        htags[tok] += str
    else:
        htags[tok] = str


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global script
        out = "<" + tag
        for at in attrs:
            if at[0] == "charset":
                at = ("charset", "UTF-8")
            if at[0] == "content":
                at = ("content", "text/html; charset=UTF-8")
            out += " " + at[0]
            if type(at[1]) == str:
                out += '="' + at[1] + '"'
        out += ">"
        if tag == "noscript" or tag == "script" or tag == "style":
            script = 1
        notrans(out)

    def handle_endtag(self, tag):
        global script
        notrans("</" + tag + ">")
        if tag == "noscript" or tag == "script" or tag == "style":
            script = 0

    def handle_data(self, data):
        global script, tokens
        if script:
            notrans(data)
        else:
            tokens += nltk.word_tokenize(data)


# break a string into alphabetic and non-alphabetic parts
# an apostrophe or period is "alphabetic" only if it's between two letters
def alpha_split(str):
    list = []
    prev = -1
    for i in range(len(str)):
        alpha = (
            str[i].isalpha()
            or "'.".find(str[i]) + 1
            and i > 0
            and i < len(str) - 1
            and str[i - 1].isalpha()
            and str[i + 1].isalpha()
        )
        if alpha == prev:
            list[-1] += str[i]
        else:
            list += str[i]
        prev = alpha
    return list


# Search all the ways a word might appear in the dictionary
def lookup(word, pos):
    ret = ""
    low = word.lower()
    pos = "_" + pos
    for look in [
        low + pos,
        low + pos[:3],
        word,
        word + ".",
        low,
        low + ".",
        low + "_NN",
        low + "_NNS",
        word[0].upper() + word[1:],
        word[0].upper() + low[1:],
        word.upper(),
    ]:
        if look in dict:
            ret = dict[look]
            if ret.find(".") + 1:
                ret = ret.replace(".", "") if (word == whole) else ""
            if not ret:
                continue
            if (
                (word[0].isupper() or look[0].isupper())
                and (look[-1] != "." or word != whole)
                and ret[-1] > "z"
            ):
                ret = "·" + ret
            break
    return ret


def suffix_split(inp, pos, adj):
    long = len(inp)
    root = lookup(inp, pos)
    if root:
        return ((long + adj) ** 2, root)
    low = inp.lower()
    best = (0, "")
    for split in range(max(long - 9, 2), long):
        suff = "$" + low[split:]
        if suff not in dict or low[split - 1 : split + 1] in ["ee", "ss"]:
            continue
        if low[split:] == "ess" and low[split - 2] == low[split - 1]:
            continue
        if low[split:] == "ry" and "aeiouf".find(low[split - 1]) + 1:
            continue
        if low[split:] == "r" and "aeiou".find(low[split - 1]) + 1:
            continue
        if (
            low[split:] == "n"
            and "eio".find(low[split - 1]) + 1
            and low[split - 2] != low[split - 1]
        ):
            continue
        suff = dict[suff]
        for pess in range(2):
            if pess:
                word = inp[:split]
            elif low[split - 1] == "i" and low[split] != "i" and low[split:] != "s":
                word = inp[: split - 1] + "y"
            elif "aeioy".find(low[split]) + 1 and not "aeio".find(low[split - 1]) + 1:
                if (
                    low[split - 1] == low[split - 2]
                    and not "sh".find(low[split - 1]) + 1
                ):
                    word = inp[: split - 1]
                elif (
                    "cghlsuvz".find(low[split - 1]) + 1
                    or low[split] == "e"
                    or "aeiousy".find(low[split - 2]) + 1
                ) and ("cg".find(low[split - 1]) < 0 or "aou".find(low[split]) < 0):
                    word = inp[:split] + "e"
                else:
                    continue
            elif low[split - 2 : split] == "dg":
                word = inp[:split] + "e"
            else:
                continue
            root = suffix_split(word, "UNK", split - len(word))
            score = (long - split + adj) ** 2 + root[0] if root[0] else 0
            if score <= best[0]:
                continue
            root = root[1]
            if root[-2:] == "𐑩𐑤" and "𐑦𐑩𐑼".find(suff[0]) + 1 and word[-2:] == "le":
                root = root[:-2] + "𐑤"
            if root[-3:] == "𐑟𐑩𐑥" and suff not in ["𐑛", "𐑟", "𐑦𐑙"]:
                root = root[:-3] + "𐑟𐑥"
            mid = root[-1] + suff[0]
            if mid == "𐑦𐑩":
                mid = "𐑾"
            if mid == "𐑦𐑼":
                mid = "𐑽"
            if mid == "𐑤𐑤" and len(suff) < 3:
                mid = "𐑤"
            best = (score, root[:-1] + mid + suff[1:])
    if len(best[1]) > 1:
        word = best[1][:-1]
        end = best[1][-1]
        edz = "𐑛𐑟".find(end) + 1
        if ["", "𐑑𐑛", "𐑕𐑖𐑗𐑟𐑠𐑡"][edz].find(word[-1]) + 1:
            word += "𐑩"
        if edz and word[-1] < "𐑘":
            end = chr(ord(end) - 10)
        word += end
        if word[-4:] == "𐑒𐑩𐑤𐑦" and "𐑦𐑩".find(word[-5]) + 1:
            word = word[:-4] + "𐑒𐑤𐑦"
        best = (best[0], word)
    return best


def prefix_split(word, pos, ms):
    best = suffix_split(word, pos, 0)
    split = min(len(word) - 2, 7)
    for split in range(split, ms, -1):
        pref = "^" + word[:split].lower()
        if pref not in dict:
            continue
        root = prefix_split(word[split:], pos, 1)
        score = split**2 + root[0] if root[0] else 0
        if score > best[0]:
            dot = "·" if word[0].isupper() else ""
            pref = dict[pref]
            if pref[-1] == root[1][0] and pref[-2] == "𐑦" and "𐑤𐑥𐑮𐑯".find(pref[-1]) + 1:
                pref = pref[:-1]
            best = (score, pref + dot + root[1])
    return best


# These are specific to the way NLTK breaks up formal and informal contractions,
# so they don't belong in dave.dict:
cont = {
    "'s": "'𐑟",
    "'d": "'𐑛",
    "'ll": "'𐑤",
    "'m": "'𐑥",
    "'re": "'𐑼",
    "'ve": "'𐑝",
    "n't": "𐑯'𐑑",
}
dict = {
    "ai": "𐑱",
    "ca": "𐑒𐑭.",
    "gim": "𐑜𐑦𐑥",
    "lem": "𐑤𐑧𐑥",
    "na": "𐑯𐑩",
    "ta": "𐑑𐑩.",
    "wo": "𐑢𐑴",
}

if len(sys.argv) < 2:
    print("Usage:", sys.argv[0], "file1.dict file2.dict ...")
    exit()

at = 1
for fname in sys.argv[1:]:
    with open(fname) as df:
        for line in df:
            word = line.split()
            if at and word[0] in dict:
                dict[word[0]] += "@" + word[1]
            else:
                dict[word[0]] = word[1]
    at = 0

text = sys.stdin.read()
text = text.replace("’", "'").replace("&#8217;", "'").replace("&rsquo;", "'")
text = text.replace("'s", " 's").replace("'S", " 's")
if text.lower().find("<html") == -1:
    text = text.replace("\n\n", " PARABREAK. ")

parser = MyHTMLParser()
parser.feed(text)

tags = nltk.pos_tag(tokens) + [(" ", " ")]
out = ""
prev = ("", ".")
tok = 0
initial = True
for token in tags:
    if tok in htags:
        out += htags[tok]
    tok += 1
    #  print (token)
    if token[1] == "." or token[1] == ":" or token[1] == "``" or token[0] == "“":
        initial = True
    if token[0] == "PARABREAK" or prev[0] == "PARABREAK":
        out += "\n"
        prev = token
        continue
    low = token[0].lower()
    if low in cont:
        apos = cont[low]
        if low == "'s":
            if "𐑐𐑑𐑒𐑓𐑔".find(out[-1]) + 1:
                apos = "'𐑕"
            if "𐑕𐑖𐑗𐑟𐑠𐑡".find(out[-1]) + 1:
                apos = "'𐑩𐑟"
        if prev[0] == "do" and low == "n't":
            out = out[:-1] + "𐑴"
        out += apos.replace("'", apostrophe)
        continue
    befto = {"have": "𐑨𐑓", "has": "𐑨𐑕", "used": "𐑕𐑑", "unused": "𐑕𐑑", "supposed": "𐑕𐑑"}
    if prev[0] in befto and low == "to":  # If "to" changes the meaning of the preceding
        i = out.rfind(tran[-2:])  # word, it also changes the pronunciation.
        out = out[:i] + befto[prev[0]] + out[i + 2 :]
    if prev[0] == "lives" and low == "matter":
        out = out[:-4] + "𐑤𐑲𐑝𐑟"
    if token[0][0].isalnum():
        out += " "
    if (
        prev[0] == "can"
        and low == "not"
        or prev[0] == "got"
        and low == "ta"
        or prev[0] == "lem"
        and low == "me"
        or prev[0] == "gim"
        and low == "me"
        or prev[0] == "gon"
        and low == "na"
        or prev[0] == "wan"
        and low == "na"
    ):
        out = out[:-2]
        token = (low, token[1])
    for word in alpha_split(token[0]):
        if word.find(".") + 1:  # "e.g.", "U.S.A.", etc.
            out += word
            continue
        if initial and word[0].isalpha():
            initial = False
            if len(word) == 1 or word[1].islower():
                word = word[0].lower() + word[1:]
        if word == "&":
            out += " 𐑯"
            continue
        tran = ""
        i = "dlo".find(word[0].lower())
        if i >= 0 and len(word) > 1 and word[1] == "'" and word.lower() != "o'er":
            tran = "𐑛𐑤𐑴"[i] + apostrophe
            word = word[2:]
        whole = word
        root = prefix_split(word, token[1], 0)
        tran += root[1] if root[1] else word
        if tran.find("·") + 1:
            tran = "·" + tran.replace("·", "")
        out += tran
    prev = (low, token[1])

out = out.replace("`` ", ' "').replace("``", '"')
out = out.replace(" ''", '" ').replace("''", '"')
for x in ["“", "‘", "(", "[", "{", "$"]:
    out = out.replace(x + " ", " " + x)
print(out)
