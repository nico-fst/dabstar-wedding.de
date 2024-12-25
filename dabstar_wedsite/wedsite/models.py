from django.db import models

class RSVP(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    attending = models.BooleanField()
    guests = models.IntegerField()
    message = models.TextField(null=True, blank=True)
    
    def status_str(self):
        if not self.attending:
            return "❌ kommt nicht"
        else:
            if self.guests == 0:
                return "✅ kommt alleine"
            else:
                return f"✅ kommt mit +{self.guests}"
    
    def __str__(self):
        return f"{self.name} - {self.status_str()}"