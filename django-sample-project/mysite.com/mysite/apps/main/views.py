#!usr/bin/python
# -*- coding:utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_http_methods
from main.models import Users


@require_http_methods(['GET'])
def load_main_page(request):
    """
    Load main page
    """
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))
