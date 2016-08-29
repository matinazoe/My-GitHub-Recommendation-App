from django.shortcuts import get_object_or_404, render, render_to_response
import requests
import json
from taggit.models import TaggedItem
from django.contrib.auth.models import User
from recommendations.models import Review, Project
from taggit.models import TaggedItem, Tag

all_repos = Project.objects.all().exclude(id=2).exclude(id=11).exclude(id=9).exclude(id=19580)

for repo in all_repos: 
    url='https://api.github.com/repos/'+repo.owner_id.username+'/'+repo.name
    r = requests.get(url)
    if(r.ok):
        repoItem = json.loads(r.text or r.content)
        tag=Tag.objects.get_or_create(name=repo.language)
        tagged=TaggedItem.objects.get_or_create(content_type_id=8, object_id=repo.id, tag_id=tag.id)
        repo.language=repoItem['language']
        print repo.owner_id.username , repo.name
        print repo.language
        print tag.id, tag.name
        repo.save()
        tag.save()
 
from django.shortcuts import get_object_or_404, render, render_to_response

all_repos = Project.objects.all().exclude(id=2).exclude(id=11).exclude(id=9).exclude(id=19580)

for repo in all_repos: 
    Tag.objects.get_or_create(name=repo.language)
    tag=get_object_or_404(Tag, name=repo.language)
    print tag
    tagged=TaggedItem.objects.get_or_create(content_type_id=8, object_id=repo.id, tag_id=tag.id)
    print tagged
    
from django.shortcuts import get_object_or_404, render, render_to_response
from topia.termextract import extract
extractor = extract.TermExtractor()
extractor.tagger
extractor.filter = extract.DefaultFilter(singleStrengthMinOccur=2)

for repo in all_repos: 
    text=repo.description
    print text
    labels=extractor(text)
    for label in labels:
        print label[0]
        Tag.objects.get_or_create(name=label[0])
        tag=get_object_or_404(Tag, name=label[0])
        print tag
        tagged=TaggedItem.objects.get_or_create(content_type_id=8, object_id=repo.id, tag_id=tag.id)
        print tagged


for label in labels:
    print label[0]
    Tag.objects.get_or_create(name=label[0])
    tag=get_object_or_404(Tag, name=label[0])
    print tag
    tagged=TaggedItem.objects.get_or_create(content_type_id=8, object_id=repo.id, tag_id=tag.id)
    print tagged	

extractor.filter = extract.permissiveFilter
extractor.filter = extract.DefaultFilter(singleStrengthMinOccur=2)


extractor.filter = extract.permissiveFilter
for repo in all_repos: 
    text=repo.description
    print text
    labels=extractor(text)
    for label in labels:
        print label
        label_is_tag=Tag.objects.filter(name=label[0])
        print label_is_tag
        if label_is_tag:
            tag=Tag.objects.get(name=label[0])
            print tag
            tagged=TaggedItem.objects.get_or_create(content_type_id=8, object_id=repo.id, tag_id=tag.id)
            print tagged


repo=get_object_or_404(Project, id=18440)
repo_tags_ids = repo.tags.values_list('id', flat=True)
similar_repos = Project.objects.filter(tags__in=repo_tags_ids).filter(forked_from=None).exclude(id=repo.id).exclude(forked_from=repo.id).exclude(forked_from=repo.forked_from)
text=repo.description
print text
extractor.filter = extract.permissiveFilter
labels=extractor(text)

repos = Project.objects.filter(forked_from=None)