from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from django.contrib import messages
from taggit.models import Tag

from .models import Review, Project
from .forms import ReviewForm
from .recommender import Recommender

import datetime

def homepage(request):
    homepage_review_list = Review.objects.order_by('-pub_date')[:4]
    context = {'homepage_review_list':homepage_review_list}
    return render(request,'recommendations/homepage.html', context)

@login_required
def dashboard(request):
    return render(request, 'recommendations/dashboard.html', {'section': 'dashboard'})

# User Views
@login_required
def editProfile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/editProfile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def active_user_list(request):
    users = User.objects.filter(is_active=True).order_by('-last_login')[:10]
    return render(request, 'recommendations/user/active_user_list.html', {'section': 'active_users',
                                                      'users': users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User,username=username, is_active=True)
    return render(request, 'recommendations/user/user_detail.html', {'section': 'active_users',
                                                        'user': user})													  	


# Review Views
    
def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'recommendations/review_list.html', context)

def latest_reviews(request, tag_slug=None):
    latest_review_list = Review.objects.order_by('-pub_date')
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        latest_review_list = latest_review_list.filter(tags__in=[tag])

    paginator = Paginator(latest_review_list, 6) 
    page = request.GET.get('page')
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:   
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
#    context = {'review_list':latest_review_list}
    return render(request, 'recommendations/last_reviews.html', {'reviews':reviews, 'page':page, 'tag': tag})


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'recommendations/review_detail.html', {'review': review})

def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    user = get_object_or_404(User, username=username)
    latest_review_list = Review.objects.filter(user_name=user).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'recommendations/user_review_list.html', context)
	

def review_detail_slug(request, year, month, day, review):
    review = get_object_or_404(Review, slug=review, status='published', publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'recommendations/review_detail_slug.html', {'review': review})


#Project Views
def repo_list(request, tag_slug=None):
    repo_list = Project.objects.order_by('-created_at')
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        repo_list  = repo_list.filter(tags__in=[tag])	

    paginator = Paginator(repo_list, 8) 
    page = request.GET.get('page')
    try:
        repos = paginator.page(page)
    except PageNotAnInteger:   
        repos = paginator.page(1)
    except EmptyPage:
        repos = paginator.page(paginator.num_pages)
    return render(request, 'recommendations/repo_list.html', {'repos':repos, 'page':page, 'tag': tag})


def repo_detail(request, repo_id):
    repo = get_object_or_404(Project, pk=repo_id)
    repo_tags_ids = repo.tags.values_list('id', flat=True)
    similar_repos = Project.objects.filter(tags__in=repo_tags_ids).exclude(id=repo.id).exclude(forked_from=repo.id)
    similar_repos = similar_repos.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]
    r = Recommender()
    recommended_projects = r.suggest_projects_for([repo], 4)
    return render(request, 'recommendations/repo_detail.html', {'repo': repo, 'similar_repos':similar_repos, 'recommended_projects':recommended_projects})

def reviews_by_repo(request, repo_id):
    if not repo_id:
        repo_id = request.repo.id
    repo_review_list = Review.objects.filter(repo=repo_id).order_by('-pub_date')
    repo_tags_ids = repo.tags.values_list('id', flat=True)
    similar_repos = Project.objects.filter(tags__in=repo_tags_ids).exclude(id=repo.id)
    similar_repos = similar_repos.annotate(same_tags=Count('tags')).order_by('-same_tags','-user_name')[:4]
    return render(request, 'recommendations/repo_review_detail.html', {'latest_review_list':latest_review_list, 'repo': repo, 'similar_repos':similar_repos})

@login_required
def add_review(request, repo_id):
    repo = get_object_or_404(Project, pk=repo_id)
    user_id = request.user.id
    user = get_object_or_404(User, pk=user_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        title = form.cleaned_data['title']
        comment = form.cleaned_data['comment']
        status = form.cleaned_data['status']		
#        user_name = form.cleaned_data['user_name']
        
        review = Review()
        review.repo = repo
        review.user_name = user
        review.rating = rating
        review.title = title
        review.comment = comment
        review.status = status
        review.pub_date = datetime.datetime.now()
        review.save()
        return HttpResponseRedirect(reverse('recommendations:repo_detail', args=(repo.id,)))

    return render(request, 'recommendations/add_repo_review.html', {'repo': repo, 'form': form})

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['name', 'description',])
        
        found_entries = Project.objects.filter(entry_query).order_by('-created_at')

    return render_to_response('search/search_results.html',
                          { 'query_string': query_string, 'found_entries': found_entries },
                          context_instance=RequestContext(request))
