import collections
from collections import Counter
import re
from django.conf import settings
from django.contrib.auth.models import User

from recommendations.models import Project, Review

class R_Recommender(object):
	allreviews = Review.objects.all()
	
	def get_repo_ids_per_reviewer(self, reviewer_id):
		reviews=Review.objects.filter(user_name=reviewer_id)
		ids_per_reviewer = []
		for repo_id in [r.repo for r in reviews]:
			ids_per_reviewer.append(repo_id)	
		return ids_per_reviewer		
	
	def get_reviewers_ids_per_repo(self, project_id):
		reviews = Review.objects.filter(repo=project_id)
		reviewers_ids = []
		for reviewer_id in [r.user_name for r in reviews]:
			reviewers_ids.append(reviewer_id)
		return reviewers_ids
	
	def get_reviewed_with_ids(self, project_id):
		reviewers_ids = self.get_reviewers_ids_per_repo(project_id)
		reviewed_with_ids = []
		for reviewers_id in reviewers_ids:
			ids_per_reviewer = self.get_repo_ids_per_reviewer(reviewers_id)
			for repo_id in ids_per_reviewer:
				if repo_id != project_id:
					reviewed_with_ids.append(repo_id)
		return reviewed_with_ids
	
	def suggest_projects_for(self, project, max_results=6):
		reviewed_with_ids = self.get_reviewed_with_ids(project.id)
		if project.id in reviewed_with_ids:
			reviewed_with_ids.remove(project.id)
		suggested_ids = Counter(reviewed_with_ids).most_common(max_results)
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
		