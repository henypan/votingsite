from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

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

    
def create_question(question_text, days):
        time = timezone.now() + timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date=time)

    
class QuestionViewTests(TestCase):
    def test_index_view_with_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        create_question(question_text='past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: past question>']
        )

    def test_index_view_with_future_question_and_past_question(self):   
        create_question(question_text='past question', days=-30)
        create_question(question_text='future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: past question>']
        )

    def test_index_with_two_past_question(self):
        create_question(question_text='past question 1', days=-30)
        create_question(question_text='past question 2', days=-20)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: past question 2>', '<Question: past question 1>']
        )


class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        future_question = create_question(question_text='future question', days=20)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        past_question = create_question(question_text='past question', days=-20)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text, status_code=200)
        
