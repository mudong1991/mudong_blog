# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-date_publish'], 'verbose_name': '\u6587\u7ae0', 'verbose_name_plural': '\u6587\u7ae0', 'permissions': [('can_view', 'Can see article'), ('can_add', 'Can add article'), ('can_edit', 'Can edit article'), ('can_delete', 'Can delete article')]},
        ),
    ]
