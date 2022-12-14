from django.db import models


# Create your here.
class result(models.Model):
    Id_Patient=models.CharField(max_length=10)
    Prediction=models.IntegerField()
    Type=models.TextField()
    
def _str_(self):
    return self.Id_Patient
    