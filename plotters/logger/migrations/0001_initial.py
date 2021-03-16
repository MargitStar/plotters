# Generated by Django 3.1.7 on 2021-03-16 08:02

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mold', '__first__'),
        ('plotter', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlotterStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('cutouts', models.IntegerField()),
                ('last_cutout_date', models.DateField(default=datetime.date.today)),
                ('plotter', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='plotter.plotter')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MoldStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cutouts', models.IntegerField()),
                ('mold', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mold.mold')),
                ('plotter', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='plotter.plotter')),
            ],
        ),
        migrations.CreateModel(
            name='Cutout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(verbose_name='Time')),
                ('mold', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mold', to='mold.mold')),
                ('plotter', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='plotter', to='plotter.plotter')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
