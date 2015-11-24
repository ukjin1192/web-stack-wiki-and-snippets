# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.views.generic import RedirectView


urlpatterns = patterns(
    'main.views',
    url(
        regex=r'^$',
        view='load_main_page'
    ),
)
