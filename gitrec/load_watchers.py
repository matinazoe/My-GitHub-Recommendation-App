import sys, os 
import pandas as pd
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gitrec.settings")

import django
django.setup()

from recommendations.models import Watchers, Project
from django.contrib.auth.models import User

def save_watchers_from_row(watchers_row):
    watchers = Watchers()
    watchers.id = watchers_row[0]
    watchers.user_id = User.objects.get(id=watchers_row[1])
    watchers.repo_id = Project.objects.get(id=watchers_row[2])
    watchers.created_at = datetime.datetime.now()
    watchers.save()
	
    
    
if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print "Reading from file " + str(sys.argv[1])
        watchers_df = pd.read_csv(sys.argv[1])
        print watchers_df

        watchers_df.apply(
            save_watchers_from_row,
            axis=1
        )

        print "There are {} watchers".format(Watchers.objects.count())
        
    else:
        print "Please, provide watchers file path"
