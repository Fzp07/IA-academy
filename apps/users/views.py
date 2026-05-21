import sys, traceback
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from .forms import CustomUserCreationForm, UserProfileForm
from .models import PasswordResetCode
from .sms import send_sms
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model, update_session_auth_hash

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            messages.success(request, 'Registro exitoso. Ya puedes iniciar sesión.')
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        if not form.get_user().is_active:
            messages.error(self.request, 'Tu cuenta aún no ha sido aprobada por un administrador.')
            return self.form_invalid(form)
        messages.success(self.request, f'¡Bienvenido de vuelta, {form.get_user().username}!')
        return super().form_valid(form)

def password_reset_request(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            try:
                user = User.objects.get(email=email, is_active=True)
            except User.DoesNotExist:
                messages.error(request, 'No existe un usuario activo con ese correo.')
                return render(request, 'users/password_reset_request.html')

            code = PasswordResetCode.generate_code()
            PasswordResetCode.objects.create(user=user, code=code)

            subject = 'Código de recuperación - AI Academy'
            html = render_to_string('emails/reset_code.html', {
                'user': user,
                'code': code,
            })
            try:
                send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html)
            except Exception as e:
                print(f'EMAIL ERROR: {e}', file=sys.stderr)
                traceback.print_exc(file=sys.stderr)

            if user.telefono:
                try:
                    send_sms(user.telefono, f'AI Academy: Tu código de recuperación es: {code}')
                except Exception as e:
                    print(f'SMS ERROR: {e}', file=sys.stderr)

            request.session['reset_user_id'] = user.id
            messages.success(request, 'Código enviado a tu correo y teléfono.')
            return redirect('users:password_reset_verify')
        except Exception as e:
            traceback.print_exc(file=sys.stderr)
            messages.error(request, f'Error al procesar la solicitud.')
            return render(request, 'users/password_reset_request.html')

    return render(request, 'users/password_reset_request.html')

def password_reset_verify(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('users:password_reset_request')

    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        reset_code = PasswordResetCode.objects.filter(
            user_id=user_id, code=code, is_used=False,
            created_at__gte=timezone.now() - timezone.timedelta(minutes=15)
        ).first()

        if not reset_code:
            messages.error(request, 'Código inválido o expirado.')
            return render(request, 'users/password_reset_verify.html')

        reset_code.is_used = True
        reset_code.save()
        request.session['reset_verified'] = True
        return redirect('users:password_reset_confirm')

    return render(request, 'users/password_reset_verify.html')

def password_reset_confirm(request):
    user_id = request.session.get('reset_user_id')
    if not user_id or not request.session.get('reset_verified'):
        return redirect('users:password_reset_request')

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'users/password_reset_confirm.html')

        if len(password1) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
            return render(request, 'users/password_reset_confirm.html')

        user = get_object_or_404(User, id=user_id)
        user.set_password(password1)
        user.save()

        del request.session['reset_user_id']
        del request.session['reset_verified']

        messages.success(request, 'Contraseña restablecida exitosamente. Inicia sesión.')
        return redirect('users:login')

    return render(request, 'users/password_reset_confirm.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('users:login')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)

    from apps.exams.models import ExamAttempt
    exam_attempts = ExamAttempt.objects.filter(user=request.user).order_by('-completed_at')

    context = {
        'form': form,
        'exam_attempts': exam_attempts,
    }
    return render(request, 'users/profile.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_panel(request):
    from apps.courses.models import Enrollment

    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment_id')
        action = request.POST.get('action')
        enrollment = get_object_or_404(Enrollment, id=enrollment_id)

        if action == 'approve':
            enrollment.status = 'approved'
            enrollment.save()
            subject = f'Inscripción aprobada - {enrollment.course.title}'
            html = render_to_string('emails/enrollment_approved.html', {
                'user': enrollment.user,
                'course': enrollment.course,
                'login_url': request.build_absolute_uri('/users/login/'),
            })
            send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [enrollment.user.email], html_message=html)
            messages.success(request, f'Inscripción de {enrollment.user.username} aprobada para {enrollment.course.title}.')
        elif action == 'reject':
            username = enrollment.user.username
            course_title = enrollment.course.title
            email = enrollment.user.email
            subject = f'Inscripción rechazada - {course_title}'
            html = render_to_string('emails/enrollment_rejected.html', {
                'user': enrollment.user,
                'course': enrollment.course,
            })
            send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [email], html_message=html)
            enrollment.delete()
            messages.success(request, f'Inscripción de {username} rechazada para {course_title}.')

        return redirect('users:admin_panel')

    pending_enrollments = Enrollment.objects.filter(status='pending').select_related('user', 'course')
    approved_enrollments = Enrollment.objects.filter(status='approved').select_related('user', 'course')

    context = {
        'pending_enrollments': pending_enrollments,
        'approved_enrollments': approved_enrollments,
        'pending_count': pending_enrollments.count(),
        'approved_count': approved_enrollments.count(),
    }
    return render(request, 'users/admin_panel.html', context)
