from datetime import timedelta
from django.utils import timezone
from django.test import TestCase

from .models import Question

class QuestionMethodsTest(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + timedelta(days=31)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.was_published_recently())
