from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Good, Token
from .serializers import GoodSerializer


def get_token(request):
    new_token = Token.objects.create() # метод для создания и сохранения нового экземпляра модели в базе данных.
    return JsonResponse({"token": str(new_token.key)})

def home(request):
    return HttpResponse("Добро пожаловать")

class GoodsListView(APIView):
    # для обработки GET-запросов
    def get(self, request):
        # Получение токена из параметров GET-запроса
        token = request.GET.get('token')
        if not token:
            return HttpResponse("Создайте токен", status=401)
        
        #  существование токена в базе данных
        if not Token.objects.filter(key=token).exists():
            return HttpResponse("Токена не существует", status=401)

        # список всех товаров из базы данных
        goods = Good.objects.all()
        
        # сложный формат в более простой списка товаров для отправки в JSON формате
        serializer = GoodSerializer(goods, many=True)
        return Response(serializer.data)

class NewGoodView(APIView):
    # для обработки POST-запросов
    def post(self, request):
        token = request.GET.get('token')
        if not token:
            return HttpResponse("Token must be present", status=401)
        if not Token.objects.filter(key=token).exists():
            return HttpResponse("Token is invalid", status=401)

        # сложный формат в более простой   для создания нового товара
        serializer = GoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Вернуть с кодом статуса 201 (Created)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # ошибки с кодом статуса 400 (Bad Request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
