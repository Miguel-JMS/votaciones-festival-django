from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Categoria, Edicion, Opcion, Votacion


def crear_base():
    ed = Edicion.objects.create(nombre="60.º Festival", anio=2027, fecha_inicio=date(2027, 4, 28), fecha_fin=date(2027, 5, 2))
    cat = Categoria.objects.create(edicion=ed, nombre="Concursos")
    ahora = timezone.now()
    vot = Votacion.objects.create(categoria=cat, titulo="Canción favorita",
                                  fecha_apertura=ahora - timedelta(days=1), fecha_cierre=ahora + timedelta(days=1))
    op = Opcion.objects.create(votacion=vot, nombre="Sin tu mirada")
    return ed, cat, vot, op


class ModelosTests(TestCase):
    def test_jerarquia_y_relaciones(self):
        ed, cat, vot, op = crear_base()
        self.assertEqual(op.votacion.categoria.edicion, ed)
        self.assertIn(vot, cat.votaciones.all())

    def test_estado_votacion(self):
        _, _, vot, _ = crear_base()
        self.assertEqual(vot.estado, "Abierta")
        vot.fecha_cierre = timezone.now() - timedelta(hours=1)
        self.assertEqual(vot.estado, "Cerrada")

    def test_fechas_incoherentes(self):
        _, cat, _, _ = crear_base()
        ahora = timezone.now()
        v = Votacion(categoria=cat, titulo="X", fecha_apertura=ahora, fecha_cierre=ahora - timedelta(days=1))
        with self.assertRaises(ValidationError):
            v.full_clean()


class VistasTests(TestCase):
    def setUp(self):
        self.ed, self.cat, self.vot, self.op = crear_base()

    def test_paginas_publicas_muestran_datos_de_la_bd(self):
        for url, texto in [(reverse("inicio"), "60.º Festival"),
                           (reverse("edicion", args=[self.ed.pk]), "Concursos"),
                           (reverse("categoria", args=[self.cat.pk]), "Canción favorita"),
                           (reverse("votacion", args=[self.vot.pk]), "Sin tu mirada")]:
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertContains(r, texto)

    def test_registro_inicio_y_cierre_de_sesion(self):
        r = self.client.post(reverse("registro"), {"username": "ana", "email": "ana@correo.com",
                                                   "password1": "ClaveSegura2027!", "password2": "ClaveSegura2027!"})
        self.assertRedirects(r, reverse("inicio"))
        self.assertTrue(User.objects.filter(username="ana").exists())
        self.client.post(reverse("logout"))
        r = self.client.post(reverse("login"), {"username": "ana", "password": "ClaveSegura2027!"})
        self.assertRedirects(r, reverse("inicio"))

    def test_correo_duplicado_rechazado(self):
        User.objects.create_user("luis", "ana@correo.com", "ClaveSegura2027!")
        r = self.client.post(reverse("registro"), {"username": "ana", "email": "ana@correo.com",
                                                   "password1": "ClaveSegura2027!", "password2": "ClaveSegura2027!"})
        self.assertContains(r, "ya está registrado")

    def test_admin_exige_sesion(self):
        r = self.client.get("/admin/")
        self.assertEqual(r.status_code, 302)

    def test_edicion_inactiva_no_se_muestra(self):
        self.ed.activa = False
        self.ed.save()
        self.assertEqual(self.client.get(reverse("edicion", args=[self.ed.pk])).status_code, 404)
