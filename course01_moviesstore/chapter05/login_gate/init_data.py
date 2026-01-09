import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def main():
    admin, _ = User.objects.get_or_create(username="admin")
    admin.is_staff = True
    admin.is_superuser = True
    admin.set_password("admin123456")
    admin.save()

    alice, _ = User.objects.get_or_create(username="alice")
    alice.is_staff = False
    alice.is_superuser = False
    alice.set_password("alice123456")
    alice.save()

    print("✅ 初始化完成")
    print("admin / admin123456")
    print("alice / alice123456")

if __name__ == "__main__":
    main()