from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Lesson, Enrollment
from apps.exams.models import Exam, ExamAttempt

def index(request):
    return render(request, 'index.html')

def course_list(request):
    courses = Course.objects.all()
    user_completed = {}
    
    if request.user.is_authenticated:
        # Obtener cursos completados por el usuario
        completed_exams = ExamAttempt.objects.filter(
            user=request.user, 
            passed=True
        ).select_related('exam__course')
        
        for attempt in completed_exams:
            if attempt.exam.course:
                user_completed[attempt.exam.course.id] = True
    
    context = {
        'courses': courses,
        'user_completed': user_completed,
    }
    return render(request, 'courses/course_list.html', context)

@login_required
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    lessons = course.lessons.all()
    
    completed = False
    exam_attempt = None
    enrollment = None
    
    if request.user.is_authenticated:
        exam = Exam.objects.filter(course=course).first()
        if exam:
            exam_attempt = ExamAttempt.objects.filter(
                user=request.user, 
                exam=exam,
                passed=True
            ).first()
            completed = exam_attempt is not None
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    
    context = {
        'course': course,
        'lessons': lessons,
        'completed': completed,
        'exam_attempt': exam_attempt,
        'enrollment': enrollment,
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    if created:
        messages.success(request, f'Solicitud enviada para "{course.title}". Espera la aprobación del administrador.')
    else:
        messages.info(request, 'Ya enviaste solicitud para este curso.')
    return redirect('courses:course_detail', slug=slug)

@login_required
def lesson_detail(request, course_slug, lesson_id):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    # Obtener lecciones anterior y siguiente
    lessons = list(course.lessons.all())
    current_index = next((i for i, l in enumerate(lessons) if l.id == lesson.id), -1)
    
    prev_lesson = lessons[current_index - 1] if current_index > 0 else None
    next_lesson = lessons[current_index + 1] if current_index < len(lessons) - 1 else None
    
    # Para lecciones de demo, redirigir a la demo correspondiente
    if lesson.lesson_type == 'demo':
        if lesson.demo_app == 'regression':
            return redirect('regression_demo:index')
        elif lesson.demo_app == 'genetic':
            return redirect('genetic_demo:index')
    
    # Para lecciones de examen
    if lesson.lesson_type == 'exam':
        exam = Exam.objects.filter(course=course).first()
        if exam:
            return redirect('exams:start_exam', exam_id=exam.id)
    
    context = {
        'course': course,
        'lesson': lesson,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
    }
    return render(request, 'courses/lesson_detail.html', context)