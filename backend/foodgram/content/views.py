from django_filters.rest_framework import DjangoFilterBackend
from django_short_url.views import get_surl
from rest_framework import status, views, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly, SAFE_METHODS
)

from content.filters import (
    AuthorFilterBackend, IsFavoritedFilterBackend, IngredientNameFilterBackend,
    ShoppingCartFilterBackend, TagFilterBackend
)
from content.models import Ingredient, Recipe, Tag
from content.paginations import PaginateByPageLimit
from content.permissions import IsAuthorOrReadOnly
from content.serializers import (
    GetRecipeSerializer,
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer
)

LURL_URL_POS = 0
SHORT_ID_POS = 2
SAFE_ACTIONS = ('list', 'retrieve')


class ShortLinkView(views.APIView):

    def get(self, request, *args, **kwargs):
        lurl = request.path.split('get_link/')[LURL_URL_POS]
        surl = get_surl(lurl)
        path = f'{request.get_host()}{surl}'
        data = {
            'short-link': path
        }
        return Response(data=data, status=status.HTTP_200_OK)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ('get',)
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = PaginateByPageLimit
    filter_backends = (
        AuthorFilterBackend, IsFavoritedFilterBackend,
        ShoppingCartFilterBackend, TagFilterBackend,
    )
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action in SAFE_ACTIONS:
            return GetRecipeSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientNameFilterBackend
    pagination_class = None
    http_method_names = ('get',)
