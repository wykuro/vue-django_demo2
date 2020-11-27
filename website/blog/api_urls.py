from django.urls import path
from blog import api

urlpatterns = [
    path('add-article/', api.add_article),
    path('dweb-login/', api.dweb_login),
    path('dweb-register/', api.dweb_register),
    path('auto-login/', api.dweb_autoLogin),
    path('dweb-logout/', api.dweb_Logout),
    path('article-list', api.article_list),
    path('del-article', api.del_article),
    path('dweb-checkperm/', api.dweb_checkperm),
    path('dweb-group/', api.dweb_group),
    path('dweb-userlist/',api.dweb_userlist),
    path('article-data/',api.article_data),
]
