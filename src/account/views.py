from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth.models import User
from .token import user_tokenizer_generate
from .forms import CreateUserForm

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
