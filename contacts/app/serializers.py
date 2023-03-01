from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    value = serializers.EmailField()


class ContactSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    firstname = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)
    created_date = serializers.DateTimeField()
    emails = EmailSerializer(read_only=True, many=True)
