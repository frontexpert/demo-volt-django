# Generated by Django 4.0.1 on 2022-01-17 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_rol', models.CharField(max_length=30)),
                ('description_rol', models.CharField(max_length=100)),
                ('estado_rol', models.IntegerField()),
                ('usuario_creacion', models.IntegerField()),
                ('fecha_creacion', models.DateTimeField()),
                ('usuario_actualizacion', models.IntegerField()),
                ('fecha_actualizacion', models.DateTimeField()),
                ('ip_creacion', models.CharField(max_length=40)),
                ('ip_actualizacion', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('codigo_usuario', models.CharField(max_length=20)),
                ('clave_usuario', models.CharField(max_length=20)),
                ('dni_usuario', models.CharField(max_length=8)),
                ('nombres_usuario', models.CharField(max_length=100)),
                ('apellido_paterno', models.CharField(max_length=100)),
                ('apellido_materno', models.CharField(max_length=100)),
                ('tipo_usuario', models.IntegerField(default=1)),
                ('correo_empresa', models.EmailField(max_length=255)),
                ('correo_personal', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('estado_usuario', models.IntegerField(default=1)),
                ('usuario_creacion', models.IntegerField(default=0)),
                ('fecha_creacion', models.DateTimeField(null=True)),
                ('usuario_actualizacion', models.IntegerField(default=0)),
                ('fecha_actualizacion', models.DateTimeField(null=True)),
                ('ip_creacion', models.CharField(max_length=40)),
                ('ip_actualizacion', models.CharField(max_length=40)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staf status')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('role', models.ForeignKey(default=3, on_delete=django.db.models.deletion.DO_NOTHING, to='home.role')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
