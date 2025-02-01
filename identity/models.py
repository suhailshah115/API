from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
	email = models.EmailField(null=True,blank=True)
	phone = PhoneNumberField()
	created_at = models.DateTimeField(auto_now_add=True)
	primary_contact = models.ForeignKey('self', null=True,
		                                 blank=True, on_delete=models.SET_NULL,
		                                 related_name= 'linked_contacts' )

	def save(self,*args,**kwargs):
		if not self.primary_contact:
			self.primary_contact = self
		super.save(*args,**kwargs)