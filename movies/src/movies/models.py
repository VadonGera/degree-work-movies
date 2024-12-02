from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Жанр")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанр"


class Director(models.Model):
    name = models.CharField(max_length=100, verbose_name="Режиссер")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Режиссер"
        verbose_name_plural = "Режиссеры"


class MediaType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Тип медиа")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип медиа"
        verbose_name_plural = "Типы медиа"


class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название фильма")
    description = models.TextField(verbose_name="Описание фильма")
    trailer = models.URLField(verbose_name="Ссылка на трейлер")
    year = models.IntegerField(verbose_name="Год выхода")
    # rating = models.CharField(max_length=5, verbose_name="Рейтинг")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name="Жанр")
    director = models.ForeignKey(
        Director, on_delete=models.CASCADE, verbose_name="Режиссёр"
    )
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

    def __str__(self):
        return self.title

    def average_rating(self):
        """Вычисляет средний рейтинг фильма"""
        ratings = self.ratings.all()
        if not ratings.exists():
            return None
        return sum(rating.value for rating in ratings) / ratings.count()

    def review_count(self):
        """Возвращает количество рецензий для фильма"""
        return self.reviews.count()


class Rating(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # Оценки от 1 до 5

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

    def __str__(self):
        return f"Review by {self.user.username} on {self.movie.title}"
