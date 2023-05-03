from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer, DirectMessageSerializer, RelationSerializer, \
    UserRegisterSerializer, DirectMessageCreateSerializer, ProfileCreateSerializer, ChangePasswordSerializer
from rest_framework import status, generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import User, DirectMessage, Profile, Relation
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

class UserRegister(APIView):
    """""
    register a user
    """""
    serializer_class = UserRegisterSerializer
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    """""
    show all user
    """""
    def list(self, request):
        srz_data = UserSerializer(instance=self.queryset, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)
    """""
    show a particular user
    pk = user_id
    """""
    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        srz_data = UserSerializer(instance=user)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)
    """""
    update a user
    pk = user_id
    """""
    def partial_update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        if user != request.user:
            return Response({'permission denied': 'you are not the owner'})
        srz_data = UserSerializer(instance=user, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data, status=status.HTTP_200_OK)
        return Response(data=srz_data.errors)
    """""
    deactive a user
    pk = user_id
    """""
    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        if user != request.user:
            return Response({'permission denied': 'you are not the owner'})
        user.is_active = False
        user.save()
        return Response({'message': 'user deactivated'})

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated,]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"message":"Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageCreate(APIView):
    """""
    create a message
    pk = to_user
    """""
    permission_classes = [IsAuthenticated, ]
    serializer_class = DirectMessageCreateSerializer
    def post(self, request, pk):
        to_user = User.objects.get(id=pk)
        ser_data = DirectMessageCreateSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.save(from_user=request.user, to_user=to_user)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageView(APIView):
    """""
    show messages between 2 users
    pk = to_user
    """""
    permission_classes = [IsAuthenticated, ]
    serializer_class = DirectMessageSerializer
    def get(self, request, pk):
        to_user = get_object_or_404(User, pk=pk)
        from_user = User.objects.get(id=request.user.id)
        message1 = DirectMessage.objects.filter(to_user=to_user, from_user=from_user)
        message2 = DirectMessage.objects.filter(to_user=from_user, from_user=to_user)
        message = message1|message2
        srz_data = DirectMessageSerializer(instance=message, many=True)
        return Response(data=srz_data.data)

class MessageSetView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = DirectMessageSerializer
    queryset = DirectMessage.objects.all()
    """""
    update a message
    pk = message_id
    """""
    def partial_update(self, request, pk=None):
        message = get_object_or_404(self.queryset, pk=pk)
        to_user = message.to_user
        from_user = message.from_user
        if from_user != request.user:
            return Response({'permission denied': 'you cannot edit others messages'})
        srz_data = DirectMessageSerializer(instance=message, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save(from_user=from_user, to_user=to_user)
            return Response(data=srz_data.data)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
    """""
    delete a message
    pk = message_id
    """""
    def destroy(self, request, pk=None):
        message = get_object_or_404(self.queryset, pk=pk)
        from_user = message.from_user
        if from_user != request.user:
            return Response({'permission denied': 'you cannot delete others messages'})
        message.delete()
        return Response({'message': 'message deleted'})

class ProfileCreateView(APIView):
    """""
    create a profile
    """""
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProfileCreateSerializer
    def post(self, request):
        ser_data = ProfileCreateSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.save(user=request.user)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    """""
    show all profiles
    """""

    def list(self, request):
        srz_data = ProfileSerializer(instance=self.queryset, many=True)
        return Response(data=srz_data.data)

    """""
    show a particular profile
    pk = user_id
    """""

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(self.queryset, user=user)
        srz_data = ProfileSerializer(instance=profile)
        return Response(data=srz_data.data)
    """""
    update a profile
    pk=user_id
    """""

    def partial_update(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(self.queryset, user=user)
        if profile.user != request.user:
            return Response({'permission denied': 'you are not the owner'})
        srz_data = ProfileSerializer(instance=profile, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowView(APIView):
    """""
    follow and unfollow a user 
    pk=to_user
    """""
    permission_classes = [IsAuthenticated, ]
    serializer_class = RelationSerializer
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        already_followed = Relation.objects.filter(to_user=user, from_user=request.user).first()
        if not already_followed:
            new_follower = Relation(to_user=user, from_user=request.user)
            new_follower.save()
            follower_count = Relation.objects.filter(to_user=user).count()
            return Response({'status': 'Following', 'followers': follower_count}, status=status.HTTP_200_OK)
        else:
            already_followed.delete()
            follower_count = Relation.objects.filter(to_user=user).count()
            return Response({'status': 'unfollowed', 'followers': follower_count}, status=status.HTTP_200_OK)
        return redirect('/')







