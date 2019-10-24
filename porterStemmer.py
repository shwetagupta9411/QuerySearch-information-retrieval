import re

class PorterStemmer:
    def __init__(self):
        self._step2list = {
                      "ational": "ate",
                      "tional": "tion",
                      "enci": "ence",
                      "anci": "ance",
                      "izer": "ize",
                      "bli": "ble",
                      "alli": "al",
                      "entli": "ent",
                      "eli": "e",
                      "ousli": "ous",
                      "ization": "ize",
                      "ation": "ate",
                      "ator": "ate",
                      "alism": "al",
                      "iveness": "ive",
                      "fulness": "ful",
                      "ousness": "ous",
                      "aliti": "al",
                      "iviti": "ive",
                      "biliti": "ble",
                      "logi": "log",
                      }

        self._step3list = {
                      "icate": "ic",
                      "ative": "",
                      "alize": "al",
                      "iciti": "ic",
                      "ical": "ic",
                      "ful": "",
                      "ness": "",
                      }


        self._cons = "[^aeiou]"
        self._vowel = "[aeiouy]"
        self._cons_seq = "[^aeiouy]+"
        self._vowel_seq = "[aeiou]+"

        # m > 0
        self._mgr0 = re.compile("^(" + self._cons_seq + ")?" + self._vowel_seq + self._cons_seq)
        # m == 0
        self._meq1 = re.compile("^(" + self._cons_seq + ")?" + self._vowel_seq + self._cons_seq + "(" + self._vowel_seq + ")?$")
        # m > 1
        self._mgr1 = re.compile("^(" + self._cons_seq + ")?" + self._vowel_seq + self._cons_seq + self._vowel_seq + self._cons_seq)
        # vowel in stem
        self._s_v = re.compile("^(" + self._cons_seq + ")?" + self._vowel)
        # ???
        self._c_v = re.compile("^" + self._cons_seq + self._vowel + "[^aeiouwxy]$")

        # Patterns used in the rules

        self._ed_ing = re.compile("^(.*)(ed|ing)$")
        self._at_bl_iz = re.compile("(at|bl|iz)$")
        self._step1b = re.compile("([^aeiouylsz])\\1$")
        self._step2 = re.compile("^(.+?)(ational|tional|enci|anci|izer|bli|alli|entli|eli|ousli|ization|ation|ator|alism|iveness|fulness|ousness|aliti|iviti|biliti|logi)$")
        self._step3 = re.compile("^(.+?)(icate|ative|alize|iciti|ical|ful|ness)$")
        self._step4_1 = re.compile("^(.+?)(al|ance|ence|er|ic|able|ible|ant|ement|ment|ent|ou|ism|ate|iti|ous|ive|ize)$")
        self._step4_2 = re.compile("^(.+?)(s|t)(ion)$")
        self._step5 = re.compile("^(.+?)e$")

    def stem(self, w):
        """Uses the Porter stemming algorithm to remove suffixes from English
        words.

        >>> stem("fundamentally")
        "fundament"
        """

        if len(w) < 3:
            return w

        first_is_y = w[0] == "y"
        if first_is_y:
            w = "Y" + w[1:]

        # Step 1a
        if w.endswith("s"):
            if w.endswith("sses"):
                w = w[:-2]
            elif w.endswith("ies"):
                w = w[:-2]
            elif w[-2] != "s":
                w = w[:-1]

        # Step 1b

        if w.endswith("eed"):
            s = w[:-3]
            if self._mgr0.match(s):
                w = w[:-1]
        else:
            m = self._ed_ing.match(w)
            if m:
                stem = m.group(1)
                if self._s_v.match(stem):
                    w = stem
                    if self._at_bl_iz.match(w):
                        w += "e"
                    elif self._step1b.match(w):
                        w = w[:-1]
                    elif self._c_v.match(w):
                        w += "e"

        # Step 1c

        if w.endswith("y"):
            stem = w[:-1]
            if self._s_v.match(stem):
                w = stem + "i"

        # Step 2

        m = self._step2.match(w)
        if m:
            stem = m.group(1)
            suffix = m.group(2)
            if self._mgr0.match(stem):
                w = stem + self._step2list[suffix]

        # Step 3

        m = self._step3.match(w)
        if m:
            stem = m.group(1)
            suffix = m.group(2)
            if self._mgr0.match(stem):
                w = stem + self._step3list[suffix]

        # Step 4

        m = self._step4_1.match(w)
        if m:
            stem = m.group(1)
            if self._mgr1.match(stem):
                w = stem
        else:
            m = self._step4_2.match(w)
            if m:
                stem = m.group(1) + m.group(2)
                if self._mgr1.match(stem):
                    w = stem

        # Step 5

        m = self._step5.match(w)
        if m:
            stem = m.group(1)
            if self._mgr1.match(stem) or (self._meq1.match(stem) and not self._c_v.match(stem)):
                w = stem

        if w.endswith("ll") and self._mgr1.match(w):
            w = w[:-1]

        if first_is_y:
            w = "y" + w[1:]

        return w
