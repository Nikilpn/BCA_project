from django.db import models
from Backend.models import roomnamedb

# Create your models here.
class customercontactdb(models.Model):
    CONTACTNAME = models.CharField(max_length=100, null=True, blank=True)
    CONTACTNUMBER = models.CharField(max_length=15, null=True, blank=True)  # Fixed: CharField for phone
    CONTACTEMAIL = models.EmailField(max_length=100, null=True, blank=True)
    CONTACTSUBJECT = models.CharField(max_length=200, null=True, blank=True)
    CONTACTMESSAGE = models.TextField(null=True, blank=True)  # Fixed: TextField for long messages
    
    def __str__(self):
        return self.CONTACTNAME or "No Name"


class Registerdb(models.Model):
    USERNAME = models.CharField(max_length=100, null=True, blank=True)
    PASSWORD = models.CharField(max_length=100, null=True, blank=True)  # ⚠️ Should be hashed!
    CONFIRMPASSWORD = models.CharField(max_length=100, null=True, blank=True)
    EMAIL = models.EmailField(max_length=100, null=True, blank=True)  # Fixed: EmailField
    
    def __str__(self):
        return self.USERNAME or "No Username"


class bookingdb(models.Model):
    # ✅ ForeignKey #2 (Optional but recommended)
    CUSTOMER = models.ForeignKey(Registerdb, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    
    CUSTOMERNAME = models.CharField(max_length=100, null=True, blank=True)
    CONTACTEMAIL = models.EmailField(max_length=100, null=True, blank=True)
    CHECKIN = models.DateField(null=True, blank=True)  # Fixed: DateField
    CHECKOUT = models.DateField(null=True, blank=True)  # Fixed: DateField
    TOTALADULTS = models.IntegerField(null=True, blank=True)  # Fixed: IntegerField
    TOTALCHILDS = models.IntegerField(null=True, blank=True)  # Fixed: Removed max_length
    
    # ✅ ForeignKey #3 (CRITICAL!)
    SELECTROOM = models.ForeignKey(roomnamedb, on_delete=models.CASCADE, null=True, blank=True, related_name='bookings')
    
    SPECIALREQUEST = models.TextField(null=True, blank=True)  # Fixed: TextField
    TOTALPRICE = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.CUSTOMERNAME} - {self.SELECTROOM}"


class Totaldb(models.Model):
    # ✅ ForeignKey #4 (Optional but recommended)
    BOOKING = models.ForeignKey(bookingdb, on_delete=models.CASCADE, null=True, blank=True, related_name='totals')
    
    CUSTOMERNAME = models.CharField(max_length=100, null=True, blank=True)
    MOBILE = models.CharField(max_length=15, null=True, blank=True)  # Fixed: CharField for phone
    TOTALPRICE = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.CUSTOMERNAME} - ₹{self.TOTALPRICE}"