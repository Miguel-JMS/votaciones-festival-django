from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegistroForm
from .models import Categoria, Edicion, Votacion


def inicio(request):
    ediciones = Edicion.objects.filter(activa=True)
    return render(request, "votaciones/inicio.html", {"ediciones": ediciones})


def edicion_detalle(request, pk):
    edicion = get_object_or_404(Edicion, pk=pk, activa=True)
    categorias = edicion.categorias.filter(activa=True)
    return render(request, "votaciones/edicion.html", {"edicion": edicion, "categorias": categorias})


def categoria_detalle(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk, activa=True, edicion__activa=True)
    votaciones = categoria.votaciones.filter(activa=True)
    return render(request, "votaciones/categoria.html", {"categoria": categoria, "votaciones": votaciones})


def votacion_detalle(request, pk):
    votacion = get_object_or_404(Votacion, pk=pk, activa=True, categoria__activa=True)
    opciones = votacion.opciones.filter(activa=True)
    return render(request, "votaciones/votacion.html", {"votacion": votacion, "opciones": opciones})


def registro(request):
    if request.user.is_authenticated:
        return redirect("inicio")
    form = RegistroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        usuario = form.save()
        login(request, usuario)
        messages.success(request, "Cuenta creada. ¡Bienvenido!")
        return redirect("inicio")
    return render(request, "registration/registro.html", {"form": form})
