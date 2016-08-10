import collections
from collections import Counter
import re
from django.conf import settings
from django.contrib.auth.models import User

from recommendations.models import Project, Watchers, Followers

class U_recommender(object):
	
	def get_uids_per_follower(self, follower_id):
		f_users=Followers.objects.filter(follower_id=follower_id)
		uids_per_follower = []
		for u_id in [f.user_id for f in f_users]:
			uids_per_follower.append(u_id)	
		return uids_per_follower		
	
	def get_followers_ids(self, user_id):
		followers = Followers.objects.filter(user_id=user_id)
		followers_ids = []
		for f_id in [f.follower_id for f in followers]:
			followers_ids.append(f_id)
		return followers_ids
	
	def get_followed_with_ids(self, user_id):
		followers_ids = self.get_followers_ids(user_id)
		followed_with_ids = []
		for f_id in followers_ids:
			ids_per_follower = self.get_uids_per_follower(f_id)
			for u_id in ids_per_follower:
				if u_id != user_id:
					followed_with_ids.append(u_id)
		return followed_with_ids
	
	def suggest_users(self, user, max_results=6):
		followed_with_ids = self.get_followed_with_ids(user.id)
		if user.id in followed_with_ids:
			followed_with_ids.remove(user.id)
		suggested_uids = Counter(followed_with_ids).most_common(max_results)
		ids = []
		for item in suggested_uids:
			ms=str(item)
			i=ms.find(': ')
			j=ms.find('>')
			sname=ms[i+2:j]
			item_id=User.objects.filter(username=sname).values('id')[0]['id']
			ids.append(item_id)
		
		suggested_users = list(User.objects.filter(id__in=ids))
		return suggested_users
		
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