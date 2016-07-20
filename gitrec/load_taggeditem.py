import sys, os 
import pandas as pd
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gitrec.settings")

import django
django.setup()

from recommendations.models import Project
from taggit.models import Taggeditem

def save_tag_from_row(taggeditem_row):
    taggeditem = Taggeditem()
    taggeditem.id = taggeditem_row[0]
    taggeditem.name = taggeditem_row[1]
    taggeditem.save()
	
    
    
if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print "Reading from file " + str(sys.argv[1])
        taggeditem_df = pd.read_csv(sys.argv[1], sep=';')
        print taggeditem_df

        taggeditem_df.apply(
            save_taggeditem_from_row,
            axis=1
        )

        print "There are {} taggeditems".format(Taggeditem.objects.count())
        
    else:
        print "Please, provide taggeditems file path"
