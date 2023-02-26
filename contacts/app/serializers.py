from rest_framework import serializers


class ContactSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    firstname = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)
    created_date = serializers.DateTimeField()
