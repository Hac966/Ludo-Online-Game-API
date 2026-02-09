from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Sessions
from .serializers import SessionsSerializer, UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SessionsViewSet(viewsets.ModelViewSet):
    queryset = Sessions.objects.all()
    serializer_class = SessionsSerializer
    lookup_field = 'name'

    # 1. Action for the Die Roll
    # URL: /sessions/{name}/{p_name}/roll/{die}/
    @action(detail=True, methods=['get', 'post'], url_path=r'(?P<p_name>\w+)/roll/(?P<die>\d+)')
    def roll_die(self, request, name=None, p_name=None, die=None):
        session = self.get_object()

        # Uses p_name exactly as Java sends it
        setattr(session, f'{p_name}DieNumber', int(die))
        session.save()

        return Response({"status": "Die updated"})

    # 2. Action for the Piece Move
    # URL: /sessions/{name}/{p_name}/move/{piece}/
    @action(detail=True, methods=['get', 'post'], url_path=r'(?P<p_name>\w+)/move/(?P<piece>\w+)')
    def move_piece(self, request, name=None, p_name=None, piece=None):
        session = self.get_object()

        # Uses p_name exactly as Java sends it
        setattr(session, f'{p_name}MovedPiece', piece)
        session.save()

        return Response({"status": "Piece moved"})


@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')

        if User.objects.filter(username=u).exists():
            return JsonResponse({"error": "Username taken"}, status=400)

        user = User.objects.create_user(username=u, email=e, password=p)
        return JsonResponse({"status": "success", "username": u})
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        if user:
            # This starts the session for the WebView
            login(request, user)
            return JsonResponse({"status": "success", "username": u})
        return JsonResponse({"error": "Invalid login"}, status=401)