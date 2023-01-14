from . import models
from rest_framework.serializers import ModelSerializer


class FriendSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'name', 'avatar']


class UserSerializer(ModelSerializer):
    friends = FriendSerializer(many=True, required=False)

    class Meta:
        model = models.User
        fields = ['id', 'name', 'email', 'password', 'friends', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance

class MessageSerializer(ModelSerializer):
    class Meta:
        model = models.Message
        fields = ['id', 'by', 'to', 'message', 'date']

class GroupMessageSerializer(ModelSerializer):
    by = FriendSerializer()
    class Meta:
        model = models.GroupMessage
        fields = ['id', 'by', 'message', 'roomID', 'date']

class GroupSerializer(ModelSerializer):
    admin = UserSerializer()
    members = FriendSerializer(many=True)
    messages = GroupMessageSerializer(many=True)
    
    class Meta:
        model = models.Group
        fields = ['id', 'name', 'admin', 'members', 'messages', 'avatar']