# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, CustomAuthenticationForm, PasswordResetForm, SetNewPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from vendeur.models import Boutique
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404
from vendeur.models import Boutique

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('authentification:home')
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def admin(request):
    return render(request, 'Admin.html')


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                if user.is_superuser:
                    return redirect('authentification:admin')
                return redirect('authentification:home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('authentification:login')


def home(request):
    if request.user.is_authenticated:
        boutique = Boutique.objects.filter(vendeur=request.user, active=False).first()
        if boutique:
            messages.info(request, "Votre demande de création de boutique est en attente de validation par l'administrateur. Vous serez contacté prochainement.")
    return render(request, 'home.html')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    email_template_name = "password_reset_email.html"
                    context = {
                        "email": user.email,
                        "domain": request.META['HTTP_HOST'],
                        "site_name": "EasyMarket",
                        "uid": uid,
                        "user": user,
                        "token": token,
                        "protocol": 'https' if request.is_secure() else 'http',
                    }
                    email_message = render_to_string(email_template_name, context)
                    try:
                        send_mail(subject, email_message, 'konatefahran3@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

                    messages.success(request, "Password reset instructions have been sent to your email.")
                    return redirect('authentification:password_reset_done')
            else:
                messages.error(request, "Email not found in our system.")
    else:
        password_reset_form = PasswordResetForm()
    return render(request, "password_reset_form.html", {"form": password_reset_form})


def password_reset_done(request):
    return render(request, 'password_reset_done.html')


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetNewPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and log in now.")
                return redirect('authentification:login')
        else:
            form = SetNewPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect('authentification:password_reset')


@login_required
def password_change(request):
    if request.method == 'POST':
        form = SetNewPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed successfully!")
            return redirect('authentification:home')
    else:
        form = SetNewPasswordForm(request.user)
    return render(request, 'password_change.html', {'form': form})

def liste_boutiques(request):
    # On affiche d'abord les boutiques non actives, puis les actives
    boutiques_inactives = Boutique.objects.filter(active=False)
    boutiques_actives = Boutique.objects.filter(active=True)
    return render(request, 'ListeBoutique.html', {
        'boutiques_inactives': boutiques_inactives,
        'boutiques_actives': boutiques_actives,
    })

@require_POST
def activate_boutique(request):
    boutique_id = request.POST.get('boutique_id')
    boutique = get_object_or_404(Boutique, id=boutique_id)
    boutique.active = True
    boutique.save()
    messages.success(request, f"La boutique {boutique.nom} a été activée.")
    return redirect('authentification:liste_boutiques')

@require_POST
def deactivate_boutique(request):
    boutique_id = request.POST.get('boutique_id')
    boutique = get_object_or_404(Boutique, id=boutique_id)
    boutique.active = False
    boutique.save()
    messages.success(request, f"La boutique {boutique.nom} a été désactivée.")
    return redirect('authentification:liste_boutiques')