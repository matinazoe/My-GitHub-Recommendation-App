import redis
import collections
from django.conf import settings
from django.contrib.auth.models import User

from .models import Project, Watchers

class Recommender(object):
	
	def get_ids_per_user(self, watcher, repo):
		watchers = Watchers.objects.filter(repo_id=repo.id).order_by('repo_id')
		
		watched_ids_per_user = collections.defaultdict(list)
		for w in watchers:
			watched_ids_per_user[w.user_id].append(w.repo_id)
			
		ids_per_user = watched_ids_per_user[watcher.user_id].values
		return ids_per_user
	
	def project_score(self, project):
		score = 0
		
		watchers = Watchers.objects.filter(repo_id=project.id).order_by('repo_id')
		for w in watchers:
			ids_per_user = get_ids_per_user(w.user_id, project)
			if repo.id in ids_per_user:
				if repo.id!= project.id:
					score =score +1
		return score
	
			
	def suggest_projects_for(self, project, max_results=6):
		watchers = Watchers.objects.filter(repo_id=project.id).order_by('repo_id')
		
		watched_ids = []
		for id in [w.id for w in watchers]:
			if id not in watched_ids:
				watched_ids.append(id)
		watched_ids = sorted(watched_ids)
		
		watched_repos = list(Project.objects.filter(id__in=watched_ids))		
		
		scored_repos = {}
		for repo in watched_repos:
			scored_repos[repo].append(project_score(repo))
		scored_repos = sorted(scored_repos, key=lambda x:x[1], reverse=True)[:max_results]
	
		suggested_ids = [p.id for p in scored_repos]
		
        # get suggested projects and sort by order of appearance
		suggested_projects = list(Project.objects.filter(id__in=suggested_ids))
		suggested_projects.sort(key=lambda x: suggested_ids_ids.index(x.id))
		return suggested_projects
	
	def clear_recommendations(self):
		watched_ids_per_user.clear()