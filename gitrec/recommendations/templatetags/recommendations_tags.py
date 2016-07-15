from django import template
from django.db.models import Count, Max
from django.utils.safestring import mark_safe

register = template.Library()

from ..models import Project, Review

@register.simple_tag
def total_repos():
	return Project.objects.count()

@register.simple_tag
def total_reviews():
	return Review.published.count()


@register.inclusion_tag('recommendations/last_reviews.html')
def show_last_reviews(count=2):
    last_reviews = Review.published.order_by('-pub_date')[:count]
    return {'last_reviews': last_reviews}


@register.assignment_tag
def get_most_reviewd_repos(count=5):
    return Review.published.annotate(total_reviews=Count('reviews')).order_by('-total_reviews')[:count]

