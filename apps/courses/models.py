from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField('Estado', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        unique_together = ['user', 'course']

    def __str__(self):
        return f'{self.user.username} -> {self.course.title} ({self.get_status_display()})'

class Course(models.Model):
    title = models.CharField('Título', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField('Descripción')
    objectives = models.TextField('Objetivos')
    prerequisites = models.TextField('Prerrequisitos', blank=True)
    image = models.ImageField(upload_to='courses/', null=True, blank=True)
    order = models.IntegerField('Orden', default=0)
    duration_months = models.IntegerField('Duración (meses)', default=6)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['order']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'slug': self.slug})
    
    @property
    def total_lessons(self):
        return self.lessons.count()
    
    @property
    def theory_lessons(self):
        return self.lessons.filter(lesson_type='theory')
    
    @property
    def example_lessons(self):
        return self.lessons.filter(lesson_type='example')

class Lesson(models.Model):
    LESSON_TYPES = [
        ('theory', 'Teoría'),
        ('example', 'Ejemplo Resuelto'),
        ('demo', 'Demo Interactiva'),
        ('exam', 'Examen'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField('Título', max_length=200)
    lesson_type = models.CharField('Tipo', max_length=20, choices=LESSON_TYPES)
    order = models.IntegerField('Orden')
    content = models.TextField('Contenido')
    
    # Para demos específicas
    demo_app = models.CharField('App de demo', max_length=50, blank=True, 
                                choices=[('regression', 'Regresión Lineal'), 
                                        ('genetic', 'Algoritmo Genético'),
                                        ('neural', 'Redes Neuronales'),
                                        ('tree', 'Árboles de Decisión'),
                                        ('svm', 'SVM'),
                                        ('clustering', 'Clustering'),
                                        ('nlp', 'NLP')])
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lección'
        verbose_name_plural = 'Lecciones'
        ordering = ['order']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def get_absolute_url(self):
        return reverse('courses:lesson_detail', kwargs={
            'course_slug': self.course.slug,
            'lesson_id': self.id
        })