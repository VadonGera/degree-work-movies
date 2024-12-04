from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.MovieListView.as_view(), name="movie_list"),  # Список фильмов
    path(
        "movie/<int:pk>/", views.MovieDetailView.as_view(), name="movie_detail"
    ),  # Детальная страница фильма
    path("login/", views.CustomLoginView.as_view(), name="login"),  # Авторизация
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "register/", views.CustomRegisterView.as_view(), name="register"
    ),  # Регистрация
    path("movie/<int:pk>/rate/", views.rate_movie, name="rate_movie"),
    path("movie/<int:pk>/review/", views.review_movie, name="review_movie"),
]
