""
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Cube(models.Model):
    length = models.IntegerField(help_text="Length of Box", default=0)
    width = models.IntegerField(help_text="Width of Box", default=0)
    height = models.IntegerField(help_text="Height of Box", default=0)
    area = models.IntegerField(help_text="Area of Box", default=0)
    volume = models.IntegerField(help_text="Volume of Box", default=0)
    created_by = models.ForeignKey(
        User,
        related_name="created_by",
        on_delete=models.CASCADE,
        help_text="User Created",
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.pk)

    def get_area(self):
        return 2 * (
            (self.length * self.width)
            + (self.length * self.height)
            + (self.width * self.height)
        )

    def get_volume(self):
        return self.length * self.width * self.height

    def save(self, *args, **kwargs):
        self.area = self.get_area()
        self.volume = self.get_volume()
        self.updated_on = datetime.now()
        super(Cube, self).save(*args, **kwargs)
