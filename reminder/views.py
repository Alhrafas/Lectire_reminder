from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Lecture
from .forms import LectureForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.dateparse import parse_date
import datetime



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

    # Apply category filter
    if category_filter:
        lectures = lectures.filter(category=category_filter)

    # Apply search filter
    if search_query:
        lectures = lectures.filter(title__icontains=search_query)

    # Apply sorting
    if sort_by == "date_asc":
        lectures = lectures.order_by("date", "time")
    elif sort_by == "date_desc":
        lectures = lectures.order_by("-date", "-time")
    elif sort_by == "title_asc":
        lectures = lectures.order_by("title")
    elif sort_by == "title_desc":
        lectures = lectures.order_by("-title")

    return render(request, 'reminder/dashboard.html', {
        "lectures": lectures,
        "category_filter": category_filter,
        "search_query": search_query,
        "sort_by": sort_by,
    })

@login_required
def calendar_view(request):
    return render(request, "reminder/calendar.html")

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
