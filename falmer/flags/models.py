from django.db import models

FLAG_MODE = (
    ('FORCE', 'Force'),
    # ('DYNAMIC', 'Dynamic'),
)


class Flag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    description = models.TextField(default='')
    state = models.BooleanField(default=False, verbose_name='Enabled')
    mode = models.CharField(max_length=12, choices=FLAG_MODE, default=FLAG_MODE[0][0])

    expired = models.BooleanField(default=False)

    def __str__(self):
        return self.name
