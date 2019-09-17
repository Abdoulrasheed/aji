from django.db import models

class Gate(models.Model):
	name = models.CharField(max_length=25)
	gate_number = models.IntegerField()

	class Meta:
		pass

	def __str__(self):
		return self.name