from django.contrib.auth.base_user import BaseUserManager



class UserManager(BaseUserManager):
    use_in_migration=True


    def create_user(self,username,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Email is required")
        user=self.model(username=username,email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,username,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)
        return self.create_user(username,email,password,**extra_fields)

        