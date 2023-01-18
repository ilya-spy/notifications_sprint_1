from typing import Dict, List

from django.http import JsonResponse
from django.views.generic.list import BaseListView
from movies.models import FilmWork, PersonFilmWork, RoleType

from ..schemas import Movie, MoviesList


class MoviesApi(BaseListView):
    http_method_names = ["get"]
    paginate_by = 50

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context, status=200 if context else 204)


class DetailedMovieApi(MoviesApi):
    @staticmethod
    def get_genres(movie) -> List[str]:
        return [genre for genre in movie.genre.values_list("name", flat=True)]

    @staticmethod
    def get_team(qs) -> Dict[str, List[str]]:
        result = {role.value: [] for role in RoleType}
        for row in qs:
            result[row.role].append(row.person.full_name)

        return result

    def get_queryset(self):
        query = PersonFilmWork.objects.filter(
            film_work__id=self.kwargs.get("id")
        ).select_related("film_work", "person")

        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        query = self.get_queryset()
        if query:
            movie = query.first().film_work
            genres = self.get_genres(movie=movie)
            team = self.get_team(qs=query)

            response = Movie(
                id=movie.id,
                title=movie.title,
                description=movie.description,
                creation_date=movie.creation_date,
                rating=movie.rating,
                type=movie.type,
                genres=genres,
                **team
            ).dict()

            return response

        return {}


class ListMoviesApi(DetailedMovieApi):
    def get_queryset(self):
        return FilmWork.objects.prefetch_related("person", "genre").all()

    def get_roles(self, movie):
        pfw = PersonFilmWork.objects.filter(film_work_id=movie.id)
        return {
            role.value: list(
                pfw.filter(role=role.value).values_list("person__full_name", flat=True)
            )
            for role in RoleType
        }

    def get_films(self, qs):
        movies = []
        for movie in qs:
            team = self.get_roles(movie)
            movies.append(
                Movie(
                    id=movie.id,
                    title=movie.title,
                    description=movie.description,
                    creation_date=movie.creation_date,
                    rating=movie.rating,
                    type=movie.type,
                    genres=self.get_genres(movie),
                    **team
                )
            )

        return movies

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()

        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, self.paginate_by
        )

        resp = MoviesList(
            count=paginator.count,
            total_pages=paginator.num_pages,
            prev=page.previous_page_number() if page.has_previous() else None,
            next=page.next_page_number() if page.has_next() else None,
            results=self.get_films(queryset),
        ).dict()

        return resp
