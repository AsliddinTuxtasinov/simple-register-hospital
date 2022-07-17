from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.urls import reverse


class UserManager(BaseUserManager):
    def create_user(self, email, tel_number, password=None):
        if not tel_number:
            raise ValueError('Users must have an telephone number')

        user = self.model(
            tel_number=tel_number,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, tel_number, password=None):
        user = self.create_user(
            email,
            password=password,
            tel_number=tel_number,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True)
    tel_number = models.CharField(max_length=55, unique=True)
    first_name = models.CharField(max_length=155, blank=True, null=True)
    last_name = models.CharField(max_length=155, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'tel_number'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.tel_number

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()


class SpecialDoctor(User):
    special_type = models.CharField(max_length=255)
    procedure_cost = models.PositiveIntegerField(verbose_name="The cost of a one-time procedure")

    def __str__(self):
        return f"{self.special_type} - {self.full_name}"

    def get_diseased(self):
        qs = self.diseased.all()
        return qs

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class DiseasedUser(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    telephone_number = models.CharField(max_length=55)
    email_address = models.EmailField()
    type_of_doctors = models.ForeignKey(to=SpecialDoctor, on_delete=models.CASCADE, blank=True,
                                        null=True, related_name='diseased')
    describe_your_condition = models.TextField(verbose_name="Brief information about your condition", max_length=300)
    time_procedure = models.PositiveIntegerField(verbose_name="How many times treatments do you want?")
    is_doctor_view = models.BooleanField(default=False)

    @property
    def total_cost_of_the_treatments(self):
        """ the total cost of the treatment """
        type_of_doctor = self.type_of_doctors
        if type_of_doctor:
            return self.time_procedure * type_of_doctor.procedure_cost
        return ""

    @property
    def full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_absolute_url(self):
        kwargs = {'pk': self.pk}
        return reverse('detail', kwargs=kwargs)

    def get_goto_doctor_url(self):
        kwargs = {'pk': self.pk}
        return reverse('goto-doctor', kwargs=kwargs)

    def get_status_diseased_url(self):
        kwargs = {'diseased_id': self.pk}
        return reverse('status-diseased-user', kwargs=kwargs)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Diseased User'
        verbose_name_plural = 'Diseased Users'


class StatusDiseasedUser(models.Model):
    class StatusType(models.TextChoices):
        ACCEPT = "Accept", "Accept"
        REFUSE = "Refuse", "Refuse"

    diseased = models.ForeignKey(to=DiseasedUser, on_delete=models.CASCADE, related_name="status_diseased")
    doctor = models.ForeignKey(to=SpecialDoctor, on_delete=models.CASCADE, related_name="doctor_status_diseased")
    status = models.CharField(max_length=10, choices=StatusType.choices)
    comment = models.TextField(max_length=300, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.status == self.StatusType.ACCEPT and not self.comment:
            self.comment = "Diseased is accept"
        elif self.status == self.StatusType.REFUSE and not self.comment:
            self.comment = "Diseased is refuse"
        super().save(*args, **kwargs)
