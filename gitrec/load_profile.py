import sys, os 
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gitrec.settings")

import django
django.setup()

from recommendations.models import UserProfile
from django.contrib.auth.models import User

def save_userprofile_from_row(userprofile_row):
    userprofile = UserProfile()
    userprofile.id = userprofile_row[0]
    userprofile.company = userprofile_row[10]
    userprofile.location = userprofile_row[11]
    userprofile.type = userprofile_row[12]
    userprofile.user_id = User.objects.get(id=repo_row[0])
    userprofile.save()
	
    
    
if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print "Reading from file " + str(sys.argv[1])
        userprofile_df = pd.read_csv(sys.argv[1])
        print userprofile_df

        userprofile_df.apply(
            save_userprofile_from_row,
            axis=1
        )

        print "There are {} users".format(UserProfile.objects.count())
        
    else:
        print "Please, provide UserProfile file path"
