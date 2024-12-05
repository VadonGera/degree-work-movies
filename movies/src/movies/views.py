import logging

from django.db.models import Avg, Max
from django.db.models.functions import Round
from django.shortcuts import render

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Movie, MediaType, Country, Genre, Rating, Review

# Настраиваем логгер для приложения "movies"
logger = logging.getLogger("movies")


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Диапазон оценок от 1 до 10
        context["rating_range"] = range(1, 11)

        # Текущая оценка пользователя (если он авторизован)
        if self.request.user.is_authenticated:
            user_rating = Rating.objects.filter(
                movie=self.object, user=self.request.user
            ).first()
            context["user_rating"] = user_rating.value if user_rating else None

            # Текущая рецензия пользователя (если есть)
            user_review = Review.objects.filter(
                movie=self.object, user=self.request.user
            ).first()
            context["user_review"] = user_review
        else:
            context["user_rating"] = None
            context["user_review"] = None

        # Список рецензий
        context["reviews"] = Review.objects.filter(movie=self.object).order_by(
            "-updated_at"
        )

        return context


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


# def movie_detail(request, movie_id):
#     # Пример данных
#     movie = Movie.objects.get(pk=movie_id)
#     user_rating = 7  # Пример: оценка пользователя
#     user_review = None  # Пример: рецензия пользователя
#
#     context = {
#         "movie": movie,
#         "user_rating": user_rating,
#         "user_review": user_review,
#         "rating_range": range(1, 11),  # Диапазон оценок
#     }
#     return render(request, "movies/movie_detail.html", context)


@login_required
def rate_movie(request, pk):
    # Получаем фильм
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == "POST":
        rating_value = request.POST.get("rating")
        if rating_value and rating_value.isdigit():
            rating_value = int(rating_value)
            if 1 <= rating_value <= 10:  # Проверяем, что оценка в диапазоне 1-10
                # Ищем существующий рейтинг для пользователя
                rating, created = Rating.objects.get_or_create(
                    movie=movie, user=request.user, defaults={"value": rating_value}
                )
                if not created:
                    rating.value = rating_value  # Обновляем оценку
                    rating.save()
                    logger.info(
                        "Пользователь с id %s успешно изменил рейтинг к фильму с id %s",
                        request.user.id,
                        movie.pk,
                    )

    return redirect("movie_detail", pk=movie.pk)


@login_required
def review_movie(request, pk):
    # Получаем фильм
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == "POST":
        review_content = request.POST.get("review")
        if review_content:
            # Ищем существующую рецензию для пользователя
            review, created = Review.objects.get_or_create(
                movie=movie, user=request.user, defaults={"content": review_content}
            )
            if not created:
                review.content = review_content  # Обновляем рецензию
                review.save()
                logger.info(
                    "Пользователь с id %s успешно опубликовал рецензию на фильм с id %s",
                    request.user.id,
                    movie.pk,
                )

    return redirect("movie_detail", pk=movie.pk)
