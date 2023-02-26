from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser


from .models import Contact
from .contact import ContactManager
from .serializers import ContactSerializer


class ListContactsView(APIView):
    def get(self, request):
        """
        List all contacts
        """
        manager = ContactManager()
        contacts = manager.get_all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new contact
        """
        data = JSONParser().parse(request)
        if "firstname" not in data:
            return Response({"error": "The field 'firstname' is required"}, 400)

        if "lastname" not in data:
            return Response({"error": "The field 'lastname' is required"}, 400)

        # serializer = ContactSerializer(data=data)
        # serializer.is_valid(raise_exception=True)
        manager = ContactManager()
        username = manager.create(data["firstname"], data["lastname"])
        return Response({"username": username})


class GetContactView(APIView):
    def get(self, request, username):
        """
        Get a contact by username
        """
        manager = ContactManager()
        try:
            contact = manager.get_by_username(username)
        except Contact.DoesNotExist:
            return Response({"error": "Contact does not exist."}, 404)

        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    def put(self, request, username):
        """"
        Update a contact
        """
        manager = ContactManager()
        try:
            manager.get_by_username(username)
        except Contact.DoesNotExist:
            return Response({"error": "Contact does not exist."}, 404)

        data = JSONParser().parse(request)
        if "firstname" not in data:
            return Response({"error": "The field 'firstname' is required"}, 400)

        if "lastname" not in data:
            return Response({"error": "The field 'lastname' is required"}, 400)

        # serializer = ContactSerializer(data=data)
        # serializer.is_valid(raise_exception=True)

        manager.update(username, data["firstname"], data["lastname"])
        return Response({"username": username})

    def delete(self, request, username):
        """
        Delete a contact
        """
        manager = ContactManager()
        try:
            manager.get_by_username(username)
        except Contact.DoesNotExist:
            return Response({"error": "Contact does not exist."}, 404)

        manager.delete(username)
        return Response({"username": username})
