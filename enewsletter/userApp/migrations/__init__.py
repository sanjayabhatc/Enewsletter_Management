from django.db import migrations
from django.db import models

def populate_departments(apps, schema_editor):
    Department = apps.get_model('yourappname', 'Department')
    CHOICES = [
        ("Computer Science",),
        ("Computer Science(IT)",),
        ("Electronics",),
        ("Data Science",),
    ]
    for choice in CHOICES:
        Department.objects.create(name=choice[0])

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.RunPython(populate_departments),
    ]