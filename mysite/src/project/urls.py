from django.conf.urls import patterns, url
from project import views

urlpatterns = patterns(
    '',
    url(r'^$', views.stations, name='home'),
    url(r'^project/$', views.stations),
    url(r'^project/about/$', views.about, name='project-about'),
    url(r'^project/example_post/$', views.example_post),
    url(r'^project/post_result/$', views.post_result),
    url(r'^project/following/$', views.view_following),
    url(r'^project/manage/$', views.manage),
    url(r'^project/manage/upload/$', views.upload),
    url(r'^project/manage/upload_result/$', views.upload_result),
    url(r'^project/manage/stations/$', views.manage_stations),
    url(r'^project/manage/stations_result/$', views.manage_stations_result),
    url(r'^project/station_details/([0-9]*)', views.station_details, name='project-station-details'),
    url(r'^project/device_details/([0-9]*)', views.device_details, name='project-device-details'),
    url(r'^project/download_reports/([0-9]*)', views.download_device_reports, name='project-download-reports'),
    url(r'^project/station/$', views.stations),
    url(r'^project/follow_unfollow/([0-9]*)', views.follow_unfollow, name='follow-unfollow'),
    url(r'^project/submit_search/(all|stations|devices)$', views.submit_search_query, name='project-submit-search'),
    url(r'^project/search_result/(all|stations|devices)/([a-zA-Z0-9]*)$', views.show_search_results, name='project-search-result'),
)
