from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from django.views.generic import ListView, DetailView, UpdateView
from django.db.models import Count
from django.db.models import Q

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
from django.contrib.sites.shortcuts import get_current_site

from django.contrib import messages
from taggit.models import Tag

from .models import Review, Project, UserProfile
from .forms import ReviewForm, UserProfileForm,  UserEditForm
from django.forms.models import inlineformset_factory
from .recommender import Recommender
from .u_recommender import U_recommender
from .r_recommender import R_Recommender

import datetime
import operator


def homepage(request):
    homepage_review_list = Review.objects.order_by('-pub_date')[:2]
    context = {'homepage_review_list':homepage_review_list}
    return render(request,'recommendations/homepage.html', context)

@login_required
def dashboard(request):
    return render(request, 'recommendations/dashboard.html', {'section': 'dashboard'})

# User Views
@login_required
def edit_user(request, pk):
    user = User.objects.get(pk=pk)
 
    # prepopulate UserProfileForm with retrieved user values from above.
    user_form = UserEditForm(instance=user)
 
    # The sorcery begins from here, see explanation below
    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('company', 'location', 'type'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserEditForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)
 
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)
 
                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('user_detail')
 
        return render(request, 'recommendations/user/account_update.html', {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied


@login_required
def editProfile(request, username=None):
    if not username:
        username = request.user.username
    user = get_object_or_404(User, username=username)
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
    return render(request, 'recommendations/user/editProfile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def active_user_list(request):
    users = User.objects.filter(is_active=True).order_by('-last_login')
	
    paginator = Paginator(users, 6) 
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:   
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'recommendations/user/active_user_list.html', {'section': 'active_users',
                                                      'users': users, 'page':page})

@login_required
def user_detail(request, user_id):

    selected_user = get_object_or_404(User, pk=user_id, is_active=True)
    r = U_recommender()
    recommended_users = r.suggest_users(selected_user, 4)
    return render(request, 'recommendations/user/user_detail.html', {'section': 'active_users',
                                                        'selected_user': selected_user, 'recommended_users':recommended_users})													  	


# Review Views
    
def review_list(request, tag_slug=None):
    latest_review_list = Review.objects.order_by('pub_date')
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        latest_review_list = latest_review_list.filter(tags__in=[tag])

    paginator = Paginator(latest_review_list, 4) 
    page = request.GET.get('page')
    try:
        latest_review_list = paginator.page(page)
    except PageNotAnInteger:   
        latest_review_list = paginator.page(1)
    except EmptyPage:
        latest_review_list = paginator.page(paginator.num_pages)

    return render(request, 'recommendations/review_list.html', {'latest_review_list':latest_review_list, 'page':page, 'tag': tag})

def latest_reviews(request, tag_slug=None):
    latest_review_list = Review.objects.order_by('pub_date')[:9]
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        latest_review_list = latest_review_list.filter(tags__in=[tag])

    paginator = Paginator(latest_review_list, 4) 
    page = request.GET.get('page')
    try:
        latest_review_list = paginator.page(page)
    except PageNotAnInteger:   
        latest_review_list = paginator.page(1)
    except EmptyPage:
        latest_review_list = paginator.page(paginator.num_pages)
#    context = {'review_list':latest_review_list}
    return render(request, 'recommendations/last_reviews.html', {'latest_review_list':latest_review_list, 'page':page, 'tag': tag})


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


def reviews_by_repo(request, repo_id):
    if not repo_id:
        repo_id = request.repo.id
    repo = get_object_or_404(Project, id=repo_id)
    r = R_Recommender()
    recommended_projects = r.suggest_projects_for(repo, 4)
    latest_review_list = Review.objects.filter(repo=repo).order_by('-pub_date')
    return render(request, 'recommendations/repo_review_detail.html', {'latest_review_list':latest_review_list, 'repo': repo, 'recommended_projects':recommended_projects})


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
    similar_repos = Project.objects.filter(tags__in=repo_tags_ids).filter(forked_from=None).exclude(id=repo.id)
    similar_repos = similar_repos.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]
    r = Recommender()
    recommended_projects = r.suggest_projects_for(repo, 4)
    return render(request, 'recommendations/repo_detail.html', {'repo': repo, 'similar_repos':similar_repos, 'recommended_projects':recommended_projects})

def user_repo_list(request, username=None):
    if not username:
        username = request.user.username
    user = get_object_or_404(User, username=username)
    repos = Project.objects.filter(owner_id=user).order_by('-created_at')
    context = {'repos':repos, 'username':username}
    return render(request, 'recommendations/user_repo_list.html', context)
	
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

        review = Review()
        review.repo = repo
        review.user_name = user
        review.rating = rating
        review.title = title
        review.comment = comment

        review.pub_date = datetime.datetime.now()
        review.save()
        return HttpResponseRedirect(reverse('recommendations:repo_detail', args=(repo.id,)))

    return render(request, 'recommendations/add_repo_review.html', {'repo': repo, 'form': form})

def search_repo(request):
    query = ''
    results = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query = request.GET.get('q')
		
    results = Project.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)).order_by('created_at')

    return render(request, 'recommendations/search_results.html', { 'query': query, 'results': results})
	
def search_user(request):
    query = ''
    results = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query = request.GET.get('q')
		
    results = User.objects.filter(Q(username__icontains=query) | Q(last_name__icontains=query)).order_by('username')

    return render(request, 'recommendations/user/user_search_results.html', {'section': 'active_users', 'query': query, 'result': result})


class RepoSearchListView(ListView):
    """
    Display a Blog List page filtered by the search query.
    """
    paginate_by = 6

    def get_queryset(self):
        result = super(RepoSearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(description__icontains=q) for q in query_list))
            )

        return result

