from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from votaciones.models import Categoria, Edicion, Opcion, Votacion


class Command(BaseCommand):
    help = "Carga datos de prueba (ediciones, categorías, votaciones y opciones). Es seguro ejecutarlo varias veces."

    def handle(self, *args, **opts):
        ahora = timezone.now()
        e26, _ = Edicion.objects.get_or_create(anio=2026, defaults=dict(
            nombre="59.º Festival de la Leyenda Vallenata", fecha_inicio=date(2026, 4, 29), fecha_fin=date(2026, 5, 3)))
        e27, _ = Edicion.objects.get_or_create(anio=2027, defaults=dict(
            nombre="60.º Festival de la Leyenda Vallenata", fecha_inicio=date(2027, 4, 28), fecha_fin=date(2027, 5, 2)))

        datos = {
            (e27, "Concursos", "Votaciones sobre las finales del Festival"): [
                ("Canción inédita favorita del público", -1, 30, ["Sin tu mirada", "Camino al Cesar", "Voz de acordeón"]),
                ("Mejor piquería infantil", -1, 30, ["Versos del río", "Rima y tambor"]),
            ],
            (e27, "Desfiles y cultura", "Piloneras, vestuario y tradición"): [
                ("Pilonera más elegante", -1, 30, ["Pilonera A", "Pilonera B", "Pilonera C"]),
            ],
            (e27, "Artistas invitados", "Elige tu concierto favorito"): [
                ("Concierto más esperado", -30, -1, ["Artista 1", "Artista 2"]),
            ],
            (e26, "Concursos", "Votaciones de la edición anterior"): [
                ("Canción inédita 2026", -400, -380, ["Canción 1", "Canción 2"]),
            ],
        }
        for (edicion, nombre, desc), votaciones in datos.items():
            cat, _ = Categoria.objects.get_or_create(edicion=edicion, nombre=nombre, defaults={"descripcion": desc})
            for titulo, ini, fin, opciones in votaciones:
                v, _ = Votacion.objects.get_or_create(categoria=cat, titulo=titulo, defaults=dict(
                    fecha_apertura=ahora + timedelta(days=ini), fecha_cierre=ahora + timedelta(days=fin),
                    descripcion="Votación de ejemplo (datos de prueba)."))
                for o in opciones:
                    Opcion.objects.get_or_create(votacion=v, nombre=o, defaults={"descripcion": "Descripción de ejemplo."})
        self.stdout.write(self.style.SUCCESS("Datos de prueba cargados."))
