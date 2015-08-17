from django.contrib.auth.models import User
[u.delete() for u in User.objects.all()]
