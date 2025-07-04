from django.db import models

# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    usertype= models.CharField(max_length=100, null=True, blank=True)

class User_Model(models.Model):
    LOGINID = models.ForeignKey(Login, on_delete=models.CASCADE, null=True, blank=True)
    abbreviation = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    cancer_type = models.CharField(max_length=100, null=True, blank=True)
    cancer_stage = models.CharField(max_length=100, null=True, blank=True)
    treatment = models.CharField(max_length=100, null=True, blank=True)
    profile = models.FileField(upload_to='user_profiles/', null=True, blank=True)

class Instructions_Model(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(null=True, blank=True)

class SpontaniousQuestion(models.Model):
    Main_category = models.CharField(max_length=100, null=True, blank=True)
    Sub_category = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, help_text="This is the correct answer / category.")
    option1 = models.CharField(max_length=100, help_text="Wrong option 1", null=True, blank=True)
    option2 = models.CharField(max_length=100, help_text="Wrong option 2", null=True, blank=True)
    option3 = models.CharField(max_length=100, help_text="Wrong option 3", null=True, blank=True)
    option4 = models.CharField(max_length=100, help_text="Wrong option 4", null=True, blank=True, default='Neutral')
    image = models.ImageField(upload_to='Spontanious_question_images/', help_text="Upload image for the question.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question - {self.category}"
    

class SpontaniousResult(models.Model):
    USERID = models.ForeignKey(User_Model, on_delete=models.CASCADE, null=True, blank=True)
    QUESTIONID = models.ForeignKey(SpontaniousQuestion, on_delete=models.CASCADE, null=True, blank=True)
    response_time = models.FloatField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    # total_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PostQuestion(models.Model):
    category = models.CharField(max_length=100, help_text="This is the correct answer / category.")
    option1 = models.CharField(max_length=100, help_text="Wrong option 1", null=True, blank=True)
    option2 = models.CharField(max_length=100, help_text="Wrong option 2", null=True, blank=True)
    option3 = models.CharField(max_length=100, help_text="Wrong option 3", null=True, blank=True)
    option4 = models.CharField(max_length=100, help_text="Wrong option 3", null=True, blank=True)
    option5 = models.CharField(max_length=100, help_text="Wrong option 3", null=True, blank=True)
    option6 = models.CharField(max_length=100, help_text="Wrong option 4", null=True, blank=True, default='Neutral')
    image = models.ImageField(upload_to='Post_question_images/', help_text="Upload image for the question.")
    created_at = models.DateTimeField(auto_now_add=True)

class PostResult(models.Model):
    USERID = models.ForeignKey(User_Model, on_delete=models.CASCADE, null=True, blank=True)
    QUESTIONID = models.ForeignKey(PostQuestion, on_delete=models.CASCADE, null=True, blank=True)
    response_time = models.FloatField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    # total_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)