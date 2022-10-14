import requests
import jwt


# Django imports
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import logout
from django.http import JsonResponse

# Rest Framework imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView

# local imports
from moviesapp.models import User, Collection, Movie
from moviesapp.serializers import UserCreateSerializer, UserListSerializer
from moviesapp.utils import generate_jwt_token
from moviesapp.tasks import add
from moviesapp.middleware.request_middleware import NO_OF_REQUESTS_SERVED


class TestAppAPIView(APIView):
    def get(self, request, format=None):
        try:
            result = add.delay(11, 15)
            print(result)
            return Response(
                {"status": True, "Response": "Successfully Tested"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class RegistrationAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer

    __doc__ = "Registration API for user"

    def post(self, request, *args, **kwargs):

        try:
            user_serializer = self.serializer_class(data=request.data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                data = generate_jwt_token(user, user_serializer.data)
                return Response(data, status=status.HTTP_200_OK)
            else:
                message = ""
                for error in user_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response(
                    {"status": False, "message": message},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer

    __doc__ = "Log In API for user which returns token"

    @staticmethod
    def post(request):

        try:
            serializer = JSONWebTokenSerializer(data=request.data)
            if serializer.is_valid():
                serialized_data = serializer.validate(request.data)
                user = User.objects.get(email=request.data.get("email"))
                return Response(
                    {
                        "status": True,
                        "token": serialized_data["token"],
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                message = ""
                for error in serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response(
                    {"status": False, "message": message},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except (AttributeError, ObjectDoesNotExist):
            return Response(
                {"status": False, "message": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        """
        Logout API for user
        """
        try:
            user = request.user
            logout(request)
            return Response(
                {"status": True, "message": "logout successfully"},
                status=status.HTTP_200_OK,
            )
        except (AttributeError, ObjectDoesNotExist):
            return Response({"status": False}, status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(GenericAPIView):
    serializer_class = UserListSerializer

    def get(self, request, format=None):
        """
        List all the users.
        """

        try:
            users = User.objects.all()
            user_serializer = UserListSerializer(users, many=True)

            users = user_serializer.data
            return Response(
                {"status": True, "Response": users}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class CredyMoviesAPIView(APIView):
    def get(self, request):
        """
        To get the list of movies from the integrated third party api
        """

        baseUrl = "https://demo.credy.in/api/v1/maya/movies/"
        try:
            response = requests.get(baseUrl)
            result = {"data": response.json()}
            return Response(result)
        except requests.exceptions.JSONDecodeError:
            print("Server Timeout error")
        except Exception as error:
            print("The Credy api has failed")
        except IOError as e:
            print("Broken pipe error")
        return Response({})


# class UserCollectionView(APIView):
#     NO_OF_REQUESTS_SERVED += 1
#     permission_classes = (IsAuthenticated,)

#     @staticmethod
#     def get(request):
#         """
#         To get the collection of all the movies of a user
#         """

#         print("Request data: ", request.META.get("HTTP_AUTHORIZATION"))
#         print()
#         print("Token: ", str(request.META.get("HTTP_AUTHORIZATION")))

#         authToken = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
#         print("Token: ", authToken)
#         decodedToken = jwt.decode(authToken, verify=False)
#         print("Decoded Token: ", decodedToken)
#         return {"data": request.user}
#         return JsonResponse(
#             {"data": Collection.objects.filter(user_id=loggedInUser.id)}
#         )


class MoviesCollectionView(APIView):
    def get(self, request):
        """
        To get all the movies under a given collection
        """

        collection_id = request.GET["collection_uuid"]
        collectionObj = list(Collection.objects.filter(id=collection_id).values())
        moviesList = list(Movie.objects.filter(coll_id=collection_id).values())

        finalObj = {
            "title": collectionObj[0]["title"],
            "description": collectionObj[0]["description"],
            "movies": moviesList,
        }
        return Response(finalObj)


class DeleteCollectionView(APIView):
    def post(self, request):
        """
        To delete a given collection
        """

        collection_id = request.GET.get("collection_uuid")
        recordsToDelete = Collection.objects.filter(id=collection_id)
        return Response(recordsToDelete.delete())


class RequstCounterView(APIView):
    def get(self, request):
        """
        To count the number of requests served
        """
        global NO_OF_REQUESTS_SERVED

        finalObj = {"no_of_requests": NO_OF_REQUESTS_SERVED}
        return Response(finalObj)

    def post(self, request):
        """
        To reset the number of requests served
        """

        finalObj = {"no_of_requests": NO_OF_REQUESTS_SERVED}
        return Response(finalObj)
