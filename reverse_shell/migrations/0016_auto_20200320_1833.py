# Generated by Django 3.0.4 on 2020-03-20 16:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reverse_shell', '0015_auto_20200301_2348'),
    ]

    operations = [
        migrations.AddField(
            model_name='attacker',
            name='owner',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, related_name='attackers', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='victim',
            name='owner',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, related_name='victims', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
