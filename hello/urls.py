from django.urls import path
from hello import views

#NOTE display downloads list from newest to oldest
home_list_view = views.HomeListView.as_view(
    context_object_name="loads_list",
    template_name="hello/home.html",
)

urlpatterns= [ 
    path("", home_list_view, name="home"),
    path("fetch", views.fetch, name="fetch"),
    path("tablelayout/<file>/<int:rowNumber>", views.tablelayout, name="tablelayout"),
    path("showMore/<file>/<int:rowNumber>", views.showMore, name="tablelayout"),
    path("tableValCan/<file>/<int:rowNumber>", views.tableValCan, name="value_counts"),
]






