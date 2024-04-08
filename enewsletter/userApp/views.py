from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm,SignUpForm,UploadForm
from .models import UserProfile,Subscription,NewsLetter,Department,Bookmark
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login , logout
from django.shortcuts import redirect
import logging
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import requests
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from io import BytesIO
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.conf import settings
from email.mime.multipart import MIMEMultipart
import smtplib


api_key = settings.GEMINI_API_KEY
logger = logging.getLogger(__name__)

def index(request):
    return redirect('login_page')

def login_page(request):
    context = {}
    forms = LoginForm(request.POST or None)
    context['form'] = forms
    return render(request,"login.html",context)

def save_data(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            regNo = form.cleaned_data['regNo']
            if UserProfile.objects.filter(username=username).exists():
                return HttpResponse("A user with this username already exists.", status=400)
            if UserProfile.objects.filter(regNo=regNo).exists():
                return HttpResponse("A user with this registration number already exists.", status=400)
            department_id = form.cleaned_data['department']
            try:
                department = Department.objects.get(id=department_id)
            except Department.DoesNotExist:
                return HttpResponse("Selected department does not exist.", status=400)
            user = UserProfile(
                username=username,
                regNo=regNo,
                department=department,
                is_staff=form.cleaned_data.get('isAdmin', False)
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            Subscription.objects.create(user=user, department=department)
            return redirect('login_page')
        else:
            return render(request, "signup.html", {'form': form})
    else:
        return redirect('signup')

logger = logging.getLogger(__name__)


def check_data(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                logger.info(f"Authentication successful for username: {username}")
                login(request, user)
                if user.is_staff:
                    return redirect('adminPage')  
                else:
                    next_url = request.POST.get('next') or 'userPage'
                    return redirect(next_url)
            else:
                logger.error(f"Authentication failed for username: {username}")
                return HttpResponse("Please enter a correct username and password. Note that both fields may be case-sensitive.", status=401)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    logger.error(f"Error in field {field}: {error}")
            return render(request, "login.html", {'form': form})
    else:
        form = LoginForm()
        return render(request, "login.html", {'form': form})


def signup(request):
    context = {}
    forms = SignUpForm(request.POST or None)
    context['form'] = forms
    return render(request,"signup.html",context)


@login_required
def userPage(request):
    user = request.user  
    if hasattr(user, 'department'):
        department = user.department
    else:
        return HttpResponse("This user does not have a department set.", status=400)
    newsletters = NewsLetter.objects.filter(department=department)
    context = {
        'user_name': user.username,  
        'department': department.name,  
        'newsletters': newsletters,
    }
    return render(request, "userPage.html", context)

@login_required
def adminPage(request):
    user_name = request.session.get('user_name')
    context = {'user_name': user_name}
    forms = UploadForm(request.POST or None)
    context['form'] = forms
    return render(request, "adminPage.html", context)


@login_required
def circulateNews(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            message = form.cleaned_data['message']
            image = form.cleaned_data['image']
            department = request.user.department
            
            newsletter = NewsLetter(
                department=department, 
                title=title, 
                message=message, 
                image=image if image else None, 
                date=timezone.now()
            )
            newsletter.save()

            users_to_email = UserProfile.objects.filter(department=department, is_staff=False)
            
            recipient_emails = [(user.username, user.username) for user in users_to_email]

            email_subject = f"New Newsletter: {title}"
            email_body = f"Title: {title}\nMessage: {message}"
            email_messages = [(email_subject, email_body, settings.EMAIL_HOST_USER, [email]) for _, email in recipient_emails]

            try:
                send_mass_mail(tuple(email_messages), fail_silently=False)
                return redirect('adminPage')
            except Exception as e:
                return HttpResponse(f"Failed to send email: {str(e)}")
        else:
            return HttpResponse("Invalid Values")
    else:
        return redirect('adminPage')


@login_required
def messagePage(request):
    message_id = request.GET.get('id')
    if not message_id:
        return redirect('userPage')  
    newsletter = get_object_or_404(NewsLetter, id=message_id)
    context = {'newsletter': newsletter}
    return render(request, "messagePage.html", context)

@login_required
def bookmark_newsletter(request):
    if request.method == "POST":
        user_profile = request.user
        newsletter_id = request.POST.get('newsletter_id')
        newsletter = get_object_or_404(NewsLetter, id=newsletter_id)
        bookmark, created = Bookmark.objects.get_or_create(user=user_profile, newsletter=newsletter)
        if not created:
            bookmark.delete()
            messages.info(request, "Newsletter unbookmarked successfully.")
        else:
            messages.info(request, "Newsletter bookmarked successfully.")
        return redirect(request.META.get('HTTP_REFERER', 'userPage'))
    else:
        return redirect('userPage')

@login_required
def bookmarked_messages(request):
    user_profile = request.user
    bookmarks = Bookmark.objects.filter(user=user_profile).select_related('newsletter')
    bookmarked_newsletters = [bookmark.newsletter for bookmark in bookmarks]

    context = {
        'user_name': user_profile.username,
        'department': user_profile.department.name,
        'newsletters': bookmarked_newsletters,
    }
    return render(request, "bookmarked_messages.html", context)

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_inbox(request):
    newsletters = NewsLetter.objects.all()
    return render(request, 'admin_inbox.html', {'newsletters': newsletters})

@login_required
@user_passes_test(is_admin)
def delete_newsletter(request):
    if 'newsletter_id' in request.GET:
        newsletter_id = request.GET['newsletter_id']
        newsletter = get_object_or_404(NewsLetter, pk=newsletter_id)
        
        if request.user.department == newsletter.department or request.user.is_superuser:
            newsletter.delete()
            return redirect(reverse('admin_inbox'))
        else:
            return HttpResponse("Unauthorized", status=401)
    
    return redirect(reverse('admin_inbox'))

@login_required
@user_passes_test(is_admin)
def edit_message_page(request):
    if 'newsletter_id' in request.GET:
        newsletter_id = request.GET['newsletter_id']
        newsletter = get_object_or_404(NewsLetter, pk=newsletter_id, department=request.user.department)
        
        if request.method == 'POST':
            title = request.POST.get('title')
            message = request.POST.get('message')
            image = request.FILES.get('image')
            newsletter.title = title
            newsletter.message = message
            if image:
                newsletter.image = image
            newsletter.save()
            return redirect('admin_inbox')
        
        return render(request, 'editMessagePage.html', {'newsletter': newsletter})
    
    return redirect('admin_inbox')

@login_required
def update_newsletter(request, newsletter_id):
    newsletter = get_object_or_404(NewsLetter, id=newsletter_id, department=request.user.department)
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES, instance=newsletter)
        if form.is_valid():
            form.save()
            messages.success(request, "Newsletter updated successfully.")
            logger.debug("Newsletter update successful for newsletter ID: %s", newsletter_id)
            return redirect('admin_inbox')
        else:
            logger.error("Form is invalid. Errors: %s", form.errors.as_text())
            messages.error(request, "Error updating the newsletter.")
    else:
        logger.debug("Loading newsletter for update. Newsletter ID: %s", newsletter_id)
        form = UploadForm(instance=newsletter)

    return render(request, 'editMessagePage.html', {'form': form, 'newsletter': newsletter})

def call_gemini_api(title_text):
    api_key = settings.GEMINI_API_KEY
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{
                "text": title_text
            }]
        }]
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        candidates = response.json().get('candidates', [])
        if candidates:
            parts = candidates[0].get('content', {}).get('parts', [])
            if parts:
                generated_message = parts[0].get('text', "No message returned")
                return generated_message
        return "Generated message is not available."
    else:
        logger.error(f"Failed to generate message. Status code: {response.status_code}, Response: {response.text}")
        return "Could not generate message due to an error."

@login_required
def generate_message_api(request):
    if request.method == "POST":
        title = request.POST.get('title', '')
        message = request.POST.get('message', '').strip()
        prompt_text = message if message else title  
        generated_message = call_gemini_api(prompt_text)
        return JsonResponse({'message': generated_message})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def logout_page(request):
    request.session.clear
    logout(request)
    return redirect('login_page')