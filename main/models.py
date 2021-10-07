from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass

# 以下を追加
class Talk(models.Model):
    # メッセージ
    talk = models.CharField(max_length=500)
    # 誰から
    talk_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="talk_from")
    # 誰に
    talk_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="talk_to")
    # 時間は
    time = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True とすると、そのフィールドの値には、オブジェクトが生成されたときの時刻が保存されます。

    def __str__(self):
        return "{}>>{}".format(self.talk_from, self.talk_to)