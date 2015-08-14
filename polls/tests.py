from datetime import timedelta
from django.utils import timezone
from django.test import TestCase

from .models import Question

class QuestionMethodsTest(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + timedelta(days=31)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_questoin(self):
        time = timezone.now() - timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertTrue(recent_question.was_published_recently())

