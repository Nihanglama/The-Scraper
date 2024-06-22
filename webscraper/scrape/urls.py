from django.urls import path
from .views import main,images,links,table,custome


urlpatterns=[
    path("",main,name='main'),
    path("imagescraping",images,name='imagescrape'),
    path("linkscraping",links,name='linkscrape'),
    path('tablescraping',table,name='tablescrape'),
    path('customescraping',custome,name='customescrape')

]