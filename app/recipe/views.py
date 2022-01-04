from rest_framework import authentication, permissions, viewsets, mixins
from recipe.serializers import TagSerializer, IngredientSerializer
from core.models import Tag, Ingredient


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    serializer_class = TagSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Tag.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ Create a new Tag """
        serializer.save(user=self.request.user)


class IngredientViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    serializer_class = IngredientSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
