from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random
import string

class PasswordResetCode(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='reset_codes')
    code = models.CharField('Código', max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Código de recuperación'
        verbose_name_plural = 'Códigos de recuperación'

    def __str__(self):
        return f'{self.user.username} - {self.code}'

    @staticmethod
    def generate_code():
        return ''.join(random.choices(string.digits, k=6))

class User(AbstractUser):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
        ('N', 'Prefiero no decirlo'),
    ]
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
        ('PA', 'Pasaporte'),
        ('NI', 'NIT'),
    ]

    edad = models.IntegerField('Edad', null=True, blank=True)
    telefono = models.CharField('Teléfono', max_length=20, blank=True)
    genero = models.CharField('Género', max_length=1, choices=GENERO_CHOICES, blank=True)
    tipo_documento = models.CharField('Tipo de documento', max_length=2, choices=TIPO_DOCUMENTO_CHOICES, blank=True)
    numero_documento = models.CharField('Número de documento', max_length=30, blank=True)

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    courses_completed = models.IntegerField(default=0)
    total_score = models.FloatField(default=0.0)

    date_joined = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return self.username
    
    def update_progress(self):
        """Actualiza el progreso general del usuario"""
        from apps.exams.models import ExamAttempt
        
        # Calcular cursos completados (aprobados)
        completed = ExamAttempt.objects.filter(
            user=self, 
            passed=True,
            exam__course__isnull=False
        ).values('exam__course').distinct().count()
        
        self.courses_completed = completed
        self.save()