from django.db import models
from users.models import User


class SupportTicket(models.Model):
    CATEGORY_CHOICES = [
        ('BOOKING', 'Booking / Ticketing Issue'),
        ('REFUND', 'Cancellation & Refund'),
        ('PNR', 'PNR Status / Waitlist'),
        ('CATERING', 'e-Catering Complaint'),
        ('PAYMENT', 'Payment / Transaction Issue'),
        ('ACCOUNT', 'Account / Login Issue'),
        ('DELAY', 'Train Delay / Cancellation'),
        ('OTHER', 'Other'),
    ]
    PRIORITY_CHOICES = [
        ('NORMAL', 'Normal'), ('URGENT', 'Urgent'), ('CRITICAL', 'Critical'),
    ]
    STATUS_CHOICES = [
        ('OPEN', 'Open'), ('IN_PROGRESS', 'In Progress'),
        ('AWAITING_USER', 'Awaiting User Response'),
        ('RESOLVED', 'Resolved'), ('CLOSED', 'Closed'),
    ]
    ticket_id = models.CharField(max_length=15, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15, blank=True)
    pnr = models.CharField(max_length=10, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='NORMAL')
    subject = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    assigned_to = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Ticket {self.ticket_id} — {self.category} [{self.status}]"

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            import random, string
            self.ticket_id = 'IRCTC' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)


class TicketReply(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='replies')
    sender = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class FAQ(models.Model):
    SECTION_CHOICES = [
        ('BOOKING', 'Booking'), ('PAYMENT', 'Payment & Refund'),
        ('PNR', 'PNR & Status'), ('ACCOUNT', 'Account'),
        ('CATERING', 'e-Catering'), ('GENERAL', 'General'),
    ]
    question = models.CharField(max_length=300)
    answer = models.TextField()
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, default='GENERAL')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['section', 'order']

    def __str__(self):
        return self.question[:80]
