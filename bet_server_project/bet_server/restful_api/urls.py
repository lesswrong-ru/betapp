from django.conf.urls import patterns, url

urlpatterns = patterns(
        'restful_api.views',
        url(r'^bets/$', 'bet_list', name='bet_list'),
        url(r'^bets/(?P<pk>[0-9]+)$', 'bet_detail', name='bet_detail'),
        )
