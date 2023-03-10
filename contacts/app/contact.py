import uuid
import json
import logging


from kafka import KafkaConsumer, KafkaProducer


from .models import Contact, Email


KAFKA_TOPIC = "contacts"
KAFKA_GROUP = "contacts_bot"
LOGGER = logging.getLogger(__name__)


class ContactCallbackBackend:
    @property
    def topic(self):
        return KAFKA_TOPIC

    @property
    def group(self):
        return KAFKA_GROUP

    @property
    def consumer(self):
        return self._consumer

    @property
    def manager(self):
        return self._manager

    @property
    def email_manager(self):
        return self._email_manager

    def __init__(self):
        self._consumer = KafkaConsumer(self.topic, group_id=self.group)
        self._callbacks = {
            "create_contact": self.create_contact,
            "update_contact": self.update_contact,
            "delete_contact": self.delete_contact,
        }
        self._manager = ContactManager()
        self._email_manager = EmailManager()

    def run(self):
        for row in self.consumer:
            message = json.loads(row.value.decode())
            cmd = message["_cmd_"]
            del message["_cmd_"]

            if cmd not in self._callbacks:
                LOGGER.error("Invalid command: {}".format(cmd))
                continue

            LOGGER.info("Calling callback {} with message {} ...".format(cmd, message))
            try:
                self._callbacks[cmd](message)
            except Exception as ex:
                LOGGER.exception(ex)

    def create_contact(self, message):
        emails = self.email_manager.get_emails_by_values(message["emails"])
        del message["emails"]

        contact = Contact(**message)
        contact.save()

        for email in emails:
            contact.emails.add(email)
        contact.save()

    def update_contact(self, message):
        contact = self.manager.get_by_username(message["username"])
        contact.firstname = message["firstname"]
        contact.lastname = message["lastname"]

        if message.get("emails") is not None:
            contact.emails.clear()
            for email in self.email_manager.get_emails_by_values(message["emails"]):
                contact.emails.add(email)
        contact.save()

    def delete_contact(self, message):
        contact = self.manager.get_by_username(message["username"])
        contact.delete()


class ContactManager:
    @property
    def topic(self):
        return KAFKA_TOPIC

    @property
    def producer(self):
        return self._producer

    def __init__(self):
        self._producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode("utf-8"))

    def get_all(self):
        return Contact.objects.all()

    def get_by_username(self, username):
        return Contact.objects.get(username=username)

    def create(self, firstname, lastname, emails=()):
        username = str(uuid.uuid4())
        message = {
            "_cmd_": "create_contact",
            "username": username,
            "firstname": firstname,
            "lastname": lastname,
            "emails": emails,
        }

        self.producer.send(self.topic, value=message)
        self.producer.flush()

        return username

    def update(self, username, firstname, lastname, emails=None):
        message = {
            "_cmd_": "update_contact",
            "username": username,
            "firstname": firstname,
            "lastname": lastname,
            "emails": emails,
        }

        self.producer.send(self.topic, value=message)
        self.producer.flush()

    def delete(self, username):
        message = {
            "_cmd_": "delete_contact",
            "username": username,
        }

        self.producer.send(self.topic, value=message)
        self.producer.flush()


class EmailManager:
    def get_emails_by_values(self, emails):
        result = []
        for item in emails:
            email = Email.objects.get_or_create(value=item["value"])[0]
            result.append(email)
        return result
