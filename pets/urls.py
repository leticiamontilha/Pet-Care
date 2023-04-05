from django.urls import path
from .views import PetViews, PetDetaisView

urlpatterns = [
    path("pets/", PetViews.as_view()),
    path("pets/<int:pet_id>/", PetDetaisView.as_view())
]