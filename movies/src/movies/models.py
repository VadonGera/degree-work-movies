from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from decimal import *
import math

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Жанр")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанр"
        ordering = ["name"]


class Director(models.Model):
    name = models.CharField(max_length=100, verbose_name="Режиссер")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Режиссер"
        verbose_name_plural = "Режиссеры"
        ordering = ["name"]


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name="Страна")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"
        ordering = ["name"]


class Actor(models.Model):
    name = models.CharField(max_length=100, verbose_name="Актер")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"
        ordering = ["name"]


class MediaType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Тип медиа")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип медиа"
        verbose_name_plural = "Типы медиа"
        ordering = ["name"]


class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название фильма")
    description = models.TextField(verbose_name="Описание фильма")
    trailer = models.URLField(verbose_name="Ссылка на трейлер")
    year = models.IntegerField(verbose_name="Год выхода")

    countries = models.ManyToManyField(Country, verbose_name="Страны", blank=True)
    genres = models.ManyToManyField(Genre, verbose_name="Жанры", blank=True)
    directors = models.ManyToManyField(Director, verbose_name="Режиссер", blank=True)
    actors = models.ManyToManyField(Actor, verbose_name="Актеры", blank=True)

    image = models.ImageField(
        upload_to="movies/", verbose_name="Изображение", blank=True, null=True
    )

    # Поле для внешней ссылки на изображение
    external_image_url = models.URLField(
        blank=True, null=True, verbose_name="URL изображения"
    )

    # Связь с моделью MediaType
    media_type = models.ForeignKey(
        MediaType, on_delete=models.CASCADE, verbose_name="Тип медиа", null=True
    )

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def clean(self):
        # Создадим валидатор для проверки URL
        validator = URLValidator()
        if self.external_image_url:
            try:
                validator(self.external_image_url)
            except ValidationError:
                raise ValidationError(
                    {"external_image_url": "Введённый URL недействителен."}
                )

    def get_image_url(self):
        """
        Возвращает URL для изображения: сначала пытается взять из поля `image`,
        затем из `external_image_url`. Если оба пустые — возвращает URL заглушки.
        """
        if self.image:
            return self.image.url
        elif self.external_image_url:
            return self.external_image_url
        return "/static/images/placeholder.png"  # Путь к изображению-заглушке

    def __str__(self):
        return self.title

    def average_rating(self):
        """Вычисляет средний рейтинг фильма"""
        ratings = self.ratings.all()
        if not ratings.exists():
            return None
        avg = sum(rating.value for rating in ratings) / ratings.count()
        return round(avg, 1)
        # return avg.quantize(Decimal("1.00"))
        # return math.ceil(avg)
        # return avg

    def rating_count(self):
        """Возвращает количество оценок для фильма"""
        return self.ratings.count()

    def review_count(self):
        """Возвращает количество рецензий для фильма"""
        return self.reviews.count()


class Rating(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 11)]  # Оценки от 1 до 10

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")
    value = models.IntegerField(choices=RATING_CHOICES, verbose_name="Рейтинг")

    class Meta:
        unique_together = ("user", "movie")
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинг"

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}: {self.value}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField(verbose_name="Рецензия")
    created_at = models.DateTimeField(auto_now_add=True)  # Устанавливается при создании
    updated_at = models.DateTimeField(
        auto_now=True
    )  # Обновляется при каждом сохранении

    class Meta:
        unique_together = ("user", "movie")
        verbose_name = "рецензия"
        verbose_name_plural = "рецензии"
        ordering = ["-created_at"]

    def __str__(self):
        media_type = (
            self.movie.media_type.name.lower()
            if self.movie.media_type
            else "unknown type"
        )
        return f"Рецензия '{self.user.username}' на {media_type} '{self.movie.title}'"
