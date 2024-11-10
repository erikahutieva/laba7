from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Good, Token
from .serializers import GoodSerializer

# Представление для получения токена
def get_token(request):
    new_token = Token.objects.create()
    return JsonResponse({"token": str(new_token.key)})

def home(request):
    return HttpResponse("Welcome to the shop API")
# Представление для списка товаров
class GoodsListView(APIView):
    def get(self, request):
        # Проверка токена
        token = request.GET.get('token')
        if not token:
            return HttpResponse("Token must be present", status=401)
        if not Token.objects.filter(key=token).exists():
            return HttpResponse("Token is invalid", status=401)

        # Получение списка товаров
        goods = Good.objects.all()
        serializer = GoodSerializer(goods, many=True)
        return Response(serializer.data)

# Представление для создания нового товара
class NewGoodView(APIView):
    def post(self, request):
        # Проверка токена
        token = request.GET.get('token')
        if not token:
            return HttpResponse("Token must be present", status=401)
        if not Token.objects.filter(key=token).exists():
            return HttpResponse("Token is invalid", status=401)

        # Создание нового товара
        serializer = GoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  
