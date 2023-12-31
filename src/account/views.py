from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .token import user_tokenizer_generate
from .forms import CreateUserForm, LoginForm, UpdateUserForm
from payment.models import ShippingAddress
from payment.forms import ShippingForm

# Create your views here.


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.active = False
            user.save()

            # email verification setup
            current_site = get_current_site(request)
            subject = "Account verification email"
            message = render_to_string(
                "account/email_verification.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": user_tokenizer_generate.make_token(user),
                },
            )

            user.email_user(subject=subject, message=message)

            return redirect("email_verification_sent")

    context = {
        "form": form,
    }
    return render(request, "account/register.html", context)


def email_verification(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    # success
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("email_verification_success")
    else:
        return redirect("email_verification_failed")


def email_verification_sent(request):
    return render(request, "account/email_verification_sent.html")


def email_verification_success(request):
    return render(request, "account/email_verification_success.html")


def email_verification_failed(request):
    return render(request, "account/email_verification_failed.html")


def user_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username, password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")

    context = {"form": form}

    return render(request, "account/login.html", context)


@login_required(login_url="login")
def user_logout(request):
    # when a user is logged out his session is deleted so is his cart data
    # by doing the following we are saving shopping cart data
    # even the user is logged out
    try:
        for key in list(request.session.keys()):
            if key == "session_key":
                continue

            else:
                del request.session[key]

    except KeyError:
        pass

    return redirect("store")


@login_required(login_url="login")
def dashboard(request):
    return render(request, "account/dashboard.html")


@login_required(login_url="login")
def profile_management(request):
    form = UpdateUserForm(instance=request.user)
    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    context = {
        "form": form,
    }

    return render(request, "account/profile_management.html", context)


@login_required(login_url="login")
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        user.delete()
        return redirect("store")
    return render(request, "account/delete_account.html")


# - Shipping View


@login_required(login_url="login")
def manage_shipping(request):
    try:
        # user account with shipping information
        shipping = ShippingAddress.objects.get(user=request.user)

    except ShippingAddress.DoesNotExist:
        # user account with no shipping information
        shipping = None

    form = ShippingForm(instance=shipping)

    if request.method == "POST":
        form = ShippingForm(request.POST, instance=shipping)
        if form.is_valid():
            shipping_form = form.save(commit=False)
            shipping_form.user = request.user
            shipping_form.save()
            return redirect("dashboard")

    context = {
        "form": form,
    }
    return render(request, "account/manage_shipping.html", context)
