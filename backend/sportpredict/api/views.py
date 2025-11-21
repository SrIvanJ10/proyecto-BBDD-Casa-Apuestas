from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count, Sum
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.cache import cache
import re
import json

from sportpredict.models import Usuario, Deporte, Equipo, Partido, Prediccion
from sportpredict.db.redis.sessions import SessionManager

def inicio(request):
    partidos_proximos = Partido.objects.filter(
        estado='PENDIENTE',
        fecha_hora__gt=timezone.now()
    ).order_by('fecha_hora')[:10]

    partidos_en_vivo = Partido.objects.filter(
        estado='EN_JUEGO'
    ).order_by('fecha_hora')[:5]

    top_usuarios = Usuario.objects.filter(
        puntos_totales__gt=0
    ).order_by('-puntos_totales')[:5]

    context = {
        'partidos_proximos': partidos_proximos,
        'partidos_en_vivo': partidos_en_vivo,
        'top_usuarios': top_usuarios,
    }

    return render(request, 'predicciones/inicio.html', context)

def lista_partidos(request):
    deporte_id = request.GET.get('deporte')
    estado = request.GET.get('estado')
    liga = request.GET.get('liga')

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
    
    paginator = Paginator(partidos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    deportes = Deporte.objects.filter(activo=True)
    ligas_disponibles = Partido.objects.values_list('liga', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'deportes': deportes,
        'ligas_disponibles': [liga for liga in ligas_disponibles if liga],
        'estados_partido': Partido.ESTADOS,
        'filtros_aplicados': {
            'deporte': deporte_id,
            'estado': estado,
            'liga': liga,
        }
    }
    
    return render(request, 'predicciones/lista_partidos.html', context)

def detalle_partido(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)
    
    mi_prediccion = None
    if request.user.is_authenticated:
        try:
            mi_prediccion = Prediccion.objects.get(
                usuario=request.user, 
                partido=partido
            )
        except Prediccion.DoesNotExist:
            pass
    
    total_predicciones = partido.total_predicciones()
    distribucion_predicciones = partido.predicciones_usuarios()
    
    partidos_relacionados = Partido.objects.filter(
        Q(equipo_local__deporte=partido.equipo_local.deporte) |
        Q(equipo_visitante__deporte=partido.equipo_local.deporte),
        estado='PENDIENTE',
        fecha_hora__gt=timezone.now()
    ).exclude(id=partido.id).order_by('fecha_hora')[:5]
    
    context = {
        'partido': partido,
        'mi_prediccion': mi_prediccion,
        'total_predicciones': total_predicciones,
        'distribucion_predicciones': distribucion_predicciones,
        'partidos_relacionados': partidos_relacionados,
        'puede_predecir': partido.es_predecible() and request.user.is_authenticated,
    }
    
    return render(request, 'predicciones/detalle_partido.html', context)

@login_required
def hacer_prediccion(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)
    
    if not partido.es_predecible():
        messages.error(request, "No se pueden hacer predicciones para este partido")
        return redirect('predicciones:detalle_partido', partido_id=partido_id)
    
    session_manager = SessionManager()
    current_predictions = session_manager.get_today_predictions(request.user.id)
    
    if not session_manager.can_make_prediction(request.user.id):
        messages.error(request, "Límite diario alcanzado (10 predicciones máximo)")
        return redirect('predicciones:detalle_partido', partido_id=partido_id)
    
    try:
        prediccion_existente = Prediccion.objects.get(
            usuario=request.user, 
            partido=partido
        )
        es_edicion = True
    except Prediccion.DoesNotExist:
        prediccion_existente = None
        es_edicion = False
    
    if request.method == 'POST':
        prediccion_texto = request.POST.get('prediccion', '').strip()
        
        if not re.match(r'^\d+-\d+$', prediccion_texto):
            messages.error(request, "Formato inválido. Use: 2-1, 0-0, etc.")
            return render(request, 'predicciones/hacer_prediccion.html', {
                'partido': partido,
                'prediccion_actual': prediccion_texto,
                'es_edicion': es_edicion,
                'predicciones_hoy': current_predictions,
            })
        
        if es_edicion:
            prediccion_existente.prediccion = prediccion_texto
            prediccion_existente.fecha_prediccion = timezone.now()
            prediccion_existente.save()
            action_type = 'updated'
            prediccion = prediccion_existente
        else:
            prediccion = Prediccion.objects.create(
                usuario=request.user,
                partido=partido,
                prediccion=prediccion_texto
            )
            action_type = 'created'
            session_manager.increment_predictions(request.user.id)
        
        messages.success(request, 
            f"Predicción {'actualizada' if es_edicion else 'guardada'} correctamente"
        )
        return redirect('predicciones:mis_predicciones')
    
    context = {
        'partido': partido,
        'prediccion_actual': prediccion_existente.prediccion if prediccion_existente else "",
        'es_edicion': es_edicion,
        'predicciones_hoy': current_predictions,
        'limite_diario': 10,
    }
    
    return render(request, 'predicciones/hacer_prediccion.html', context)

@login_required
def mis_predicciones(request):
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
        predicciones = predicciones.filter(
            partido__estado='FINALIZADO', 
            correcta=False
        )
    
    total_predicciones = Prediccion.objects.filter(usuario=request.user).count()
    predicciones_correctas = Prediccion.objects.filter(
        usuario=request.user, 
        correcta=True
    ).count()
    puntos_totales = Prediccion.objects.filter(
        usuario=request.user
    ).aggregate(total=Sum('puntos_obtenidos'))['total'] or 0
    
    session_manager = SessionManager()
    predicciones_hoy = session_manager.get_today_predictions(request.user.id)
    
    context = {
        'predicciones': predicciones,
        'total_predicciones': total_predicciones,
        'predicciones_correctas': predicciones_correctas,
        'puntos_totales': puntos_totales,
        'predicciones_hoy': predicciones_hoy,
        'porcentaje_aciertos': round(
            (predicciones_correctas / total_predicciones * 100) if total_predicciones > 0 else 0, 
            1
        ),
        'estado_filtro': estado_filtro,
    }
    
    return render(request, 'predicciones/mis_predicciones.html', context)

@login_required
def eliminar_prediccion(request, prediccion_id):
    prediccion = get_object_or_404(
        Prediccion, 
        id=prediccion_id, 
        usuario=request.user
    )
    
    if not prediccion.es_editable():
        messages.error(request, "No se puede eliminar esta predicción")
        return redirect('predicciones:mis_predicciones')
    
    partido_id = prediccion.partido.id
    prediccion.delete()
    
    messages.success(request, "Predicción eliminada correctamente")
    return redirect('predicciones:detalle_partido', partido_id=partido_id)

@login_required
def dashboard(request):
    estadisticas_usuario = {
        'total_predicciones': Prediccion.objects.filter(usuario=request.user).count(),
        'predicciones_correctas': Prediccion.objects.filter(
            usuario=request.user, correcta=True
        ).count(),
        'puntos_totales': request.user.puntos_totales,
        'racha_actual': request.user.racha_actual,
        'mejor_racha': request.user.mejor_racha,
        'nivel_experto': request.user.nivel_experto,
    }
    
    predicciones_recientes = Prediccion.objects.filter(
        usuario=request.user
    ).select_related('partido').order_by('-fecha_prediccion')[:5]
    
    deportes_favoritos = Prediccion.objects.filter(
        usuario=request.user
    ).values_list(
        'partido__equipo_local__deporte', 
        flat=True
    ).distinct()
    
    partidos_recomendados = Partido.objects.filter(
        equipo_local__deporte__in=deportes_favoritos,
        estado='PENDIENTE',
        fecha_hora__gt=timezone.now()
    ).exclude(
        prediccion__usuario=request.user
    ).order_by('fecha_hora')[:5]
    
    context = {
        'estadisticas_usuario': estadisticas_usuario,
        'predicciones_recientes': predicciones_recientes,
        'partidos_recomendados': partidos_recomendados,
    }
    
    return render(request, 'predicciones/dashboard.html', context)

def leaderboard(request):
    top_usuarios = Usuario.objects.filter(
        puntos_totales__gt=0
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
    
    context = {
        'top_usuarios': top_usuarios,
        'posicion_usuario': posicion_usuario,
        'total_usuarios': total_usuarios,
        'total_predicciones': total_predicciones,
        'total_partidos': total_partidos,
    }
    
    return render(request, 'predicciones/leaderboard.html', context)

def lista_deportes(request):
    deportes = Deporte.objects.filter(activo=True).annotate(
        num_equipos=Count('equipo'),
        num_partidos=Count('partido')
    )
    
    return render(request, 'predicciones/lista_deportes.html', {
        'deportes': deportes
    })

def detalle_deporte(request, deporte_id):
    deporte = get_object_or_404(Deporte, id=deporte_id)
    
    equipos = Equipo.objects.filter(deporte=deporte, activo=True)
    partidos_proximos = deporte.partidos_proximos()[:10]
    
    return render(request, 'predicciones/detalle_deporte.html', {
        'deporte': deporte,
        'equipos': equipos,
        'partidos_proximos': partidos_proximos,
    })

def lista_equipos(request):
    deporte_id = request.GET.get('deporte')
    
    equipos = Equipo.objects.filter(activo=True)
    
    if deporte_id:
        equipos = equipos.filter(deporte_id=deporte_id)
    
    equipos = equipos.select_related('deporte').order_by('deporte__nombre', 'nombre')
    
    deportes = Deporte.objects.filter(activo=True)
    
    return render(request, 'predicciones/lista_equipos.html', {
        'equipos': equipos,
        'deportes': deportes,
        'deporte_filtro': deporte_id,
    })

def detalle_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    
    partidos_local = equipo.partidos_local.all().order_by('-fecha_hora')[:10]
    partidos_visitante = equipo.partidos_visitante.all().order_by('-fecha_hora')[:10]
    partidos_proximos = equipo.partidos_totales().filter(
        estado='PENDIENTE',
        fecha_hora__gt=timezone.now()
    ).order_by('fecha_hora')[:5]
    
    estadisticas = equipo.estadisticas()
    
    return render(request, 'predicciones/detalle_equipo.html', {
        'equipo': equipo,
        'partidos_local': partidos_local,
        'partidos_visitante': partidos_visitante,
        'partidos_proximos': partidos_proximos,
        'estadisticas': estadisticas,
    })

def api_partidos_proximos(request):
    partidos = Partido.objects.filter(
        estado='PENDIENTE',
        fecha_hora__gt=timezone.now()
    ).select_related(
        'equipo_local', 'equipo_visitante'
    ).order_by('fecha_hora')[:10]
    
    data = []
    for partido in partidos:
        data.append({
            'id': partido.id,
            'equipo_local': partido.equipo_local.nombre,
            'equipo_visitante': partido.equipo_visitante.nombre,
            'fecha_hora': partido.fecha_hora.strftime('%d/%m/%Y %H:%M'),
            'liga': partido.liga,
            'deporte': partido.equipo_local.deporte.nombre,
        })
    
    return JsonResponse({'partidos': data})

@login_required
def api_estadisticas_usuario(request):
    session_manager = SessionManager()
    predicciones_hoy = session_manager.get_today_predictions(request.user.id)
    
    estadisticas = {
        'puntos_totales': request.user.puntos_totales,
        'total_predicciones': request.user.total_predicciones,
        'predicciones_correctas': request.user.predicciones_correctas,
        'porcentaje_aciertos': request.user.porcentaje_aciertos(),
        'racha_actual': request.user.racha_actual,
        'mejor_racha': request.user.mejor_racha,
        'predicciones_hoy': predicciones_hoy,
        'predicciones_restantes': 10 - predicciones_hoy,
    }
    
    return JsonResponse(estadisticas)

@login_required
def recomendaciones(request):
    partidos_recomendados = Partido.objects.filter(
        estado='PENDIENTE',
        fecha_hora__gt=timezone.now()
    ).exclude(
        prediccion__usuario=request.user
    ).order_by('?')[:5]
    
    context = {
        'partidos_recomendados': partidos_recomendados,
        'mensaje': 'Sistema de recomendaciones en desarrollo (usando Neo4j)',
    }
    
    return render(request, 'predicciones/recomendaciones.html', context)

def estadisticas_globales(request):
    total_usuarios = Usuario.objects.count()
    total_predicciones = Prediccion.objects.count()
    total_partidos = Partido.objects.count()
    partidos_finalizados = Partido.objects.filter(estado='FINALIZADO').count()
    
    deporte_popular = Deporte.objects.annotate(
        num_predicciones=Count('equipo__partidos_local__prediccion') + 
                         Count('equipo__partidos_visitante__prediccion')
    ).order_by('-num_predicciones').first()
    
    usuario_top = Usuario.objects.order_by('-puntos_totales').first()
    
    context = {
        'total_usuarios': total_usuarios,
        'total_predicciones': total_predicciones,
        'total_partidos': total_partidos,
        'partidos_finalizados': partidos_finalizados,
        'deporte_popular': deporte_popular,
        'usuario_top': usuario_top,
    }
    
    return render(request, 'predicciones/estadisticas_globales.html', context)