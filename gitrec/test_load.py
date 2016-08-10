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
    print "This project is written in: " + repoItem['language']
    language=repoItem['language']

from taggit.models import TaggedItem
from recommendations.models import Review, Project

doom=get_object_or_404(Project, id=152)
tagcplus=Tag.objects.get_or_create(name=language) 
tag152=get_object_or_404(TaggedItem, name=language)
print tag152.id
	