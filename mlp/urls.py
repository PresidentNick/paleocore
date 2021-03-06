from django.conf.urls import patterns, url
from mlp import views as mlp_views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',

    # e.g. /mlp/upload/
    url(r'^upload/$', login_required(mlp_views.UploadKMLView.as_view(), login_url='/login/'), name="mlp_upload_kml"),
    url(r'^download/$', mlp_views.DownloadKMLView.as_view(), name="mlp_download_kml"),
    url(r'^confirmation/$', mlp_views.Confirmation.as_view(), name="mlp_upload_confirmation"),
    url(r'^upload/shapefile/', mlp_views.UploadView.as_view(), name="mlp_upload"),
    url(r'^change_xy/', mlp_views.ChangeXYView, name="change_xy"),

)
