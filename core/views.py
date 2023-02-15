import json
import datetime
from itertools import chain

from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, MessageSerializer, FriendSerializer, GroupSerializer, GroupMessageSerializer
from .models import User, UserToken, Message, Group, GroupMessage
from .authentication import create_access_token, create_refresh_token, decode_access_token


class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Login(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        if email == '' or password == '':
            raise exceptions.AuthenticationFailed('Invalid credentials')

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid credentials')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Invalid credentials')

        refresh_token = create_refresh_token(user.id)
        access_token = create_access_token(user.id)

        UserToken.objects.create(
            user_id=user.id,
            token=refresh_token,
            expired_at=datetime.datetime.utcnow() + datetime.timedelta(days=365)
        )

        response = Response()

        response.set_cookie(key='refresh_token',
                            value=refresh_token, httponly=True, samesite='None')
        response.set_cookie(key='access_token',
                            value=access_token, httponly=True, samesite='None')
        response.data = UserSerializer(user).data
        return response


class Logout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        response.data = "Logged out successfully!"
        return response


class GetUser(APIView):
    def get(self, request):
        token = request.COOKIES.get('access_token')
        user_id = decode_access_token(token)
        user = User.objects.filter(id=user_id).first()

        if user is None:
            raise exceptions.AuthenticationFailed('unauthenticated')

        userGroups = Group.objects.filter(members__id=user.id)
        userData = UserSerializer(user).data
        userData['groups'] = GroupSerializer(userGroups, many=True).data
        return Response(userData)


class HandleFriends(APIView):
    def get(self, request):
        users = User.objects.all()

        return Response(FriendSerializer(users, many=True).data)

    def post(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
            return Response(status=401)

        id = decode_access_token(token)
        user = User.objects.filter(pk=id).first()

        user.friends.add(User.objects.get(id=request.data['id']))

        userGroups = Group.objects.filter(members__id=user.id)
        userData = UserSerializer(user).data
        userData['groups'] = GroupSerializer(userGroups, many=True).data
        return Response(userData)


class RemoveFriend(APIView):
    def post(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
            return Response(status=401)

        id = decode_access_token(token)
        user = User.objects.filter(pk=id).first()

        user.friends.remove(User.objects.get(id=request.data['id']))

        userGroups = Group.objects.filter(members__id=user.id)
        userData = UserSerializer(user).data
        userData['groups'] = GroupSerializer(userGroups, many=True).data
        return Response(userData)


class UpdateUser(APIView):
    def post(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
            return Response(status=401)

        id = decode_access_token(token)
        user = User.objects.filter(pk=id).first()
        user.name = request.data['name']
        print(request.data['avatar'])
        if request.data['avatar'] != 'null':
            user.avatar = request.data['avatar']
        user.save()
        return Response(UserSerializer(user).data)


class HandleMessages(APIView):
    def post(self, request, by, to):
        serializer = MessageSerializer(data={
            "by": by,
            "to": to,
            "message": request.data['message']
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data)

    def get(self, request, by, to):
        messagesFromYou = Message.objects.filter(by=by, to=to)
        messagesFromOther = Message.objects.filter(to=by, by=to)
        messages = chain(messagesFromYou, messagesFromOther)

        return Response(MessageSerializer(messages, many=True).data)


class HandleGroup(APIView):
    def post(self, request):
        admin = User.objects.get(id=request.data['admin']['id'])
        groupOBJ = Group()
        groupOBJ.name = request.data['name']
        groupOBJ.admin = admin
        groupOBJ.save()
        for i in request.data['members']:
            groupOBJ.members.add(i)

        groupOBJ.save()
        return Response(GroupSerializer(groupOBJ).data)


class DeleteGroup(APIView):
    def post(self, request):
        group = Group.objects.filter(pk=request.data['id']).first()
        if (group):
            group.delete()
        return Response('Group deleted successfully!')


class UpdateGroup(APIView):
    def post(self, request):
        group = Group.objects.filter(pk=request.data['id']).first()
        group.name = request.data['name']
        if request.data['avatar'] != 'null':
            group.avatar = request.data['avatar']
        memberIDs = []
        for i in json.loads(request.data['members']):
            memberIDs.append(i['id'])
        group.members.set(memberIDs)
        group.save()
        return Response('Saved changes')

class LeaveGroup(APIView):
    def post(self, request):
        group = Group.objects.filter(pk=request.data['groupID']).first()
        group.members.remove(request.data['userID'])
        return Response('Left group successfully!')


class GroupMessages(APIView):
    def get(self, request, id):
        group = Group.objects.get(id=id)
        return Response(GroupMessageSerializer(group.messages, many=True).data)

    def post(self, request, id):
        group = Group.objects.get(id=id)
        by = User.objects.get(id=request.data['by']['id'])
        message = GroupMessage.objects.create(
            by=by, message=request.data['message'], roomID=request.data['roomID'])
        group.messages.add(message)
        # print(group)
        # group.save()
        return Response(GroupMessageSerializer(group.messages, many=True).data)
