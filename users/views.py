from django.contrib import auth, messages
from django.shortcuts import redirect, render


# Create your views here.
def signup(request):
    if request.method == "GET":
        return render(request, "signup.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get("confirmar_senha")

        if senha != confirmar_senha:
            messages.add_message(request, messages.ERROR, "As senhas não coincidem")
            return redirect("signup")

        if len(senha) < 8:
            messages.add_message(
                request, messages.ERROR, "A senha deve ter no mínimo 8 caracteres"
            )
            return redirect("signup")

        users = auth.models.User.objects.filter(username=username)
        print(users.exists())

        if users.exists():
            messages.add_message(request, messages.ERROR, "Usuário já cadastrado")
            return redirect("signup")

        user = auth.models.User.objects.create_user(
            username=username, email=email, password=senha
        )
        user.save()

        return redirect("login")


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        senha = request.POST.get("senha")
        user = auth.authenticate(request, username=username, password=senha)

        if user:
            auth.login(request, user)
            return redirect("/pacientes/home")
        messages.add_message(request, messages.ERROR, "Usuário ou senha incorretos")
        return redirect("/usuarios/login")
    

def logout_view(request):
    auth.logout(request)
    return redirect("login")
