from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Announcement
from .forms import AnnouncementForm
from accounts.models import Profile


def _require_admin(request):
    """Returns True if user is admin, False otherwise (also sets an error message)."""
    if not request.user.is_authenticated:
        return False
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return profile.is_admin


# ── Public list ───────────────────────────────────────────────────────────────

def announcement_list(request):
    ann_type = request.GET.get('type', '')
    qs = Announcement.objects.filter(is_published=True)
    if ann_type in ('news', 'announcement'):
        qs = qs.filter(announcement_type=ann_type)
    return render(request, 'announcements/announcement_list.html', {
        'announcements': qs,
        'current_type': ann_type,
    })


def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk, is_published=True)
    return render(request, 'announcements/announcement_detail.html', {
        'announcement': announcement,
    })


# ── Admin CRUD ────────────────────────────────────────────────────────────────

@login_required
def announcement_create(request):
    if not _require_admin(request):
        messages.error(request, 'Доступ заборонено. Тільки для адміністраторів.')
        return redirect('announcement_list')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            ann = form.save(commit=False)
            ann.author = request.user
            ann.save()
            messages.success(request, 'Оголошення створено.')
            return redirect('announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'announcements/announcement_form.html', {
        'form': form, 'action': 'create'
    })


@login_required
def announcement_edit(request, pk):
    if not _require_admin(request):
        messages.error(request, 'Доступ заборонено. Тільки для адміністраторів.')
        return redirect('announcement_list')

    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Оголошення оновлено.')
            return redirect('announcement_detail', pk=pk)
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'announcements/announcement_form.html', {
        'form': form, 'action': 'edit', 'announcement': announcement
    })


@login_required
def announcement_delete(request, pk):
    if not _require_admin(request):
        messages.error(request, 'Доступ заборонено. Тільки для адміністраторів.')
        return redirect('announcement_list')

    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        announcement.delete()
        messages.success(request, 'Оголошення видалено.')
        return redirect('announcement_list')
    return render(request, 'announcements/announcement_confirm_delete.html', {
        'announcement': announcement
    })
