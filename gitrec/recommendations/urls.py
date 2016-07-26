"""gitrec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.homepage, name='homepage'),
	# User
    url(r'^users/dashboard^$', views.dashboard, name='dashboard'),
    url(r'^users/$', views.active_user_list, name='active_user_list'),	
    url(r'^users/(?P<user_id>\w+)/$', views.user_detail, name='user_detail'),
    # Reviews
    url(r'^reviews$', views.review_list, name='review_list'),
    url(r'^reviews/latest$', views.latest_reviews, name='latest_reviews'),
    url(r'^review/(?P<review_id>\w+)/$', views.review_detail, name='review_detail'),
    url(r'^review/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<review>[-\w]+)/$', views.review_detail_slug, name='review_detail_slug'),
    url(r'^review/tag/(?P<tag_slug>[-\w]+)/$', views.review_list, name='review_list_by_tag'),
    url(r'^review/repo//(?P<repo_id>\w+)/$', views.reviews_by_repo, name='reviews_by_repo'),
	# ex: /review/user - get reviews for the logged user
    url(r'^review/user/(?P<username>\w+)/$', views.user_review_list, name='user_review_list'),
    url(r'^review/user/$', views.user_review_list, name='user_review_list'),
	# Projects: /repo/
    url(r'^repo$', views.repo_list, name='repo_list'),
    url(r'^repo/search/$', views.search, name='search_repo'),
    url(r'^repo/user/$', views.user_repo_list, name='user_repo_list'),
    url(r'^repo/user/(?P<username>\w+)/$', views.user_repo_list, name='user_repo_list'),
    url(r'^repo/tag/(?P<tag_slug>[-\w]+)/$', views.repo_list, name='repo_list_by_tag'),
    # ex: /repo/5/
    url(r'^repo/(?P<repo_id>\w+)/$', views.repo_detail, name='repo_detail'),
    url(r'^repo/(?P<repo_id>\w+)/add_review/$', views.add_review, name='add_review'),

]