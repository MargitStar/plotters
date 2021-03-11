from django.db import models


class Mold(models.Model):
    name = models.CharField(
        'Name',
        max_length=150,
        unique=True
    )

    def __str__(self):
        return f"Mold f{self.name}"
