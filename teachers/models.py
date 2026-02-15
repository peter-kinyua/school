from django.db import models

class Student(models.Model):
	admission_number = models.CharField(max_length=20, unique=True)
	name = models.CharField(max_length=200)
	current_class = models.CharField(max_length=100)
	password = models.CharField(max_length=128, default='changeme')
	def __str__(self):
		return f"{self.name} ({self.admission_number})"

from django.contrib.auth.models import User

class PastPaper(models.Model):
	title = models.CharField(max_length=200)
	file = models.FileField(upload_to='past_papers/')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	teacher = models.ForeignKey(User, on_delete=models.CASCADE)
	target_class = models.CharField(max_length=100)

	def __str__(self):
		return f"{self.title} ({self.target_class}) by {self.teacher.username}"

class ZoomLink(models.Model):
	class_name = models.CharField(max_length=200)
	zoom_link = models.URLField()
	added_at = models.DateTimeField(auto_now_add=True)
	teacher = models.ForeignKey(User, on_delete=models.CASCADE)
	target_class = models.CharField(max_length=100)

	def __str__(self):
		return f"{self.class_name} ({self.target_class}) by {self.teacher.username}"
