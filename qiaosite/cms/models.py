from djongo import models

class Blog(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

class Entry(models.Model):
    blog = models.EmbeddedField(
        model_container=Blog
    )    
    headline = models.CharField(max_length=255)   
