
# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
import random, string, json
from shortener.models import Urls
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.core.context_processors import csrf
import sqlite3
 
def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('shortener/index.html', c)
 
def redirect_original(request):
    # url = get_object_or_404(Urls, pk=short_id) # get object, if not  found return 404 error
    # url.count += 1
    # url.save()
    # return HttpResponseRedirect(url.httpurl)
    short_url = request.POST.get('short_url')
    short_id = short_url - settings.SITE_URL
    url_entry_in_db = Urls.objects.filter(short_id = short_id)
    return HttpResponseRedirect(url_entry_in_db.httpurl)

 
def shorten_url(request):
    url = request.POST.get("url", '')
    # import pdb;pdb.set_trace()
    if not (url == ''):
        response_data = {}
        url_entry_in_db = Urls.objects.filter(httpurl=url)
        if url_entry_in_db:
            response_data['url'] = settings.SITE_URL+"/"+ url_entry_in_db[0].short_id
            return HttpResponse(json.dumps(response_data),  content_type="application/json")
        short_id = get_short_code()
        b = Urls(httpurl=url, short_id=short_id)
        b.save()
        response_data['url'] = settings.SITE_URL + "/" + short_id
        return HttpResponse(json.dumps(response_data),  content_type="application/json")
    return HttpResponse(json.dumps({"error": "error occurs"}), content_type="application/json")
 
def get_short_code():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if the randomly generated short_id is used then generate next
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        if not Urls.objects.filter(pk=short_id):
            return short_id
        else:
            pass

