from django.test import TestCase
from .models import Genre, Director, Country, Actor, MediaType, Movie, Rating, Review
from django.contrib.auth import get_user_model

User = get_user_model()


class MoviesModelsTest(TestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.genre = Genre.objects.create(name="Action")
        self.director = Director.objects.create(name="John Doe")
        self.country = Country.objects.create(name="USA")
        self.actor = Actor.objects.create(name="Jane Smith")
        self.media_type = MediaType.objects.create(name="Movie")

        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test Description",
            year=2023,
            media_type=self.media_type,
            external_image_url="https://example.com/image.jpg",
        )
        self.movie.countries.add(self.country)
        self.movie.genres.add(self.genre)
        self.movie.directors.add(self.director)
        self.movie.actors.add(self.actor)

        self.user = User.objects.create_user(username="testuser", password="password")
        self.rating = Rating.objects.create(user=self.user, movie=self.movie, value=8)
        self.review = Review.objects.create(
            user=self.user, movie=self.movie, content="Great movie!"
        )

    def test_genre_creation(self):
        self.assertEqual(self.genre.name, "Action")

    def test_director_creation(self):
        self.assertEqual(self.director.name, "John Doe")

    def test_country_creation(self):
        self.assertEqual(self.country.name, "USA")

    def test_actor_creation(self):
        self.assertEqual(self.actor.name, "Jane Smith")

    def test_movie_creation(self):
        self.assertEqual(self.movie.title, "Test Movie")
        self.assertEqual(self.movie.year, 2023)
        self.assertIn(self.country, self.movie.countries.all())
        self.assertIn(self.genre, self.movie.genres.all())
        self.assertIn(self.director, self.movie.directors.all())
        self.assertIn(self.actor, self.movie.actors.all())

    def test_rating_creation(self):
        self.assertEqual(self.rating.value, 8)
        self.assertEqual(self.rating.movie, self.movie)
        self.assertEqual(self.rating.user, self.user)

    def test_review_creation(self):
        self.assertEqual(self.review.content, "Great movie!")
        self.assertEqual(self.review.movie, self.movie)
        self.assertEqual(self.review.user, self.user)

    def test_average_rating(self):
        # Добавляем ещё одну оценку
        Rating.objects.create(
            user=User.objects.create_user(username="testuser2"),
            movie=self.movie,
            value=6,
        )
        self.assertEqual(self.movie.average_rating(), 7.0)  # Среднее (8 + 6) / 2

    def test_review_count(self):
        self.assertEqual(self.movie.review_count(), 1)

    def test_get_image_url_with_local_image(self):
        # Тест локального изображения
        self.movie.image = "movies/local_image.jpg"
        self.movie.save()
        self.assertEqual(self.movie.get_image_url(), "/media/movies/local_image.jpg")

    def test_get_image_url_with_external_image(self):
        # Тест внешнего URL
        self.movie.image = None  # Удаляем локальное изображение
        self.assertEqual(self.movie.get_image_url(), "https://example.com/image.jpg")

    def test_get_image_url_with_placeholder(self):
        # Тест с пустыми полями
        self.movie.image = None
        self.movie.external_image_url = None
        self.assertEqual(self.movie.get_image_url(), "/static/images/placeholder.png")
