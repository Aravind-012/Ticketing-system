from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User


# class Ticket(models.Model):
#     subject = models.CharField(max_length=200)
#     requester_name = models.CharField(max_length=100)
#     requester_email = models.EmailField()
#     requester_phone = models.CharField(max_length=20, blank=True, null=True)
#     priority = models.CharField(
#         max_length=10,
#         choices=[("High", "High"), ("Medium", "Medium"), ("Low", "Low")]
#     )
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = "ticket_list"   # ✅ custom table name 


# 2
# class Ticket(models.Model):
#     STATUS_CHOICES = [
#         ("Pending", "Pending"),
#         ("Work in Process", "Work in Process"),
#         ("Completed", "Completed"),
#     ]

#     subject = models.CharField(max_length=200)
#     requester_name = models.CharField(max_length=100)
#     requester_email = models.EmailField()
#     requester_phone = models.CharField(max_length=20, blank=True, null=True)
#     priority = models.CharField(
#         max_length=10,
#         choices=[("High", "High"), ("Medium", "Medium"), ("Low", "Low")]
#     )
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")  # New field added
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = "ticket_list"


#     def __str__(self):
#         return f"{self.subject} - {self.priority}"

# 3
class Ticket(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Work in Process", "Work in Process"),
        ("Completed", "Completed"),
    ]

    PRIORITY_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    subject = models.CharField(max_length=200)
    requester_name = models.CharField(max_length=100)
    requester_email = models.EmailField()
    requester_phone = models.CharField(max_length=20, blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    sla_due_at = models.DateTimeField(null=True, blank=True)  # Add SLA due date field
    is_escalated = models.BooleanField(default=False)  # Whether ticket is escalated
    assigned_to = models.CharField(max_length=50, blank=True, null=True)
    assigned_phone = models.CharField(max_length=20, blank=True, null=True)


    class Meta:
        db_table = "ticket_list"

    # def save(self, *args, **kwargs):
    #     # Calculate SLA due date on creation or if missing
    #     if not self.sla_due_at:
    #         if self.priority == "High":
    #             self.sla_due_at = self.created_at + timedelta(hours=4)
    #         elif self.priority == "Medium":
    #             self.sla_due_at = self.created_at + timedelta(days=1)
    #         elif self.priority == "Low":
    #             self.sla_due_at = self.created_at + timedelta(days=3)
    #     super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)  # created_at is now set
        if is_new and not self.sla_due_at:
            if self.priority == "High":
                self.sla_due_at = self.created_at + timedelta(hours=4)
            elif self.priority == "Medium":
                self.sla_due_at = self.created_at + timedelta(days=1)
            elif self.priority == "Low":
                self.sla_due_at = self.created_at + timedelta(days=3)
            super().save(update_fields=["sla_due_at"])


    def __str__(self):
        return f"{self.subject} - {self.priority}"
    
class ClientOnboarding(models.Model):
    client_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    plan = models.CharField(max_length=50)
    assigned_to = models.CharField(max_length=50)
    assigned_phone = models.CharField(max_length=20, blank=True, null=True)  # New field
    onboarding_deadline_days = models.IntegerField(default=7)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.client_name
