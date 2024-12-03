from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Movie


class MovieListView(ListView):
    model = Movie
    template_name = "movies/movie_list.html"
    context_object_name = "movies"

    def get_queryset(self):
        return Movie.objects.all()  # Можно настроить фильтрацию


class MovieDetailView(DetailView):
    model = Movie
    template_name = "movies/movie_detail.html"
    context_object_name = "movie"


class CustomLoginView(LoginView):
    template_name = "movies/login.html"
    redirect_authenticated_user = True


class CustomRegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "movies/register.html"
    success_url = reverse_lazy("movie_list")

    def form_valid(self, form):
        # Автоматический вход после регистрации
        user = form.save()
        from django.contrib.auth import login

        login(self.request, user)
        return super().form_valid(form)
