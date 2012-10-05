from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
import datetime
import locale

from posts.models import Post

def index(request):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

    main_post = Post.objects.latest('pub_date')
    latest_posts = Post.objects.all().order_by('-pub_date')[1:6]
   
    return render_to_response('posts/index.html', 
    {
    'datetime': datetime.datetime.now().strftime('%H:%M, %A, %b %Y'),
    'latest_posts': latest_posts,
    'main_post': main_post
    }, 
    context_instance=RequestContext(request))

def detail(request, post_id):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

    post = get_object_or_404(Post, pk=post_id)
   
    return render_to_response('posts/detail.html', 
    {
    'datetime': datetime.datetime.now().strftime('%H:%M, %A, %b %Y'),
    'post': post
    }, 
    context_instance=RequestContext(request))
    
def archive(request):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

    latest_posts = Post.objects.all().order_by('-pub_date')
   
    return render_to_response('posts/index.html', 
    {
    'datetime': datetime.datetime.now().strftime('%H:%M, %A, %b %Y'),
    'latest_posts': latest_posts
    }, 
    context_instance=RequestContext(request))