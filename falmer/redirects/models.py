from django.db import models

class Redirect(models.Model):
    ABSOLUTE = 'ABS'
    FORWARD = 'FWD'
    MODES = (
        (ABSOLUTE, 'Absolute'),
        (FORWARD, 'Forward'),
    )
    MARKETING = 'MARKETING'
    LEGACY = 'LEGACY'
    PURPOSE = (
        (MARKETING, 'Marketing'),
        (LEGACY, 'Legacy'),
    )
    # site = models.ForeignKey(Site, verbose_name='site', on_delete=models.CASCADE)
    from_path = models.CharField(max_length=255, db_index=True, null=False, blank=False)
    to_path = models.CharField(max_length=255, null=False, blank=False)
    mode = models.CharField(choices=MODES, max_length=20, default=FORWARD, null=False, blank=False)

    purpose = models.CharField(choices=PURPOSE, max_length=20)

    class Meta:
        verbose_name = 'redirect'
        verbose_name_plural = 'redirects'
        unique_together = (( 'from_path'),)
        ordering = ('from_path',)

    def __str__(self):
        return '{0} ---> {1}'.format(self.old_path, self.new_path)
