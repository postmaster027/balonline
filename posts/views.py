from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
import datetime
import locale

from posts.models import Post
from cbrexchange.models import CBRExchange, Quote
from weather.models import GismeteoWeather, Forecast

def index(request):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    
    GismeteoWeather().refresh()

    main_post = False
    try:
        main_post = Post.objects.latest('pub_date')
    except:
        pass

    return render_to_response('posts/index.html', 
    {
    'datetime': datetime.datetime.now().strftime('%H:%M, %A, %b %Y'),
    'latest_posts': Post.objects.all().order_by('-pub_date')[1:6],
    'main_post': main_post,
    'quote': CBRExchange().refresh(),
    'forecasts': Forecast.objects.all().order_by('tstamp')
    }, 
    context_instance=RequestContext(request))

def detail(request, post_id):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

    main_post = get_object_or_404(Post, pk=post_id)
   
    return render_to_response('posts/detail.html', 
    {
    'datetime': datetime.datetime.now().strftime('%H:%M, %A, %b %Y'),
    'main_post': main_post
    }, 
    context_instance=RequestContext(request))
    
def archive(request):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

    latest_posts = Post.objects.all().order_by('-pub_date')
   
    return render_to_response('posts/archive.html', 
    {
    'datetime': datetime.datetime.now().strftime('%H:%M, %A, %b %Y'),
    'latest_posts': latest_posts
    }, 
    context_instance=RequestContext(request))
