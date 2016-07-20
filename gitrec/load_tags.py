import sys, os 
import pandas as pd
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gitrec.settings")

import django
django.setup()

from recommendations.models import Project
from taggit.models import Tag

def save_tag_from_row(tag_row):
    tag = Tag()
    tag.id = tag_row[0]
    tag.name = tag_row[1]
    tag.save()
	
    
    
if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print "Reading from file " + str(sys.argv[1])
        tag_df = pd.read_csv(sys.argv[1], sep=';')
        print tag_df

        tag_df.apply(
            save_tag_from_row,
            axis=1
        )

        print "There are {} tags".format(Tag.objects.count())
        
    else:
        print "Please, provide tags file path"
