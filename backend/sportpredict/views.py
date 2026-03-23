from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import re
import json

from .models import Usuario, Deporte, Equipo, Partido, Prediccion
from sportpredict.db.redis import session_manager
# from sportpredict.db.mongo_utils import log_prediccion_mongodb  # COMENTADO - No se usa en las nuevas APIs

@require_http_methods(["GET"])
def inicio(request):
    """API: Página principal con partidos próximos y destacados"""
    partidos_proximos = Partido.objects.filter(
        estado='PENDIENTE',
        fecha_hora__gt=timezone.now()
    ).select_related('equipo_local', 'equipo_visitante', 'equipo_local__deporte').order_by('fecha_hora')[:10]

    partidos_en_vivo = Partido.objects.filter(
        estado='EN_JUEGO'
    ).select_related('equipo_local', 'equipo_visitante').order_by('fecha_hora')[:5]

    top_usuarios = Usuario.objects.filter(
        puntos_totales__gt=0
    ).order_by('-puntos_totales')[:5]

    return JsonResponse({
        'success': True,
        'data': {
            'partidos_proximos': [
                {
                    'id': p.id,
                    'equipo_local': {
                        'id': p.equipo_local.id,
                        'nombre': p.equipo_local.nombre,
                    },
                    'equipo_visitante': {
                        'id': p.equipo_visitante.id,
                        'nombre': p.equipo_visitante.nombre,
                    },
                    'fecha_hora': p.fecha_hora.isoformat(),
                    'liga': p.liga,
                    'deporte': p.equipo_local.deporte.nombre,
                } for p in partidos_proximos
            ],
            'partidos_en_vivo': [
                {
                    'id': p.id,
                    'equipo_local': p.equipo_local.nombre,
                    'equipo_visitante': p.equipo_visitante.nombre,
                    'resultado_local': p.resultado_local,
                    'resultado_visitante': p.resultado_visitante,
                } for p in partidos_en_vivo
            ],
            'top_usuarios': [
                {
                    'username': u.username,
                    'puntos_totales': u.puntos_totales,
                    'total_predicciones': u.total_predicciones,
                } for u in top_usuarios
            ]
        }
    })


@require_http_methods(["GET"])
def lista_partidos(request):
    """API: Lista completa de partidos con filtros"""
    deporte_id = request.GET.get('deporte')
    estado = request.GET.get('estado')
    liga = request.GET.get('liga')
    page = int(request.GET.get('page', 1))
    page_size = 20

    partidos = Partido.objects.all()

    if deporte_id:
        partidos = partidos.filter(
            Q(equipo_local__deporte_id=deporte_id) |
            Q(equipo_visitante__deporte_id=deporte_id)
        )

    if estado:
        partidos = partidos.filter(estado=estado)

    if liga:
        partidos = partidos.filter(liga__icontains=liga)

    partidos = partidos.select_related(
        'equipo_local', 'equipo_visitante',
        'equipo_local__deporte', 'equipo_visitante__deporte'
    ).order_by('-fecha_hora')

    total = partidos.count()
    start = (page - 1) * page_size
    end = start + page_size
    partidos_page = partidos[start:end]

    deportes = Deporte.objects.filter(activo=True)
    ligas_disponibles = Partido.objects.values_list('liga', flat=True).distinct()

    return JsonResponse({
        'success': True,
        'partidos': [
            {
                'id': p.id,
                'equipo_local': {
                    'id': p.equipo_local.id,
                    'nombre': p.equipo_local.nombre,
                },
                'equipo_visitante': {
                    'id': p.equipo_visitante.id,
                    'nombre': p.equipo_visitante.nombre,
                },
                'fecha_hora': p.fecha_hora.isoformat(),
                'liga': p.liga,
                'estado': p.estado,
                'deporte': p.equipo_local.deporte.nombre,
                'resultado_local': p.resultado_local,
                'resultado_visitante': p.resultado_visitante,
            } for p in partidos_page
        ],
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': (total + page_size - 1) // page_size,
        },
        'filtros': {
            'deportes': [{'id': d.id, 'nombre': d.nombre} for d in deportes],
            'ligas': [l for l in ligas_disponibles if l],
            'estados': [{'value': e[0], 'label': e[1]} for e in Partido.ESTADOS],
        }
    })


