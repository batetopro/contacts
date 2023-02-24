from django.db import models


class Contact(models.Model):
    username = models.CharField(max_length=100, primary_key = True, editable = False)
    firstname = models.CharField(max_length=100, null=False)
    lastname = models.CharField(max_length=100, null=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}: {} {}".format(self.username, self.firstname, self.lastname)

    class Meta:
        ordering = ["firstname", "lastname"]
