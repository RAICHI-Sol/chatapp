from datetime import timedelta

from main.forms import TalkForm
from main.models import Talk
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from main.models import User #追加箇所
# Create your tests here.

class TalkModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        now = timezone.now()
        cls._talk_30minutes_ago = Talk(time=now - timedelta(minutes=30))
        cls._talk_3hours_ago = Talk(time=now - timedelta(hours=3))
        cls._talk_3days_ago = Talk(time=now - timedelta(days=3))
        cls._talk_9days_ago = Talk(time=now - timedelta(days=9))
        cls._talk_3weeks_ago = Talk(time=now - timedelta(weeks=3))
        cls._talk_future = Talk(time=now + timedelta(weeks=3))

    def test_valid_elapsed_time(self):
        self.assertEqual(self._talk_30minutes_ago.get_elapsed_time(), "30分前")
        self.assertEqual(self._talk_3hours_ago.get_elapsed_time(), "3時間前")
        self.assertEqual(self._talk_3days_ago.get_elapsed_time(), "3日前")
        self.assertEqual(self._talk_9days_ago.get_elapsed_time(), "1週間以上前")
        self.assertEqual(self._talk_3weeks_ago.get_elapsed_time(), "1週間以上前")

    def test_invalid_elapsed_time(self):
        with self.assertRaises(ValueError):
            self._talk_future.get_elapsed_time()

class TalkFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._good_form = TalkForm({"talk": "こんにちは今日もプログラミングを頑張るぞ"})
        cls._bad_form1 = TalkForm({"talk": "君はあほだね"})
        cls._bad_form2 = TalkForm({"talk": "彼はバカというよりかはあほだ"})
        cls._bad_form3 = TalkForm({"talk": "テストばかりで疲れた"})

    def test_good_talk(self):
        self.assertTrue(self._good_form.is_valid())

    def test_bad_talk(self):
        self.assertFalse(self._bad_form1.is_valid())
        with self.assertRaisesMessage(ValidationError, "禁止ワード あほ が含まれています"):
            self._bad_form1.clean()

        self.assertFalse(self._bad_form2.is_valid())
        with self.assertRaisesMessage(ValidationError, "禁止ワード バカ, あほ が含まれています"):
            self._bad_form2.clean()

        self.assertFalse(self._bad_form3.is_valid())
        with self.assertRaisesMessage(ValidationError, "禁止ワード ばか が含まれています"):
            self._bad_form3.clean()


class SignupViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        return super().setUpClass()

    def test_get(self):
        res = self.client.get('http://127.0.0.1:8000/signup') #変更箇所
        self.assertEqual(res.status_code,200)
        self.assertTemplateUsed(res, "main/signup.html") #変更箇所

    def test_valid_post(self):
        params = {
            "username": "test太郎",
            "email": "test@example.com",
            "password1": "thisistest",
            "password2": "thisistest",
        }
        res = self.client.post('http://127.0.0.1:8000/signup', params) #変更箇所

        self.assertRedirects(
            res,
            "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_invalid_post(self):
        params = {
            "username": "test",
            "email": "メールアドレス",
            "password1": "thisistest",
            "password2": "thisistest",
        }
        res = self.client.post('http://127.0.0.1:8000/signup', params) #変更箇所
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "main/signup.html") #変更箇所

class TestsWithAuthMixin():
    """
    ログインが必要なテストクラスで継承する
    """

    @classmethod
    def setUpAuthData(cls):
        cls._username = "test太郎"
        cls._email = "test@example.com"
        cls._password = "thisistest"
        cls.user = User.objects.create_user(
            username=cls._username, email=cls._email, password=cls._password
        )

    def login(self):
        return self.client.login(
            username=self._username, password=self._password
        )

class TalkRoomViewTests(TestCase, TestsWithAuthMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._good_form = {"talk": "こんにちは今日もプログラミングを頑張るぞ"}
        cls._bad_form = {"talk": "彼はバカというよりかはあほだ"}

    @classmethod
    def setUpTestData(cls):
        cls.setUpAuthData()
        cls._friend_username = "friend太郎"
        cls._friend_email = "friend@example.com"
        cls._friend_password = "thisistest"
        cls._friend = User.objects.create_user(
            username=cls._friend_username,
            email=cls._friend_email,
            password=cls._friend_password,
        )
        cls._talk_room_url = f"http://127.0.0.1:8000/talk_room/{cls._friend.id}/" #変更箇所

    def test_get(self):
        self.login()
        res = self.client.get(self._talk_room_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "main/talk_room.html") #変更箇所

    def test_valid_post(self):
        self.login()
        res = self.client.post(self._talk_room_url, self._good_form)
        self.assertRedirects(
            res,
            self._talk_room_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_invalid_post(self):
        self.login()
        res = self.client.post(self._talk_room_url, self._bad_form)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "main/talk_room.html") #変更箇所
        self.assertContains(res, "禁止ワード バカ, あほ が含まれています")
