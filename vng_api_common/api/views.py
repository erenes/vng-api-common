from rest_framework.generics import CreateAPIView

from ..models import JWTSecret
from .serializers import JWTSecretSerializer
from .scopes import SCOPE_MANAGE_CREDENTIALS


class CreateJWTSecretView(CreateAPIView):
    swagger_schema = None

    model = JWTSecret
    serializer_class = JWTSecretSerializer
    permission_classes = ()  # TODO: protect with auth as well
    required_scopes = SCOPE_MANAGE_CREDENTIALS
