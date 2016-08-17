from django import template
from django.db.models import Count, Max
from django.utils.safestring import mark_safe

register = template.Library()

from ..models import Project, Review
from django.contrib.auth.models import User

@register.simple_tag
def total_repos():
	return Project.objects.count()

@register.simple_tag
def total_reviews():
	return Review.published.count()

@register.simple_tag
def total_users():
	return User.objects.count()	

@register.inclusion_tag('recommendations/last_reviews.html')
def show_last_reviews(count=2):
    last_reviews = Review.published.order_by('-pub_date')[:count]
    return {'last_reviews': last_reviews}


@register.assignment_tag
def get_most_reviewed_repos(count=5):
    return Project.objects.annotate(total_reviews=Count('rates')).order_by('-total_reviews')[:count]

