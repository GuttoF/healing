# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import DoctorData, Speciality


@login_required
def doctor_signup(request):
    doctor_data_existance = DoctorData.objects.filter(user=request.user)
    if doctor_data_existance.exists():
        messages.add_message(
            request, messages.ERROR, "Usuário já cadastrado como médico."
        )
        return redirect("/medicos/abrir_horario")
    
    if request.method == "GET":
        specialities = Speciality.objects.all()
        return render(request, "doctor_signup.html", {"specialities": specialities})
    elif request.method == "POST":
        crm = request.POST.get("crm")
        name = request.POST.get("nome")
        cep = request.POST.get("cep")
        street = request.POST.get("rua")
        neighborhood = request.POST.get("bairro")
        number = request.POST.get("numero")
        cim = request.FILES.get("cim")
        rg = request.FILES.get("rg")
        picture = request.FILES.get("foto")
        speciality = request.POST.get("especialidade")
        description = request.POST.get("descricao")
        bill = request.POST.get("valor_consulta")

        # TODO: Validar todos os campos

        doctor_data = DoctorData(
            crm=crm,
            name=name,
            cep=cep,
            street=street,
            neighborhood=neighborhood,
            number=number,
            rg=rg,
            cim=cim,
            picture=picture,
            user=request.user,
            description=description,
            speciality_id=speciality,
            bill=bill,
        )
        doctor_data.save()

        messages.add_message(
            request, messages.SUCCESS, "Cadastro médico realizado com sucesso."
        )

        return redirect("/medicos/abrir_horario")
