import requests
import json
from taggit.models import TaggedItem
from django.contrib.auth.models import User
from recommendations.models import Review, Project
from django.shortcuts import get_object_or_404, render, render_to_response

all_repos = Project.objects.all().exclude(id=2).exclude(id=11).exclude(id=9).exclude(id=19580)
for repo in all_repos: 
    url='https://api.github.com/repos/'+repo.owner_id.username+'/'+repo.name
    html_url='https://github.com/'+repo.owner_id.username+'/'+repo.name
    r = requests.get(url)
    if(r.ok):
        repoItem = json.loads(r.text or r.content)
        repo.url=html_url
        repo.created_at=repoItem['created_at']
        repo.language=repoItem['language']
        print repo.owner_id.username
        print repo.name
        repo.save()
		

for repo in all_repos: 
    url='https://github.com/'+repo.owner_id.username+'/'+repo.name
    repo.url=url
    print repo.owner_id.username, repo.name
    print repo.url
    if repo.created_at==None:
        repo.created_at=datetime.datetime.now()
    print repo.created_at
    repo.save()
	
	r = requests.get(url)
    if(r.ok):
        repoItem = json.loads(r.text or r.content)
        repo.url=repoItem['html_url']
        repo.created_at=repoItem['created_at']
        repo.language=repoItem['language']
        print repo.owner_id.username
        print repo.name
        repo.save()
		
repo=Project.objects.get(id=725)