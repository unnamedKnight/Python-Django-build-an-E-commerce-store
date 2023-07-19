from django.shortcuts import render, redirect


from .forms import CreateUserForm

# Create your views here.


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            return redirect('')

    context = {
        "form": form,
    }
    return render(request, "account/register.html", context)
