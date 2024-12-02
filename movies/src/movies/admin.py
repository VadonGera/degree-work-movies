from django.contrib import admin
from .models import Movie, Genre, Director, MediaType, Rating, Review

from django.contrib.auth.admin import UserAdmin


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "genre", "director", "media_type")
    search_fields = (
        "title",
        "director__name",
    )  # Позволяет искать по названию фильма и имени режиссера
    list_filter = ("genre", "year")


@admin.register(MediaType)
class MediaTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "value")
    list_filter = ("value",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
