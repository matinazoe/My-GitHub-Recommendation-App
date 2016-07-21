import redis
import collections
from django.conf import settings
from django.contrib.auth.models import User

from .models import Project, Watchers

class Recommender(object):
	watchers = Watchers.objects.filter(repo_id=object.id).order_by('repo_id')
	watcher_ids=[w.id for w in watchers]
	watched_ids_per_user = collections.defaultdict(list)
		for w in watchers:
		watched_ids_per_user[w.user_id].append(w.repo_id)
	
	watched_ids = []
	for id in watcher_ids
		if id not in watched_ids.values
			watched_ids.append(id)
	watched_ids = sorted(watched_ids)
	
	watched_repos = list(Project.objects.filter(id__in=watched_ids))
	
	def is_project_watched(self, id):
		if id in watched_ids:
		return 'project:{}:is_watched'.format(id)
		
	
	def project_score(self, repo):
		score = 0
		for w in watchers:
			if repo.id in watched_ids_per_user[w.user_id].values:
				if repo.id!= object.id:
					score =score +1
		return score
	
			
	def suggest_projects_for(self, projects, max_results=6):
		scored_repos = {}
		for repo in watched_repos
			scored_repos[repo].append(project_score(repo))
		scored_repos = sorted(scored_repos, key=lambda x:x[1], reverse=True)[:6]
	
		suggested_ids = [p.id for p in scored_repos.keys()]
		
        # get suggested projects and sort by order of appearance
		suggested_projects = list(Project.objects.filter(id__in=suggested_projects_ids))
		suggested_projects.sort(key=lambda x: suggested_projects_ids.index(x.id))
		return suggested_projects
	
	def clear_recommendations(self):
		for id in Project.objects.values_list('id', flat=True):
			r.delete(self.get_project_watched(id))