from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta #追加部分

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
    
    def get_elapsed_time(self) -> str:
        # メッセージが生成されてから経った時間
        delta = timezone.now() - self.time
        zero_delta, hour_delta, day_delta, week_delta = (
            timedelta(),
            timedelta(hours=1),
            timedelta(days=1),
            timedelta(days=7),
        )
        if zero_delta < delta < hour_delta:
            return f"{int(delta.seconds // 60)}分前"

        elif hour_delta <= delta < day_delta:
            return f"{int(delta.seconds // (60 * 60))}時間前"

        elif day_delta <= delta < week_delta:
            return f"{int(delta.days)}日前"

        elif week_delta <= delta:
            return "1週間以上前"

        else:
            raise ValueError