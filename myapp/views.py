from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import LoginSerializer
from rest_framework import views, status, viewsets
from .models import Reason, Record, Agent
from .serializers import  ReasonSerializer, RecordSerializer, AgentSerializer

class AgentListView(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

class ReasonListView(viewsets.ModelViewSet):
    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer

class RecordListView(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    
    
class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Authenticate the user
            user = authenticate(username=username, password=password)
            if user is not None:
                # Retrieve the agent object
                agent = Agent.objects.filter(user=user).first()

                if agent:
                    phone_numbers = list(agent.phone_numbers.values_list("number", flat=True))
                else:
                    phone_numbers = []

                # Generate or retrieve token
                token, _ = Token.objects.get_or_create(user=user)

                return Response({
                    "message": "Login successful",
                    "token": token.key,
                    "userid": user.id,
                    "numbers": phone_numbers  # Return the list of phone numbers
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