@require_http_methods(["GET"])
def detalle_partido(request, partido_id):
    """API: Detalle de un partido específico"""
    try:
        partido = Partido.objects.select_related(
            'equipo_local', 'equipo_visitante',
            'equipo_local__deporte'
        ).get(id=partido_id)
    except Partido.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Partido no encontrado'}, status=404)

    mi_prediccion = None
    if request.user.is_authenticated:
        try:
            pred = Prediccion.objects.get(usuario=request.user, partido=partido)
            mi_prediccion = {
                'id': pred.id,
                'prediccion': pred.prediccion,
                'fecha_prediccion': pred.fecha_prediccion.isoformat(),
                'correcta': pred.correcta,
                'puntos_obtenidos': pred.puntos_obtenidos,
            }
        except Prediccion.DoesNotExist:
            pass

    total_predicciones = partido.total_predicciones()
    distribucion = partido.predicciones_usuarios()

    partidos_relacionados = Partido.objects.filter(
        Q(equipo_local__deporte=partido.equipo_local.deporte) |
        Q(equipo_visitante__deporte=partido.equipo_local.deporte),
        estado='PENDIENTE',
        fecha_hora__gt=timezone.now()
    ).exclude(id=partido.id).select_related(
        'equipo_local', 'equipo_visitante'
    ).order_by('fecha_hora')[:5]

    return JsonResponse({
        'success': True,
        'partido': {
            'id': partido.id,
            'equipo_local': {
                'id': partido.equipo_local.id,
                'nombre': partido.equipo_local.nombre,
            },
            'equipo_visitante': {
                'id': partido.equipo_visitante.id,
                'nombre': partido.equipo_visitante.nombre,
            },
            'fecha_hora': partido.fecha_hora.isoformat(),
            'liga': partido.liga,
            'estado': partido.estado,
            'resultado_local': partido.resultado_local,
            'resultado_visitante': partido.resultado_visitante,
            'deporte': partido.equipo_local.deporte.nombre,
            'es_predecible': partido.es_predecible(),
        },
        'mi_prediccion': mi_prediccion,
        'estadisticas': {
            'total_predicciones': total_predicciones,
            'distribucion': distribucion,
        },
        'partidos_relacionados': [
            {
                'id': p.id,
                'equipo_local': p.equipo_local.nombre,
                'equipo_visitante': p.equipo_visitante.nombre,
                'fecha_hora': p.fecha_hora.isoformat(),
            } for p in partidos_relacionados
        ],
        'puede_predecir': partido.es_predecible() and request.user.is_authenticated,
    })


@login_required
@require_http_methods(["GET"])
def mis_predicciones(request):
    """API: Predicciones del usuario"""
    estado_filtro = request.GET.get('estado', 'todas')

    predicciones = Prediccion.objects.filter(
        usuario=request.user
    ).select_related(
        'partido',
        'partido__equipo_local',
        'partido__equipo_visitante'
    ).order_by('-fecha_prediccion')

    if estado_filtro == 'pendientes':
        predicciones = predicciones.filter(partido__estado='PENDIENTE')
    elif estado_filtro == 'finalizados':
        predicciones = predicciones.filter(partido__estado='FINALIZADO')
    elif estado_filtro == 'acertadas':
        predicciones = predicciones.filter(correcta=True)
    elif estado_filtro == 'falladas':
        predicciones = predicciones.filter(partido__estado='FINALIZADO', correcta=False)

    total_predicciones = Prediccion.objects.filter(usuario=request.user).count()
    predicciones_correctas = Prediccion.objects.filter(usuario=request.user, correcta=True).count()
    puntos_totales = Prediccion.objects.filter(
        usuario=request.user
    ).aggregate(total=Sum('puntos_obtenidos'))['total'] or 0

    hoy = timezone.now().date()
    predicciones_hoy = Prediccion.objects.filter(
        usuario=request.user,
        fecha_prediccion__date=hoy
    ).count()

    return JsonResponse({
        'success': True,
        'predicciones': [
            {
                'id': p.id,
                'prediccion': p.prediccion,
                'fecha_prediccion': p.fecha_prediccion.isoformat(),
                'correcta': p.correcta,
                'puntos_obtenidos': p.puntos_obtenidos,
                'partido': {
                    'id': p.partido.id,
                    'equipo_local': p.partido.equipo_local.nombre,
                    'equipo_visitante': p.partido.equipo_visitante.nombre,
                    'fecha_hora': p.partido.fecha_hora.isoformat(),
                    'estado': p.partido.estado,
                    'resultado_local': p.partido.resultado_local,
                    'resultado_visitante': p.partido.resultado_visitante,
                }
            } for p in predicciones
        ],
        'estadisticas': {
            'total_predicciones': total_predicciones,
            'predicciones_correctas': predicciones_correctas,
            'puntos_totales': puntos_totales,
            'predicciones_hoy': predicciones_hoy,
            'porcentaje_aciertos': round(
                (predicciones_correctas / total_predicciones * 100) if total_predicciones > 0 else 0,
                1
            ),
        },
        'estado_filtro': estado_filtro,
    })


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_prediccion(request, prediccion_id):
    """API: Eliminar una predicción"""
    try:
        prediccion = Prediccion.objects.get(id=prediccion_id, usuario=request.user)

        if not prediccion.es_editable():
            return JsonResponse({'success': False, 'error': 'No se puede eliminar esta predicción'}, status=400)

        partido_id = prediccion.partido.id
        prediccion.delete()

        return JsonResponse({'success': True, 'message': 'Predicción eliminada correctamente', 'partido_id': partido_id})

    except Prediccion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Predicción no encontrada'}, status=404)


