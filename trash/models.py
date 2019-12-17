from django.db import models

class user_info(models.Model):
    nickname = models.CharField(max_length=20)
    password  = models.CharField(max_length=20)
    datetime = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    avatarsrc = models.CharField(max_length=50)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["datetime"]

class trash(models.Model):
    name = models.CharField(max_length=30)
    mtype = models.IntegerField()
    modify1 = models.CharField(max_length=50)
    modify2 = models.CharField(max_length=50)
    modify3 = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name) + ":" + str(self.mtype) + ":" + str(self.modify1)

    class Meta:
        ordering = ["name"]

class edit_history(models.Model):
    method = models.CharField(max_length=10)
    userid = models.IntegerField()
    name = models.CharField(max_length=30)
    mtype = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["datetime"]