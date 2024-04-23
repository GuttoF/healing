# Create your views here.
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import DoctorData, OpenDate, Speciality, is_doctor


def doctor_signup(request):
    if is_doctor(request.user):
        messages.add_message(
            request, messages.ERROR, "Usuário já cadastrado como médico."
        )
        return redirect("/medicos/schedule")

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

        return redirect("/medicos/schedule")


@login_required
def schedule(request):
    if not is_doctor(request.user):
        messages.add_message(
            request, messages.ERROR, "Usuário não cadastrado como médico."
        )
        return redirect("/users/logout")

    if request.method == "GET":
        doctor_data = DoctorData.objects.get(user=request.user)
        open_date = OpenDate.objects.filter(user=request.user)
        return render(
            request,
            "schedule.html",
            {"doctor_data": doctor_data, "open_date": open_date},
        )
    elif request.method == "POST":
        date = request.POST.get("date")
        formatted_data = datetime.strptime(date, "%Y-%m-%dT%H:%M")

        if formatted_data <= datetime.now():
            messages.add_message(
                request, messages.ERROR, "A data deve ser maior ou igual a data atual."
            )
            return redirect("/medicos/schedule")

        open_date = OpenDate(user=request.user, date=date)
        open_date.save()

        messages.add_message(request, messages.SUCCESS, "Data aberta com sucesso.")

        return redirect("/medicos/schedule")
