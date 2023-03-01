from django.db import models


class Email(models.Model):
    value = models.EmailField(editable=False, null=False, unique=True)

    def __str__(self):
        return "{}".format(self.value)


class Contact(models.Model):
    username = models.CharField(max_length=100, primary_key=True, editable=False)
    firstname = models.CharField(max_length=100, null=False)
    lastname = models.CharField(max_length=100, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    emails = models.ManyToManyField(Email)

    def __str__(self):
        return "{}: {} {}".format(self.username, self.firstname, self.lastname)

    class Meta:
        ordering = ["firstname", "lastname"]