@login_required
@require_http_methods(["GET"])
def dashboard(request):
    """API: Dashboard personal del usuario"""
    estadisticas_usuario = {
        'total_predicciones': Prediccion.objects.filter(usuario=request.user).count(),
        'predicciones_correctas': Prediccion.objects.filter(usuario=request.user, correcta=True).count(),
        'puntos_totales': request.user.puntos_totales,
        'racha_actual': request.user.racha_actual,
        'mejor_racha': request.user.mejor_racha,
        'nivel_experto': request.user.nivel_experto,
    }

    predicciones_recientes = Prediccion.objects.filter(
        usuario=request.user
    ).select_related(
        'partido', 'partido__equipo_local', 'partido__equipo_visitante'
    ).order_by('-fecha_prediccion')[:5]

    deportes_favoritos = Prediccion.objects.filter(
        usuario=request.user
    ).values_list('partido__equipo_local__deporte', flat=True).distinct()

    partidos_recomendados = Partido.objects.filter(
        equipo_local__deporte__in=deportes_favoritos,
        estado='PENDIENTE',
        fecha_hora__gt=timezone.now()
    ).exclude(
        prediccion__usuario=request.user
    ).select_related('equipo_local', 'equipo_visitante').order_by('fecha_hora')[:5]

    return JsonResponse({
        'success': True,
        'estadisticas': estadisticas_usuario,
        'predicciones_recientes': [
            {
                'id': p.id,
                'prediccion': p.prediccion,
                'partido': {
                    'equipo_local': p.partido.equipo_local.nombre,
                    'equipo_visitante': p.partido.equipo_visitante.nombre,
                },
                'correcta': p.correcta,
                'puntos': p.puntos_obtenidos,
            } for p in predicciones_recientes
        ],
        'partidos_recomendados': [
            {
                'id': p.id,
                'equipo_local': p.equipo_local.nombre,
                'equipo_visitante': p.equipo_visitante.nombre,
                'fecha_hora': p.fecha_hora.isoformat(),
            } for p in partidos_recomendados
        ],
    })


@require_http_methods(["GET"])
def leaderboard(request):
    """API: Tabla de clasificación global"""
    top_usuarios = Usuario.objects.filter(
        puntos_totales__gt=0
    ).annotate(
        num_predicciones=Count('prediccion')
    ).order_by('-puntos_totales')[:50]

    posicion_usuario = None
    if request.user.is_authenticated:
        usuarios_por_delante = Usuario.objects.filter(
            puntos_totales__gt=request.user.puntos_totales
        ).count()
        posicion_usuario = usuarios_por_delante + 1

    total_usuarios = Usuario.objects.count()
    total_predicciones = Prediccion.objects.count()
    total_partidos = Partido.objects.count()

    return JsonResponse({
        'success': True,
        'leaderboard': [
            {
                'posicion': idx + 1,
                'username': u.username,
                'puntos_totales': u.puntos_totales,
                'total_predicciones': u.num_predicciones,
                'racha_actual': u.racha_actual,
            } for idx, u in enumerate(top_usuarios)
        ],
        'posicion_usuario': posicion_usuario,
        'estadisticas_globales': {
            'total_usuarios': total_usuarios,
            'total_predicciones': total_predicciones,
            'total_partidos': total_partidos,
        }
    })


@require_http_methods(["GET"])
def lista_deportes(request):
    """API: Lista de deportes"""
    deportes = Deporte.objects.filter(activo=True).annotate(num_equipos=Count('equipo'))

    return JsonResponse({
        'success': True,
        'deportes': [
            {
                'id': d.id,
                'nombre': d.nombre,
                'icono': d.icono,
                'descripcion': d.descripcion,
                'num_equipos': d.num_equipos,
            } for d in deportes
        ]
    })


