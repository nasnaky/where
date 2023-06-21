from django.db import models


class STATE(models.Model):
    user = models.ForeignKey('user.USER', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    where = models.TextField()
