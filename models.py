import django
from django.db import models
from django.utils import timezone
from users.models import SeamUser
from django.contrib.auth.models import User


class Lecture(models.Model):
    name_lecture = models.CharField(max_length=20, blank=True)
    # due_date = models.DateTimeField(blank=True, null=True) # 팀 결성되야 할 시간
    num_max = models.IntegerField()  #팀플 최대인원

    def __str__(self):
        return self.name_lecture


class BeforeTeam(models.Model):
    team_name = models.CharField(max_length=20)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    num_member = models.IntegerField()   #현재 팀원 수
    members_ability1 = models.BooleanField(default=False)
    members_ability2 = models.BooleanField(default=False)
    members_ability3 = models.BooleanField(default=False)
    members_ability4 = models.BooleanField(default=False)
    members_ability5 = models.BooleanField(default=False)
    kid = models.CharField(max_length=20)

    def __str__(self):
        return str(self.team_name)

# class after_team(models.Model):
#     team_name = models.CharField(max_length=20,blank=True)
#     numofmember = models.IntegerField() #결성된 팀원수
#     kid = models.ForeignKey('before_team', on_delete=models.CASCADE)

    # def make_team(self,):








