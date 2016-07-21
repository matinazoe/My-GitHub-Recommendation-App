import redis
from django.conf import settings
from django.contrib.auth.models import User

from .models import Project, Watchers

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
						port=settings.REDIS_PORT,
						db=settings.REDIS_DB)
class Recommender(object):
# the projects  the user(user.id) watches
	def get_project_watched_id(self, id):
		return 'project:{}:is_watched'.format(id)
		

	def projects_watched(self, projects):
		project_ids = [p.id for p in projects]
		for project_id in project_ids:
			for with_id in project_ids:
			# get the other project watched with each project
				if project_id != with_id:
				# increment score for product purchased together
					r.zincrby(self.get_project_watched_id(project_id),
								with_id, amount=1)
							

	def suggest_projects_for(self, projects, max_results=6):
		project_ids = [p.id for p in projects]
		if len(projects) == 1:
			# only 1 project
			suggestions = r.zrange(self.get_project_watched_id(project_ids[0]), 0, -1, desc=True)[:max_results]
		else:
			# generate a temporary key
			flat_ids = ''.join([str(id) for id in project_ids])
			tmp_key = 'tmp_{}'.format(flat_ids)
			# multiple projects, combine scores of all projects
			# store the resulting sorted set in a temporary key
			keys = [self.get_project_watched_id(id) for id in project_ids]
			r.zunionstore(tmp_key, keys)
			# remove ids for the projects the recommendation is for
			r.zrem(tmp_key, *project_ids)
            # get the project ids by their score, descendant sort
			suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            # remove the temporary key
			r.delete(tmp_key)
		suggested_projects_ids = [int(id) for id in suggestions]

        # get suggested projects and sort by order of appearance
		suggested_projects = list(Project.objects.filter(id__in=suggested_projects_ids))
		suggested_projects.sort(key=lambda x: suggested_projects_ids.index(x.id))
		return suggested_projects
	
	def clear_recommendations(self):
		for id in Project.objects.values_list('id', flat=True):
			r.delete(self.get_project_watched_id(id))