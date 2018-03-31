# python3
# coding=<UTF-8>

import re


class Target:
    def __init__(self, text, idxs, meta, tags, transl=None, lang=None):
        """
        text: str: full sentence / document
        idxs: tuple (l, r): target idxs in self.text -> self.text[l:r]
        meta: str: sentence / document info (if exists)
        tags: dict?: target tags
        """
        self.text = text
        self.idxs = idxs
        self.meta = meta
        self.tags = tags
        self.transl = transl
        self.lang = lang
        
    def __str__(self):
        return 'Target(%s, %s)' \
                % (self.text[self.idxs[0]: self.idxs[1]],
                   self.meta
                   )

    __repr__ = __str__
        
    def __get_kwic_wlvl_idx(self):
        """
        get word level target index
        """
        _t = '<TARGET>%s<TARGET>' \
              % self.text[self.idxs[0]: self.idxs[1]]
        _s = '%s%s%s' % (self.text[: self.idxs[0]],
                         _t,
                         self.text[self.idxs[1]:]
                        )
        for i, tkn in enumerate(_s.split()):
            if _t in tkn:
                return i
        raise ValueError('no target found, check `level`')
    
    def __fix_kwic(self, l, c, r):
        """
        handle punctuation outside the target
        """
        if re.search('[\W]', c) is not None:
            l_punct = re.search('(^[\W]*)', c).group(1)
            r_punct = re.search('([\W]*)$', c).group(1)
            c = re.sub('[\W]', '', c)
            l += l_punct
            r = r_punct + r
        return (l, c, r)
    
    def kwic(self, left, right, level='word'):
        """
        level: ['word', 'char']: if "word" - split by words
                                 if "char" - split by characters
        """
        if level not in ['word', 'char']:
            raise ValueError('got invalid `level` "%s"' % level)
        
        if ' ' not in self.text:
            level = 'char'
        
        if level == 'word':
            tkns = self.text.split()
            idx = self.__get_kwic_wlvl_idx()
            if idx - left < 1:
                return self.__fix_kwic(' '.join(tkns[: idx]),
                                       tkns[idx],
                                       ' '.join(tkns[idx+1: idx+right+1])
                                      )
            return self.__fix_kwic(' '.join(tkns[idx-left: idx]),
                                   tkns[idx],
                                   ' '.join(tkns[idx+1: idx+right+1])
                                  )

        else:
            if self.idxs[0] - left < 1:
                return (self.text[: self.idxs[0]],
                        self.text[self.idxs[0]: self.idxs[1]],
                        self.text[self.idxs[1]:self.idxs[1]+right]
                       )
            return (self.text[self.idxs[0]-left: self.idxs[0]],
                    self.text[self.idxs[0]: self.idxs[1]],
                    self.text[self.idxs[1]: self.idxs[1]+right]
                   )
