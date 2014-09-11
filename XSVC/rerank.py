__author__ = 'sergi'
#!/usr/bin/env python
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "XSCV.settings")
from Xarxa.models import Aportacio
from Xarxa.models import Debat

def rank_all():
    for link in Aportacio.with_votes.all():
        link.set_rank()

    for aux in Debat.with_votes.all():
        aux.set_rank()

import time

def show_all():
    print "\n".join("%10s %0.2f" % (l.titol, l.rank_score,
                         ) for l in Aportacio.with_votes.all())


    print "\n".join("%10s %0.2f" % (l.titol, l.rank_score,
                         ) for l in Debat.with_votes.all())


    print "----\n\n\n"



######## repetició per al debat----------------------------------------


# def rank_all2():
#     for link in Debat.with_votes.all():
#         link.set_rank()
#
#
# def show_all2():
#     print "\n".join("%10s %0.2f" % (l.titol, l.rank_score,
#                          ) for l in Debat.with_votes.all())
#     print "----\n\n\n"
#
#

############################3

if __name__=="__main__":
    while 1:
        print "---"
        rank_all()
        show_all()

        time.sleep(5)





