from django.db.models import Avg, Max
from django.db.models.functions import Round
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Movie, MediaType, Country, Genre


class MovieListView(ListView):
    model = Movie
    template_name = "movies/movie_list.html"
    context_object_name = "movies"

    def get_queryset(self):
        queryset = Movie.objects.all()

        # Аннотация для среднего рейтинга
        # queryset = queryset.annotate(average_rating=Avg("ratings__value"))
        queryset = queryset.annotate(average_rating=Round(Avg("ratings__value"), 1))

        # Фильтры
        media = self.request.GET.get("media")
        country = self.request.GET.get("country")
        genre = self.request.GET.get("genre")
        year = self.request.GET.get("year")
        sort = self.request.GET.get(
            "sort", "title"
        )  # По умолчанию сортировка по названию

        if media:
            queryset = queryset.filter(media_type__id=media)
        if country:
            queryset = queryset.filter(countries__id=country)
        if genre:
            queryset = queryset.filter(genres__id=genre)
        if year:
            queryset = queryset.filter(year=year)

        # Сортировка
        if sort == "-average_rating":
            queryset = queryset.order_by("-average_rating")
        elif sort == "average_rating":
            queryset = queryset.order_by("average_rating")
        else:
            queryset = queryset.order_by(sort)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем данные для фильтров
        context["media_types"] = MediaType.objects.all()
        context["countries"] = Country.objects.all()
        context["genres"] = Genre.objects.all()
        context["years"] = (
            Movie.objects.values_list("year", flat=True).distinct().order_by("-year")
        )

        return context


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
