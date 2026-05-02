from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        from django.db.models.signals import post_migrate
        from django.contrib.auth.models import User

        def create_admin(sender, **kwargs):
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@gmail.com',
                    password='admin'
                )

        post_migrate.connect(create_admin, sender=self)