# python3
# coding=<UTF-8>

# from . import * CRASHES

from . import rus_corpus
from . import bam_corpus
from . import emk_corpus
from . import zho_corpus
from . import rus_parallel_corpus
from . import dan_corpus
from . import est_corpus
from . import kat_corpus
from . import crh_corpus
from . import tat_corpus
from . import deu_corpus
from . import slk_corpus
from . import hin_corpus
from . import rus_pol_corpus
from . import zho_eng_corpus
from . import jpn_eng_corpus
from . import jpn_zho_corpus
from . import sl_dict

functions = {'rus': rus_corpus,
             'bam': bam_corpus,
             'emk': emk_corpus,
             'zho': zho_corpus,
             'rus_parallel': rus_parallel_corpus,
             'dan': dan_corpus,
             'est': est_corpus,
             'kat': kat_corpus,
             'crh': crh_corpus,
             'tat': tat_corpus,
             'deu': deu_corpus,
             'slk': slk_corpus,
             'hin': hin_corpus,
             'rus_pol': rus_pol_corpus,
             'zho_eng': zho_eng_corpus,
             'jpn_eng': jpn_eng_corpus,
             'jpn_zho': jpn_zho_corpus,
             'sls': sl_dict
}
