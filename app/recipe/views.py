from rest_framework import authentication, permissions, viewsets, mixins
from recipe.serializers import TagSerializer, IngredientSerializer
from core.models import Tag, Ingredient


class BaseRecipeAttrVieSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrVieSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrVieSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
