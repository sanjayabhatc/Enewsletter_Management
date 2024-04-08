from django.db import migrations

def add_department_data(apps, schema_editor):
    Department = apps.get_model('userApp', 'Department')
    department_names = [
        "Computer Science Engineering",
        "Information Technology",
        "Electronics and Communication Engineering",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Civil Engineering",
        "Chemical Engineering",
        "Aerospace Engineering",
        "Biomedical Engineering",
        "Environmental Engineering",
    ]

    for name in department_names:
        Department.objects.get_or_create(name=name)

class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0001_initial'),  # Make sure this reflects the actual dependency
    ]

    operations = [
        migrations.RunPython(add_department_data),
    ]
