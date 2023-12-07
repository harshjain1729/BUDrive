from django.db import models
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _

#https://stackoverflow.com/a/58495709/12512406
class LowercaseEmailField(models.EmailField):
	def to_python(self, value):
		value = super(LowercaseEmailField, self).to_python(value)
		if isinstance(value, str):
			return value.lower()
		return value

class LowercaseCharField(models.CharField):
	def to_python(self, value):
		value = super(LowercaseCharField, self).to_python(value)
		if isinstance(value, str):
			return value.lower()
		return value

# https://stackoverflow.com/a/9016664/12512406
class RestrictedFileField(models.FileField):
	def __init__(self, *args, **kwargs):
		self.content_types = kwargs.pop("content_types", [])
		self.max_upload_size = kwargs.pop("max_upload_size", 0)

		super(RestrictedFileField, self).__init__(*args, **kwargs)

	def clean(self, *args, **kwargs):
		data = super(RestrictedFileField, self).clean(*args, **kwargs)

		file = data.file
		try:
			content_type = file.content_type
			if content_type in self.content_types:
				if file._size > self.max_upload_size:
					raise ValidationError(f'Please keep filesize under {filesizeformat(self.max_upload_size)}. Current filesize {filesizeformat(file._size)}')
			else:
				raise ValidationError('Filetype not supported.')
		except AttributeError:
			pass

		return data
