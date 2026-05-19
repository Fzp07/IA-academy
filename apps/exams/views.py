from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Exam, ExamAttempt

@login_required
def start_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.generate_random_questions()

    if request.method == 'POST':
        user_answers = {}
        for q in questions:
            answer = request.POST.get(f'question_{q.id}')
            if answer is not None:
                user_answers[str(q.id)] = answer

        attempt = ExamAttempt.objects.create(
            user=request.user,
            exam=exam,
            questions=[q.id for q in questions],
            user_answers=user_answers,
            completed_at=timezone.now()
        )
        attempt.calculate_score()

        messages.success(request, f'Examen completado. Tu puntuación: {attempt.score:.1f}%')
        return redirect('courses:course_detail', slug=exam.course.slug)

    context = {
        'exam': exam,
        'questions': questions,
    }
    return render(request, 'exams/exam.html', context)

@login_required
def submit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.generate_random_questions()

    if request.method == 'POST':
        user_answers = {}
        for q in questions:
            answer = request.POST.get(f'question_{q.id}')
            if answer is not None:
                user_answers[str(q.id)] = answer

        attempt = ExamAttempt.objects.create(
            user=request.user,
            exam=exam,
            questions=[q.id for q in questions],
            user_answers=user_answers,
            completed_at=timezone.now()
        )
        attempt.calculate_score()

        messages.success(request, f'Examen completado. Tu puntuación: {attempt.score:.1f}%')
        return redirect('courses:course_detail', slug=exam.course.slug)

    return redirect('exams:start_exam', exam_id=exam.id)
