# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        admin = settings.ADMINS[0]
        username = admin[0]
        email = admin[1]
        password = User.objects.make_random_password(length=14)

        try:
            User.objects.get(username=username)
            print "Admin {} already exists".format(username)
        except User.DoesNotExist:
            u = User.objects.create_user(username, email, password)
            u.is_staff = True
            u.is_superuser = True
            u.save()
            print 'Created admin with username {} and password {}'.format(
                username,
                password
            )
