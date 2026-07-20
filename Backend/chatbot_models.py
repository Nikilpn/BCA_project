from django.db import models
from Backend.models import roomtypedb, staffdb
from webapp.models import bookingdb

class ChatbotResponse(models.Model):
    """Store predefined chatbot responses for different query types"""
    QUERY_TYPES = [
        ('room', 'Room Query'),
        ('staff', 'Staff Query'),
        ('booking', 'Booking Query'),
        ('general', 'General Query'),
    ]
    
    query_type = models.CharField(max_length=20, choices=QUERY_TYPES)
    keyword = models.CharField(max_length=200, help_text="Keywords to match (comma-separated)")
    response = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_query_type_display()} - {self.keyword}"
    
    class Meta:
        ordering = ['-created_at']


class ChatbotConversation(models.Model):
    """Track user conversations with chatbot"""
    username = models.CharField(max_length=100, null=True, blank=True)
    user_message = models.TextField()
    bot_response = models.TextField()
    query_type = models.CharField(max_length=20, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-created_at']


class Notification(models.Model):
    """Store notifications for users"""
    NOTIFICATION_TYPES = [
        ('booking', 'Booking Confirmation'),
        ('cancellation', 'Booking Cancelled'),
        ('availability', 'Room Available'),
        ('price_drop', 'Price Drop'),
        ('system', 'System Alert'),
    ]
    
    username = models.CharField(max_length=100)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    related_object_id = models.IntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, null=True, blank=True)  # 'room', 'booking', etc.
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} - {self.title}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username', '-created_at']),
            models.Index(fields=['is_read', 'username']),
        ]
