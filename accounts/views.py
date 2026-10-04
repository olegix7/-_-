from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Profile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('resume_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f'welcome|{user.first_name or user.username}',
                extra_tags='welcome'
            )
            return redirect('resume_list')
        else:
            messages.error(request, 'Виправте помилки у формі.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('resume_list')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Ласкаво просимо, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'resume_list')
            return redirect(next_url)
        else:
            messages.error(request, 'Невірне ім\'я користувача або пароль.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Ви вийшли з системи.')
    return redirect('home')


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профіль успішно оновлено!')
            return redirect('profile')
        else:
            messages.error(request, 'Виправте помилки у формі.')
    else:
        form = ProfileForm(instance=profile)
    published_count = request.user.resumes.filter(status='published').count()
    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile,
        'published_count': published_count,
    })


@login_required
def admin_users_view(request):
    """Admin-only view to list all users."""
    try:
        is_admin = request.user.profile.is_admin
    except Exception:
        is_admin = request.user.is_staff
    if not is_admin:
        messages.error(request, 'Доступ заборонено.')
        return redirect('home')
    users = User.objects.select_related('profile').all().order_by('-date_joined')
    return render(request, 'accounts/admin_users.html', {'users': users})


@login_required
def admin_toggle_role(request, user_id):
    """Admin can toggle user role between user/admin."""
    try:
        is_admin = request.user.profile.is_admin
    except Exception:
        is_admin = request.user.is_staff
    if not is_admin:
        messages.error(request, 'Доступ заборонено.')
        return redirect('home')
    target_user = User.objects.get(pk=user_id)
    if target_user == request.user:
        messages.warning(request, 'Не можна змінити власну роль.')
        return redirect('admin_users')
    target_profile, _ = Profile.objects.get_or_create(user=target_user)
    if target_profile.role == Profile.ROLE_ADMIN:
        target_profile.role = Profile.ROLE_USER
        msg = f'Роль користувача {target_user.username} змінено на "Користувач".'
    else:
        target_profile.role = Profile.ROLE_ADMIN
        msg = f'Роль користувача {target_user.username} змінено на "Адміністратор".'
    target_profile.save()
    messages.success(request, msg)
    return redirect('admin_users')
