from django.db import models

class RSVP(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    attending = models.BooleanField()
    partner = models.BooleanField()
    kids = models.IntegerField()
    
    def count_guests(self):
        if self.attending:
            return 1 + (1 if self.partner else 0) + self.kids
        return 0
    
    def status_str(self):
        if not self.attending:
            return "❌ kommt nicht"
        else:
            return (
                    f"[{self.count_guests()}] {self.name} kommt "
                f"{'mit Partner' if self.partner else 'allein'} "
                f"{f'und bringt Kinder: {self.kids}' if self.kids > 0 else ''}"
            ).strip()
    
    def __str__(self):
        return f"{self.name} - {self.status_str()}"