from __future__ import unicode_literals
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager


from django.db import models

import numpy as np

# User Profile models here.
class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profiled', blank=True)
# Can retrieve related objects as userprofile.user.(all) or from a user object as user.profiled.(all)
	company = models.CharField(max_length=100,blank=True,null=True)
	location = models.CharField(max_length=250,blank=True)
	type = models.CharField(max_length=100)

	def __str__(self):
		return self.user.username
	
	def get_GitHub_url(self):
		BASE_URL='https://github.com/'
		GitHub_url = BASE_URL + self.user.username
		return (GitHub_url)
		

def create_profile(sender, instance, created, **kwargs):
	if created:
		profile, created = UserProfile.objects.get_or_create(user=instance)

from django.db.models.signals import post_save
post_save.connect(create_profile, sender=User)

class Followers(models.Model):
    user_id = models.ForeignKey(User,related_name='is_followed')
    follower_id = models.ForeignKey(User,related_name='follows')
    created = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        ordering = ('-created',)
		
    def __str__(self):
        return '{} follows {}'.format(self.follower_id,self.user_id)
		
		
User.add_to_class('following', models.ManyToManyField('self',
                                                      through=Followers, 
													  related_name='all_followers',
													  symmetrical=False))


# User Github models here.
class RatedManager(models.Manager):
    def get_queryset(self):
        return super(RatedManager, self).get_queryset().all()

class Project(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.URLField(max_length=200, default="https://github.com/personal")
    owner_id = models.ForeignKey(User, related_name='owns')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(max_length=500, blank=True)
    language = models.CharField(max_length=50,blank=True,null=True)
    created_at = models.DateTimeField('date created')
    forked_from = models.ForeignKey('self', models.SET_NULL,blank=True,null=True)
    updated_at = models.DateTimeField('date updated',blank=True,null=True)

    objects = models.Manager() # The default manager.
    rated = RatedManager() # The custom manager.
    
    tags = TaggableManager()
	
    class Meta:
        ordering = ('-created_at',)
	
    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.rates.all())
        return np.mean(all_ratings)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recommendations:project_detail', args=[self.id])
		

class Project_Languages(models.Model):
	project_id = models.ForeignKey(Project, related_name='has_code_of')
	language = models.CharField(max_length=100)
	created_at = models.DateTimeField('date created')

class Watchers(models.Model):
	repo_id = models.ForeignKey(Project, related_name='is_watched')
	user_id = models.ForeignKey(User, related_name='watches')
	created_at = models.DateTimeField('date created')

class Project_members(models.Model):
	repo_id = models.ForeignKey(Project, related_name='is_made')
	user_id = models.ForeignKey(User, related_name='contributes')
	created_at = models.DateTimeField('date created')
												 

# Review models here.		
class ReviewManager(models.Manager):
    def get_queryset(self):
        return super(ReviewManager, self).get_queryset().filter(status='Published')


class Review(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=250, null=True)
    slug = models.SlugField(max_length=250, unique_for_date='pub_date',null=True)
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    repo = models.ForeignKey(Project, related_name='rates', on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    user_name = models.ForeignKey(User, related_name='reviewer')
    comment = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)

    objects = models.Manager() # The default manager.
    published = ReviewManager() 
    Tags = TaggableManager()
	
    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recommendations:review_detailslug', args=[self.pub_date.year,
                                                 self.pub_date.strftime('%m'),
                                                 self.pub_date.strftime('%d'),
                                                 self.slug])		

