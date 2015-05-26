#!/usr/bin/env python
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "steelrumors.settings")

from Xarxa.models import Aportacio

def rank_all():
    for link in Aportacio.with_votes.all():
        link.set_rank()

import time

def show_all():
    print "\n".join("%10s %0.2f" % (l.titol, l.rank_score,
                         ) for l in Aportacio.with_votes.all())
    print "----\n\n\n"

if __name__=="__main__":
    while 1:
        print "---"
        rank_all()
        show_all()
        time.sleep(5)
