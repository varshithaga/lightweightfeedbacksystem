from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class User(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def clean(self):
        if self.role == 'manager' and not self.username.endswith('@manager'):
            raise ValidationError("Manager username must end with @manager")
        if self.role == 'employee' and not self.username.endswith('@employee'):
            raise ValidationError("Employee username must end with @employee")

    def save(self, *args, **kwargs):
        self.full_clean()  # run clean() before saving
        super().save(*args, **kwargs)


class Feedback(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks_received')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks_given')
    strengths = models.TextField()
    areas_to_improve = models.TextField()
    sentiment = models.CharField(max_length=10, choices=[('positive', 'Positive'), ('neutral', 'Neutral'), ('negative', 'Negative')])
    acknowledged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback from {self.manager.username} to {self.employee.username} - {self.sentiment}'
