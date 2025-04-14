from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.http import JsonResponse
from .models import Lecture
from .forms import LectureForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import timedelta, datetime
from celery import current_app
from django.utils.timezone import now
from django.conf import settings


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Auto-login after registration
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'reminder/register.html', {'form': form})


@login_required
def dashboard(request):
    category_filter = request.GET.get("category", "")
    search_query = request.GET.get("search", "")
    sort_by = request.GET.get("sort", "date_asc")  # Default: Oldest first

    lectures = Lecture.objects.filter(user=request.user)
    completed_lectures = lectures.filter(date__lt=now().date())
    upcoming_lectures = lectures.filter(date__gte=now().date())

    upcoming_soon_lectures = upcoming_lectures.filter(
        date=now().date(),
        time__gte=now().time(),
        time__lte=(now() + timedelta(hours=1)).time()
    )

    # Apply category filter
    if category_filter:
        upcoming_lectures = upcoming_lectures.filter(category=category_filter)
        completed_lectures = completed_lectures.filter(category=category_filter)

    # Apply search filter
    if search_query:
        upcoming_lectures = upcoming_lectures.filter(title__icontains=search_query)
        completed_lectures = completed_lectures.filter(title__icontains=search_query)

    # Apply sorting
    if sort_by == "date_asc":
        upcoming_lectures = upcoming_lectures.order_by("date", "time")
        completed_lectures = completed_lectures.order_by("-date", "-time")
    elif sort_by == "date_desc":
        upcoming_lectures = upcoming_lectures.order_by("-date", "-time")
        completed_lectures = completed_lectures.order_by("date", "time")
    elif sort_by == "title_asc":
        upcoming_lectures = upcoming_lectures.order_by("title")
        completed_lectures = completed_lectures.order_by("title")
    elif sort_by == "title_desc":
        upcoming_lectures = upcoming_lectures.order_by("-title")
        completed_lectures = completed_lectures.order_by("-title")

    # Progress tracking
    total_lectures = lectures.count()
    completed_count = completed_lectures.count()
    progress_percentage = (completed_count / total_lectures * 100) if total_lectures > 0 else 0

    next_lecture = upcoming_lectures.order_by("date", "time").first()

    return render(request, 'reminder/dashboard.html', {
        "next_lecture": next_lecture,
        "upcoming_soon_lectures": upcoming_soon_lectures,
        "upcoming_lectures": upcoming_lectures,
        "completed_lectures": completed_lectures,
        "category_filter": category_filter,
        "search_query": search_query,
        "sort_by": sort_by,
        "progress_percentage": round(progress_percentage, 2),
        "total_lectures": total_lectures,
    })



@login_required
def lecture_api(request):
    lectures = Lecture.objects.filter(user=request.user)
    events = []

    for lecture in lectures:
        events.append({
            "id": lecture.id,
            "title": lecture.title,
            "start": lecture.date.strftime("%Y-%m-%d"),  # Format date
            "time": lecture.time.strftime("%H:%M"),
            "url": f"/lectures/edit/{lecture.id}/"
        })

    return JsonResponse(events, safe=False)


@login_required
def add_lecture(request):
    if request.method == "POST":
        form = LectureForm(request.POST)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.user = request.user  # Assign user
            lecture.save()
            messages.success(request, "Lecture added successfully!")
            return redirect("dashboard")
    else:
        form = LectureForm()  # Ensure form is created when loading page

    return render(request, "reminder/lecture_form.html", {"form": form})


@login_required
def edit_lecture(request, pk):
    lecture = get_object_or_404(Lecture, id=pk, user=request.user)

    if request.method == "POST":
        form = LectureForm(request.POST, instance=lecture)
        if form.is_valid():
            form.save()
            messages.success(request, "Lecture updated successfully!")
            return redirect("dashboard")
    else:
        form = LectureForm(instance=lecture)  # Pre-fill form

    return render(request, "reminder/lecture_form.html", {"form": form, "lecture": lecture})


@login_required
def delete_lecture(request, pk):
    lecture = get_object_or_404(Lecture, id=pk, user=request.user)
    lecture.delete()
    messages.success(request, "Lecture deleted successfully!")
    return redirect("dashboard")
