from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.courses.models import Course
import random

class QuestionBank(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Opción Múltiple'),
        ('true_false', 'Verdadero/Falso'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField('Pregunta')
    question_type = models.CharField('Tipo', max_length=20, choices=QUESTION_TYPES)
    options = models.JSONField('Opciones', help_text='Para opción múltiple, lista de opciones')
    correct_answer = models.CharField('Respuesta correcta', max_length=500)
    explanation = models.TextField('Explicación', blank=True)
    difficulty = models.IntegerField('Dificultad', default=1, choices=[(1, 'Fácil'), (2, 'Media'), (3, 'Difícil')])
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Banco de Preguntas'
    
    def __str__(self):
        return f"{self.course.title} - {self.question_text[:50]}"

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descripción')
    passing_score = models.IntegerField('Puntaje mínimo', default=70)
    questions_count = models.IntegerField('Número de preguntas', default=10)
    time_limit_minutes = models.IntegerField('Límite de tiempo (minutos)', default=30)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Examen'
        verbose_name_plural = 'Exámenes'
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def generate_random_questions(self):
        """Genera preguntas aleatorias del banco"""
        total_questions = QuestionBank.objects.filter(course=self.course).count()
        if total_questions >= self.questions_count:
            questions = list(QuestionBank.objects.filter(course=self.course))
            return random.sample(questions, self.questions_count)
        return list(QuestionBank.objects.filter(course=self.course))

class ExamAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exam_attempts')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    
    questions = models.JSONField('Preguntas', help_text='Lista de IDs de preguntas')
    user_answers = models.JSONField('Respuestas del usuario', default=dict)
    score = models.FloatField('Puntuación', null=True, blank=True)
    passed = models.BooleanField('Aprobado', default=False)
    
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Intento de Examen'
        verbose_name_plural = 'Intentos de Exámenes'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.exam.title} - {self.started_at.date()}"
    
    def calculate_score(self):
        """Calcula la puntuación del examen"""
        question_ids = self.questions
        total_questions = len(question_ids)
        correct_answers = 0
        
        questions = QuestionBank.objects.filter(id__in=question_ids)
        questions_map = {q.id: q for q in questions}
        
        for q_id in question_ids:
            question = questions_map.get(q_id)
            if question is None:
                continue
            
            user_answer = self.user_answers.get(str(q_id))
            
            if question.question_type == 'true_false':
                if str(user_answer).lower() == question.correct_answer.lower():
                    correct_answers += 1
            else:
                if user_answer == question.correct_answer:
                    correct_answers += 1
        
        self.score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        self.passed = self.score >= self.exam.passing_score
        self.save()
        
        self.user.update_progress()
        
        return self.score