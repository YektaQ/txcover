from django.utils import timezone
from rest_framework import status

from rest_framework.permissions import (IsAuthenticated,IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category,Product,File
from .serializers import CategorySerializer,ProductSerializer,FileSerializer
