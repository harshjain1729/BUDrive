from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.utils.deconstruct import deconstructible

import uuid
import os

from .utils import get_email_verification_token
from .model_fields import LowercaseCharField, LowercaseEmailField, RestrictedFileField

# https://stackoverflow.com/a/61854214/12512406
@deconstructible
class AllowlistEmailValidator(EmailValidator):
	def validate_domain_part(self, domain_part):
		return False

	def __eq__(self, other):
		return isinstance(other, AllowlistEmailValidator) and super().__eq__(other)


def change_filename(instance, filename) :
	path = 'Resources'
	format = str(uuid.uuid4()) + '.' + filename.split('.')[-1]
	return os.path.join(path, format)


def change_filename_with_user(instance, filename) :
	path = str(instance.user.uid)
	format = str(uuid.uuid4()) + '.' + filename.split('.')[-1]
	return os.path.join(path, format)


class CustomUserManager(BaseUserManager):
	def create_user(self, email, username, password = None, is_active = True, is_admin = False):
		user = self.model(email = self.normalize_email(email), username = username, is_active = is_active, is_admin = is_admin)

		user.set_password(password)
		user.save(using = self._db)
		return user

	def create_superuser(self, email, username, password = None):
		return self.create_user(email = email, username = username, password = password, is_active = True, is_admin = True)

class CustomUser(AbstractBaseUser):
	uid = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True, editable = False)
	email = LowercaseEmailField(verbose_name = 'Email address', help_text = 'only BU emails', unique = True, max_length = 50, validators = [AllowlistEmailValidator(allowlist=['bennett.edu.in']), ])
	username = models.CharField(unique = True, max_length = 30, blank = False)

	email_verified = models.BooleanField(verbose_name = 'Email Verified?', default = False)
	email_verification_token = models.CharField(unique = True, max_length = 32, default = get_email_verification_token)

	date_joined = models.DateTimeField(auto_now_add = True)

	is_active = models.BooleanField(verbose_name = 'Is Active?', default = False)
	is_admin = models.BooleanField(verbose_name = 'Is Admin?', default = False)

	objects = CustomUserManager()
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ('email', )

	def __str__(self):
		return f'{self.username}'

	def has_perm(self, perm, obj = None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_admin

	@property
	def is_superuser(self):
		return self.is_admin


class UserDetails(models.Model) :
	user = models.OneToOneField(get_user_model(), related_name = 'details', on_delete = models.CASCADE, null = False, blank = False, editable = False)
	profile_picture = RestrictedFileField(upload_to = change_filename_with_user, null = True, blank = True, content_types = ['image/jpg', 'image/jpeg'], max_upload_size = 1 * 1024 * 1024)
	about_me = models.CharField(max_length = 200, default = '', blank = True)

	def __str__(self):
		return f'{self.user.username}'


@receiver(post_save, sender = get_user_model())
def create_user_profile(sender, instance, created, *args, **kwargs):
	if created:
		UserDetails.objects.get_or_create(user = instance)
	instance.details.save()


class Social(models.Model) :
	user_details = models.ForeignKey('UserDetails', related_name='socials', on_delete=models.CASCADE)
	name = models.CharField(max_length=20, null=False, blank=False)
	link = models.URLField(max_length=200, null=False, blank=False)

	class Meta :
		unique_together = ('user_details', 'name')

	def __str__(self) :
		return f'{self.user_details}-{self.name}'


class ResourceFile(models.Model) :
	uid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
	file = models.FileField(upload_to=change_filename, null=True, blank=True)
	name = models.CharField(max_length=30, null=False, blank=False)
	type = models.CharField(max_length=15, null=False, blank=False)

	def save(self, *args, **kwargs):
		if self._state.adding is True :
			self.name, self.type = self.file.name.rsplit('.', 1)
		super(ResourceFile, self).save(*args, **kwargs)

	def __str__(self):
		return f'{self.name}.{self.type}'


class UserFiles(models.Model):
	owner = models.ForeignKey(get_user_model(), related_name='owned_files', on_delete=models.SET_NULL, null=True)
	file = models.OneToOneField('ResourceFile', on_delete=models.CASCADE, null=False, blank=False)

	is_starred = models.BooleanField(default=False)
	is_trashed = models.BooleanField(default=False)
	is_deleted = models.BooleanField(default=False)

	shared_with = models.ManyToManyField(get_user_model(), related_name='shared_files')

	def __str__(self):
		return f'{self.owner} - {self.file}'


class Post(models.Model):
	uid = models.UUIDField(default=uuid.uuid4, editable=False)
	owner = models.ForeignKey(get_user_model(), related_name='posts', on_delete=models.SET_NULL, null=True)
	text = models.CharField(max_length=300, null=False, blank=False)
	file = models.OneToOneField('ResourceFile', on_delete=models.CASCADE, null=True, blank=True)
	tags = models.ManyToManyField('Tag', related_name='posts')
	created_at = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return f'{self.owner} - {self.uid}'


class Tag(models.Model):
	name = LowercaseCharField(max_length=20, unique=True, null=False, blank=False)

	def __str__(self):
		return f'{self.name}'


class Like(models.Model):
	user = models.ForeignKey(get_user_model(), related_name='likes', on_delete=models.SET_NULL, null=True)
	post = models.ForeignKey('Post', related_name='likes', on_delete=models.CASCADE)

	class Meta :
		unique_together = ('user', 'post')

	def __str__(self):
		return f'{self.user} - {self.post}'


class Comment(models.Model):
	user = models.ForeignKey(get_user_model(), related_name='comments', on_delete=models.SET_NULL, null=True)
	post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
	comment = models.CharField(max_length=50, null=False, blank=False)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user} - {self.post}'
