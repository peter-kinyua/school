
# ...existing code...

# Place all imports at the top
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from .models import PastPaper, ZoomLink, Student
import json


@login_required
def edit_paper(request, paper_id):
	paper = get_object_or_404(PastPaper, id=paper_id, teacher=request.user)
	if request.method == 'POST':
		paper.title = request.POST.get('title', paper.title)
		paper.target_class = request.POST.get('target_class', paper.target_class)
		if 'file' in request.FILES:
			paper.file = request.FILES['file']
		paper.save()
		return redirect('teacher_dashboard')
	return render(request, 'teachers/edit_paper.html', {'paper': paper})


@login_required
def delete_paper(request, paper_id):
	paper = get_object_or_404(PastPaper, id=paper_id, teacher=request.user)
	if request.method == 'POST':
		paper.delete()
		return redirect('teacher_dashboard')
	return render(request, 'teachers/confirm_delete.html', {'object': paper, 'type': 'Paper'})


@login_required
def edit_zoom_link(request, link_id):
	link = get_object_or_404(ZoomLink, id=link_id, teacher=request.user)
	if request.method == 'POST':
		link.class_name = request.POST.get('class_name', link.class_name)
		link.target_class = request.POST.get('target_class', link.target_class)
		link.zoom_link = request.POST.get('zoom_link', link.zoom_link)
		link.save()
		return redirect('teacher_dashboard')
	return render(request, 'teachers/edit_zoom_link.html', {'link': link})


@login_required
def delete_zoom_link(request, link_id):
	link = get_object_or_404(ZoomLink, id=link_id, teacher=request.user)
	if request.method == 'POST':
		link.delete()
		return redirect('teacher_dashboard')
	return render(request, 'teachers/confirm_delete.html', {'object': link, 'type': 'Zoom Link'})

# Student login page
def student_login_page(request):
	return render(request, 'teachers/student_login.html')

# Student dashboard page
def student_dashboard(request):
	return render(request, 'teachers/student_dashboard.html')

# Teacher login page (GET)
def teacher_login_page(request):
	return render(request, 'teachers/login.html')

# Upload paper view for API endpoint
@csrf_exempt
@login_required
def upload_paper(request):
    if request.method == 'POST':
        title = request.POST.get('paperTitle')
        file = request.FILES.get('paper-file')
        target_class = request.POST.get('paperClass')
        teacher = request.user
        if not file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        paper = PastPaper.objects.create(title=title, file=file, teacher=teacher, target_class=target_class)
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.files.storage import default_storage
from .models import PastPaper, ZoomLink, Student
import json

# Teacher web forms for dashboard
@login_required
def teacher_add_student(request):
	return render(request, 'teachers/add_student.html')

@login_required
def teacher_upload_paper(request):
	return render(request, 'teachers/upload_paper.html')

@login_required
def teacher_add_zoom_link(request):
	return render(request, 'teachers/add_zoom_link.html')

def list_teachers(request):
	teachers = User.objects.all()
	result = [
		{
			'username': t.username,
			'email': t.email,
			'first_name': t.first_name,
			'last_name': t.last_name
		} for t in teachers
	]
	return JsonResponse(result, safe=False)

# Teacher dashboard view
@login_required
def teacher_dashboard(request):
	papers = PastPaper.objects.filter(teacher=request.user).order_by('-uploaded_at')
	links = ZoomLink.objects.filter(teacher=request.user).order_by('-added_at')
	return render(request, 'teachers/dashboard.html', {
		'papers': papers,
		'links': links
	})

@csrf_exempt
@login_required
def add_student(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		admission_number = data.get('admission_number')
		name = data.get('name')
		current_class = data.get('current_class')
		password = data.get('password')
		if not (admission_number and name and current_class and password):
			return JsonResponse({'error': 'All fields required'}, status=400)
		if Student.objects.filter(admission_number=admission_number).exists():
			return JsonResponse({'error': 'Admission number already exists'}, status=400)
		Student.objects.create(admission_number=admission_number, name=name, current_class=current_class, password=password)
		return JsonResponse({'success': True})
	return JsonResponse({'error': 'Invalid request'}, status=400)
@csrf_exempt
def student_login(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		admission_number = data.get('admission_number')
		password = data.get('password')
		try:
			student = Student.objects.get(admission_number=admission_number)
			if student.password == password:
				return JsonResponse({
					'name': student.name,
					'current_class': student.current_class
				})
			else:
				return JsonResponse({'error': 'Incorrect password'}, status=401)
		except Student.DoesNotExist:
			return JsonResponse({'error': 'Student not found'}, status=404)
	return JsonResponse({'error': 'Invalid request'}, status=400)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.files.storage import default_storage
from .models import PastPaper, ZoomLink, Student
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from .models import PastPaper, ZoomLink
import json

@csrf_exempt
def teacher_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def add_zoom_link(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		class_name = data.get('className')
		target_class = data.get('zoomClass')
		zoom_link = data.get('zoomLink')
		teacher = request.user
		ZoomLink.objects.create(class_name=class_name, zoom_link=zoom_link, teacher=teacher, target_class=target_class)
		return JsonResponse({'success': True})
	return JsonResponse({'error': 'Invalid request'}, status=400)

def list_papers(request):
	student_class = request.GET.get('class')
	teacher_username = request.GET.get('teacher')
	papers = PastPaper.objects.all().order_by('-uploaded_at')
	if student_class:
		papers = papers.filter(target_class__icontains=student_class)
	if teacher_username:
		papers = papers.filter(teacher__username=teacher_username)
	result = [
		{
			'title': p.title,
			'filename': p.file.url,
			'download_url': p.file.url  # For direct download
		} for p in papers
	]
	return JsonResponse(result, safe=False)

def list_zoom_links(request):
	student_class = request.GET.get('class')
	links = ZoomLink.objects.all().order_by('-added_at')
	if student_class:
		links = links.filter(class_name__icontains=student_class)
	result = [
		{
			'className': l.class_name,
			'zoomLink': l.zoom_link
		} for l in links
	]
	return JsonResponse(result, safe=False)
