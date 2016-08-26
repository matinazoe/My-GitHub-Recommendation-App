import requests
import json
from taggit.models import TaggedItem
from django.contrib.auth.models import User
from recommendations.models import Review, Project

all_repos = Project.objects.all().exclude(id=2).exclude(id=11).exclude(id=9).exclude(id=19580)
for repo in all_repos: 
    url='https://api.github.com/repos/'+repo.owner_id.username+'/'+repo.name
    r = requests.get(url)
    if(r.ok):
        repoItem = json.loads(r.text or r.content)
        repo.url=repoItem['html_url']
        repo.created_at=repoItem['created_at']
        repo.language=repoItem['language']
        print repo.owner_id.username
        print repo.name
        repo.save()
		
		