@require_http_methods(["GET"])
def detalle_deporte(request, deporte_id):
    """API: Detalle de un deporte"""
    try:
        deporte = Deporte.objects.get(id=deporte_id)
    except Deporte.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Deporte no encontrado'}, status=404)

    equipos = Equipo.objects.filter(deporte=deporte, activo=True)
    partidos_proximos = deporte.partidos_proximos()[:10]

    return JsonResponse({
        'success': True,
        'deporte': {
            'id': deporte.id,
            'nombre': deporte.nombre,
            'icono': deporte.icono,
            'descripcion': deporte.descripcion,
        },
        'equipos': [{'id': e.id, 'nombre': e.nombre} for e in equipos],
        'partidos_proximos': [
            {
                'id': p.id,
                'equipo_local': p.equipo_local.nombre,
                'equipo_visitante': p.equipo_visitante.nombre,
                'fecha_hora': p.fecha_hora.isoformat(),
            } for p in partidos_proximos
        ]
    })


@require_http_methods(["GET"])
def lista_equipos(request):
    """API: Lista de equipos"""
    deporte_id = request.GET.get('deporte')

    equipos = Equipo.objects.filter(activo=True)

    if deporte_id:
        equipos = equipos.filter(deporte_id=deporte_id)

    equipos = equipos.select_related('deporte').order_by('deporte__nombre', 'nombre')

    return JsonResponse({
        'success': True,
        'equipos': [
            {
                'id': e.id,
                'nombre': e.nombre,
                'deporte': {'id': e.deporte.id, 'nombre': e.deporte.nombre},
            } for e in equipos
        ]
    })


@require_http_methods(["GET"])
def detalle_equipo(request, equipo_id):
    """API: Detalle de un equipo"""
    try:
        equipo = Equipo.objects.select_related('deporte').get(id=equipo_id)
    except Equipo.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Equipo no encontrado'}, status=404)

    partidos_proximos = equipo.partidos_totales().filter(
        estado='PENDIENTE',
        fecha_hora__gt=timezone.now()
    ).select_related('equipo_local', 'equipo_visitante').order_by('fecha_hora')[:5]

    estadisticas = equipo.estadisticas()

    return JsonResponse({
        'success': True,
        'equipo': {
            'id': equipo.id,
            'nombre': equipo.nombre,
            'deporte': equipo.deporte.nombre,
        },
        'partidos_proximos': [
            {
                'id': p.id,
                'equipo_local': p.equipo_local.nombre,
                'equipo_visitante': p.equipo_visitante.nombre,
                'fecha_hora': p.fecha_hora.isoformat(),
            } for p in partidos_proximos
        ],
        'estadisticas': estadisticas,
    })


@require_http_methods(["GET"])
def estadisticas_globales(request):
    """API: Estadísticas globales de la plataforma"""
    total_usuarios = Usuario.objects.count()
    total_predicciones = Prediccion.objects.count()
    total_partidos = Partido.objects.count()
    partidos_finalizados = Partido.objects.filter(estado='FINALIZADO').count()

    deporte_popular = Deporte.objects.annotate(
        num_predicciones=Count('equipo__partidos_local__prediccion') +
                         Count('equipo__partidos_visitante__prediccion')
    ).order_by('-num_predicciones').first()

    usuario_top = Usuario.objects.order_by('-puntos_totales').first()

    return JsonResponse({
        'success': True,
        'estadisticas': {
            'total_usuarios': total_usuarios,
            'total_predicciones': total_predicciones,
            'total_partidos': total_partidos,
            'partidos_finalizados': partidos_finalizados,
            'deporte_popular': {
                'nombre': deporte_popular.nombre,
                'predicciones': deporte_popular.num_predicciones,
            } if deporte_popular else None,
            'usuario_top': {
                'username': usuario_top.username,
                'puntos': usuario_top.puntos_totales,
            } if usuario_top else None,
        }
    })


@login_required
@require_http_methods(["GET"])
def recomendaciones(request):
    """API: Recomendaciones personalizadas"""
    partidos_recomendados = Partido.objects.filter(
        estado='PENDIENTE',
        fecha_hora__gt=timezone.now()
    ).exclude(
        prediccion__usuario=request.user
    ).select_related('equipo_local', 'equipo_visitante').order_by('?')[:5]

    return JsonResponse({
        'success': True,
        'recomendaciones': [
            {
                'id': p.id,
                'equipo_local': p.equipo_local.nombre,
                'equipo_visitante': p.equipo_visitante.nombre,
                'fecha_hora': p.fecha_hora.isoformat(),
                'liga': p.liga,
            } for p in partidos_recomendados
        ],
        'mensaje': 'Sistema de recomendaciones en desarrollo (usando Neo4j)',
    })
