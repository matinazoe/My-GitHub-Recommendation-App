from django.shortcuts import get_object_or_404, render, render_to_response
from topia.termextract import extract
extractor = extract.TermExtractor()
extractor.tagger
extractor.filter = extract.DefaultFilter(singleStrengthMinOccur=2)

import requests
import json
r = requests.get('https://api.github.com/repos/mtrencseni/doom3')
if(r.ok):
    repoItem = json.loads(r.text or r.content)
    print "This is project: " + repoItem['full_name']
    print "This project' description: " + repoItem['description']
    description=repoItem['description']

from taggit.models import TaggedItem, Tag
from recommendations.models import Review, Project

all_repos = Project.objects.all()
for repo in all_repos: 
	tag=Tag.objects.get_or_create(name=repo.language)

	
doom=get_object_or_404(Project, id=152)
tagged=Tag.objects.get_or_create(name=language) 
tag152=get_object_or_404(TaggedItem, name=language)
print tag152.id
	