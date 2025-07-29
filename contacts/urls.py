from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_contact, name="add_contact"),
    path("list/", views.contact_list, name="contact_list"),
    path("search/", views.contact_search, name="contact_search"),
    path("city-list/", views.city_list, name="city_list"),
    path("state-list/", views.state_list, name="state_list"),
    path("country-list/", views.country_list, name="country_list"),
    path("type-list/", views.contact_type_list, name="contact_type_list"),
    path(
        "communication-method/",
        views.preferred_communication_list,
        name="preferred_communication_list",
    ),
    path("<int:pk>/", views.contact_details, name="contact_details"),
    path("<int:pk>/update/", views.contact_update, name="contact_update"),
    path("<int:pk>/delete/", views.contact_delete, name="contact_delete"),
]
