from django.urls import path, include
from moviesapp.views import (
    TestAppAPIView,
    RegistrationAPIView,
    LoginView,
    LogoutView,
    UserAPIView,
    CredyMoviesAPIView,
    # UserCollectionView,
    MoviesCollectionView,
    DeleteCollectionView,
    RequstCounterView,
)

app_name = "moviesapp"


urlpatterns = [
    path("test/", TestAppAPIView.as_view(), name="moviesapp"),
    path("register/", RegistrationAPIView.as_view(), name="register-api"),
    path("login/", LoginView.as_view(), name="login-api"),
    path("logout/", LogoutView.as_view(), name="logout-api"),
    path("list/users/", UserAPIView.as_view(), name="user-api"),
    path("movies/", CredyMoviesAPIView.as_view(), name="credy-movies"),
    # path("collection/", UserCollectionView.as_view(), name="user-collection"),
    path("collections/", MoviesCollectionView.as_view(), name="movie-collection"),
    path("collection/delete", DeleteCollectionView.as_view(), name="delete-collection"),
    path("request-count/", RequstCounterView.as_view(), name="request-count"),
    path(
        "request-count-reset/", RequstCounterView.as_view(), name="request-count-reset"
    ),
]
