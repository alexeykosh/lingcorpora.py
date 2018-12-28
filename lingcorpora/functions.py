# python3
# coding=<UTF-8>

# from . import * CRASHES

from .corpora import rus_corpus
from .corpora import bam_corpus
from .corpora import emk_corpus
from .corpora import zho_corpus
from .corpora import rus_parallel_corpus
from .corpora import dan_corpus
from .corpora import est_corpus
from .corpora import kat_corpus
from .corpora import crh_corpus
from .corpora import tat_corpus
from .corpora import deu_corpus
from .corpora import slk_corpus
from .corpora import hin_corpus
from .corpora import rus_pol_corpus
from .corpora import zho_eng_corpus
from .corpora import jpn_eng_corpus
from .corpora import jpn_zho_corpus
from .corpora import sl_dict
from .corpora import arm_corpus
from .corpora import grk_corpus
from .corpora import ady_corpus
from .corpora import mon_corpus
from .corpora import kaz_corpus
from .corpora import yid_corpus
from .corpora import kal_corpus
from .corpora import udm_corpus
from .corpora import bua_corpus
from .corpora import alb_corpus

functions = {
    'rus': rus_corpus,
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
    'sls': sl_dict,
    'arm': arm_corpus,
    'grk': grk_corpus,
    'ady': ady_corpus,
    'mon': mon_corpus,
    'kaz': kaz_corpus,
    'yid': yid_corpus,
    'kal': kal_corpus,
    'udm': udm_corpus,
    'bua': bua_corpus,
    'alb': alb_corpus
}
