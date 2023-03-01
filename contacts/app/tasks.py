import datetime
import random


import django.utils.timezone


from contacts.celery import app
from .contact import ContactManager


CONTACTS = [
    {
        "firstname": "Fred",
        "lastname": "Flinstone",
        "emails": [
            {"value": "fred.flinstone@gmail.com",},
            {"value": "fred.flinstone@abv.bg",},
        ],
    },
    {
        "firstname": "Wilma",
        "lastname": "Flintstone",
        "emails": [
            {"value": "wilma.flinstone@gmail.com",},
        ],
    },
    {
        "firstname": "Pebbles",
        "lastname": "Flinstone",
        "emails": [],
    },
    {
        "firstname": "Barney",
        "lastname": "Rubble",
        "emails": [
            {"value": "barney.rubble@gmail.com",},
        ],
    },
    {
        "firstname": "Betty",
        "lastname": "Rubble",
        "emails": [
            {"value": "betty.rubble@gmail.com",},
        ],
    },
    {
        "firstname": "Bamm Bamm",
        "lastname": "Rubble",
        "emails": [],
    },
]


@app.task
def generate_contact():
    manager = ContactManager()
    contact = random.choice(CONTACTS)
    return manager.create(contact["firstname"], contact["lastname"], contact["emails"])


@app.task
def delete_old_contacts():
    delete_before = django.utils.timezone.now() - datetime.timedelta(minutes=1)
    manager = ContactManager()
    cnt = 0
    for contact in manager.get_all():
        if contact.created_date < delete_before:
            manager.delete(contact.username)
            cnt += 1
    return cnt
