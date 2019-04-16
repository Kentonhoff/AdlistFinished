from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings

class Cat(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Name must be greater than 1 character")]
    )
    foods = models.CharField(max_length=300)
    weight = models.PositiveIntegerField()
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Comment',
       related_name='cat_comments')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
       related_name='cat_owner')
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        return self.name

class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
       related_name='cat_comment_owner')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'
