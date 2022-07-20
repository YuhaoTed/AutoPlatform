from django.db import models

# Create your models here.
from django.contrib.auth.models import User,AbstractUser

class UserAuto(AbstractUser):
    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11,null=True,unique=True)
    creatime =models.DateTimeField(verbose_name="注册时间",auto_now_add=True)
    authen = models.BooleanField(default=False)

class Project(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=12, unique=True)
class Function(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=12)#名字
    eng_name = models.CharField(max_length=10,unique=True)#英语名字
    project = models.ForeignKey(to='Project',to_field="nid",on_delete=models.SET_NULL,null=True)#对应项目
    user = models.ManyToManyField(to="UserAuto")#对应用户  多对多的关系
    class Meta:
        unique_together = ['name','project']
class Feature(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=12, unique=True)  # 名字
    eng_name = models.CharField(max_length=10, unique=True)  # 英语名字
    func = models.ForeignKey(to="Function",to_field="nid",on_delete=models.CASCADE)
    class Meta:
        unique_together = ['name','func']

class Case(models.Model):
    nid = models.AutoField(primary_key=True)#主键 序号
    name = models.CharField(max_length=12,unique=True)#名字
    desc = models.CharField(max_length=64)#描述
    ID = models.CharField(max_length=64)#自动拼接的ID 项目+模块+子feature+序号
    creatime = models.DateTimeField(verbose_name="注册时间", auto_now_add=True)#自动生成的创建时间
    detail = models.OneToOneField(to="Case_Detail",on_delete=models.CASCADE)
    user = models.ForeignKey(to='UserAuto', to_field='nid',on_delete=models.CASCADE,null=True)
    feature = models.ForeignKey(to='Feature',to_field='nid',on_delete=models.CASCADE,null=True)
    status = models.IntegerField(max_length=2,null=False)

class Case_Detail(models.Model):
    desc = models.JSONField(null=False)# 测试步骤描述
    test = models.IntegerField()# 测试预计执行情况

class SDS_Content(models.Model):
    nid = models.AutoField(primary_key=True)  # 主键 序号
    name = models.CharField(max_length=50, unique=True)  # 名字
    category = models.CharField(max_length=12)  # 种类
    content = models.FileField(upload_to='SDS/')
class ICON_Content(models.Model):
    nid = models.AutoField(primary_key=True)  # 主键 序号
    name = models.CharField(max_length=50, unique=True)  # 名字
    category = models.CharField(max_length=12)  # 种类
    content = models.FileField(upload_to='ICON/')