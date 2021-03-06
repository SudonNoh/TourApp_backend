from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        
        if email is None:
            raise TypeError("User must have an email address.")
        
        if password is None:
            raise TypeError("User must have a password.")
        
        user = self.model(
            email = self.normalize_email(email),
            **extra_fields
        )
        
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        
        if email is None:
            raise TypeError("Superuser must have an email address.")
        
        if password is None:
            raise TypeError("Superuser must have a password.")
        
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.save()
        
        return user
        