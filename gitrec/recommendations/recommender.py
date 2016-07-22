import collections
from collections import Counter
import re
from django.conf import settings
from django.contrib.auth.models import User

from recommendations.models import Project, Watchers

class Recommender(object):
	allwatchers = Watchers.objects.all()
	
	def get_ids_per_user(self, watcher_id):
		w_user=Watchers.objects.filter(user_id=watcher_id)
		ids_per_user = []
		for r_id in [w.repo_id for w in w_user]:
			ids_per_user.append(r_id)	
		return ids_per_user		
	
	def get_watchers_ids(self, project_id):
		watchers = Watchers.objects.filter(repo_id=project_id)
		watchers_ids = []
		for u_id in [w.user_id for w in watchers]:
			watchers_ids.append(u_id)
		return watchers_ids
	
	def get_watched_with_ids(self, project_id):
		watchers_ids = self.get_watchers_ids(project_id)
		watched_with_ids = []
		for u_id in watchers_ids:
			ids_per_user = self.get_ids_per_user(u_id)
			ids_per_user.remove(project_id)
			for r_id in ids_per_user:
				if r_id != project_id:
					watched_with_ids.append(r_id)
		return watched_with_ids
	
	def suggest_projects_for(self, project, max_results=6):
		watched_with_ids = self.get_watched_with_ids(project.id)
		if project.id in watched_with_ids:
			watched_with_ids.remove(project.id)
		suggested_ids = Counter(watched_with_ids).most_common(max_results)
		ids = []
		for item in suggested_ids:
			ms=str(item)
			i=ms.find(': ')
			j=ms.find('>')
			sname=ms[i+2:j]
			item_id=Project.objects.filter(name=sname).values('id')[0]['id']
			ids.append(item_id)
		
		suggested_projects = list(Project.objects.filter(id__in=ids))
		return suggested_projects
		
	'''
	def repo_score(self, project, repo):
		# project is the project we are looking suggestions for
		# repo is one of the projects users:watchers are also watching
		score = 0
		if repo.id in watched_repos = get_watched_with_ids(project_id):
			score = watched_repos.count(repo.id)
		return score
	
	def suggest_projects_for(self, project, max_results=6):
				
		scored_repos = {}
		for repo in watched_repos= get_watched_with_ids(project_id):
			scored_repos[repo].append(repo_score(project_id,repo))
		scored_repos = sorted(scored_repos, key=lambda x:x[1], reverse=True)[:max_results]
	
		suggested_ids = [p.id for p in scored_repos]
		
        # get suggested projects and sort by order of appearance
		suggested_projects = list(Project.objects.filter(id__in=suggested_ids))
		suggested_projects.sort(key=lambda x: suggested_ids_ids.index(x.id))
		return suggested_projects
	
	def clear_recommendations(self):
		watched_ids_per_user.clear()
	'''	