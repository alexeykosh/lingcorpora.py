# python3
# coding=<UTF-8>

import re


class Target:

    def __init__(
        self,
        text,
        idxs,
        meta,
        analysis,
        gr_tags=None,
        transl=None,
        lang=None
    ):
        """
        text: str: full sentence / document
        idxs: tuple (l, r): target idxs in self.text -> self.text[l:r]
        meta: str: sentence / document info (if exists)
        analysis: dict?: target analysis (parsed)
        gr_tags: str or None: grammatical tags passed by user
        transl: str or None: text translation (for parallel corporas and dictionaries)
        lang: str or None: translation language (for parallel corporas and dictionaries)
        """
        
        self.text = text
        self.idxs = idxs
        self.meta = meta
        self.analysis = analysis
        self.gr_tags = gr_tags
        self.transl = transl
        self.lang = lang
        
    def __str__(self):
        return 'Target(%s, %s)' % \
                (self.text[self.idxs[0]:self.idxs[1]], self.meta)

    __repr__ = __str__
            
    def __get_kwic_wlvl_target_idx(self):
        """
        get word level index of target
        """
        
        return len(self.text[:self.idxs[0]].split())
    
    def __handle_punct(self, l, c, r):
        """
        handle punctuation outside the target
        ('one;', 'two;', 'three!') >> ('one;', 'two', ';three!') 
        """
        
        if re.search(r'[\W]', c) is not None:
            l_punct = re.search(r'^([\W]*)', c).group(1)
            r_punct = re.search(r'([\W]*)$', c).group(1)
            c = re.sub(r'^[\W]*', '', c)
            c = re.sub(r'[\W]*$', '', c)
            l += l_punct
            r = r_punct + ' ' + r
            r = r.strip()
            
        return (l, c, r)
    
    def kwic(self, left, right, level='word'):
        """
        level: ['word', 'char']: if "word" - split by words
                                 if "char" - split by characters
        """

        # ISSUE: 'one , two, three >> kwic(1, 1, word) >> (',', 'two', ',three')
        
        if level not in {'word', 'char'}:
            raise ValueError('got invalid `level` "%s"' % level)
        
        level = 'char' if ' ' not in self.text else level
        
        if level == 'word':
            tokens = self.text.split()
            idx = self.__get_kwic_wlvl_target_idx()

            return self.__handle_punct(
                ' '.join(tokens[max(0, idx-left):idx]),
                tokens[idx],
                ' '.join(tokens[idx+1:idx+right+1])
            )

        else:
            return (
                self.text[max(0, self.idxs[0]-left):self.idxs[0]],
                self.text[self.idxs[0]:self.idxs[1]],
                self.text[self.idxs[1]:self.idxs[1]+right]
            )
