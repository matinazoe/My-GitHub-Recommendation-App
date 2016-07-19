import sys, os 
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gitrec.settings")

import django
django.setup()

from recommendations.models import Project 
from django.contrib.auth.models import User

def save_repo_from_row(repo_row):
	repo = Project()
	repo.id = repo_row[0]
	repo.name = repo_row[1]
	repo.owner_id = User.objects.get(id=repo_row[2])
	repo.url = repo_row[3]
	repo.description = repo_row[4]
	repo.language = repo_row[5]
	repo.created_at = repo_row[6]
	repo.save()
    
    
if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print "Reading from file " + str(sys.argv[1])
        repos_df = pd.read_csv(sys.argv[1])
        print repos_df

        repos_df.apply(
            save_repo_from_row,
            axis=1
        )

        print "There are {} repos".format(Project.objects.count())
        
    else:
        print "Please, provide Project file path"
