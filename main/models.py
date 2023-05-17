from django.db import models
from django.contrib.auth.models import User
import uuid


class Category(models.Model):
	class Meta:
		verbose_name_plural = "Categories"
		
	name = models.CharField(max_length=20)
	
	def __str__(self):
		return self.name


class Group(models.Model):
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False
	)
	name = models.CharField(max_length=20)
	description = models.TextField()
	creator = models.ForeignKey(
		User, on_delete=models.CASCADE,
		related_name="owner")
	category = models.ForeignKey(
		Category, on_delete=models.CASCADE)
	participants = models.ManyToManyField(User, blank=True)
	
	def __str__(self):
		return self.name


class Message(models.Model):
	sender = models.ForeignKey(
		User, on_delete=models.CASCADE)
	group = models.ForeignKey(
		Group, on_delete=models.CASCADE)
	message = models.TextField()
	time_created = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.message

