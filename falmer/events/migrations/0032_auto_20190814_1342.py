# Generated by Django 2.2.3 on 2019-08-14 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0031_auto_20180928_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='brandingperiod',
            name='display_from',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bundle',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.BrandingPeriod'),
        ),
        migrations.AddField(
            model_name='bundle',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='bundle',
            name='ticket_data',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='bundle',
            name='ticket_level',
            field=models.CharField(choices=[('NA', 'Not applicable'), ('LA', 'Limited availability'), ('SO', 'Sold out')], default='NA', max_length=2),
        ),
        migrations.AddField(
            model_name='bundle',
            name='ticket_type',
            field=models.CharField(choices=[('NA', 'n/a'), ('NT', 'Native'), ('EB', 'Eventbrite'), ('AC', 'ACCA'), ('GN', 'Generic'), ('MSL', 'MSL')], default='NA', max_length=3),
        ),
    ]
