"""
API de Administración - Solo para usuarios staff
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q

from sportpredict.models import Usuario, Partido, Equipo, Deporte, Prediccion
from sportpredict.serializers import (
    UsuarioSerializer, PartidoSerializer, EquipoSerializer,
    DeporteSerializer, PrediccionSerializer
)


# ============ USERS MANAGEMENT ============

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_users_list(request):
    """GET /api/admin/users/ - Listar todos los usuarios"""
    try:
        users = Usuario.objects.all().order_by('-date_joined')
        serializer = UsuarioSerializer(users, many=True)
        return Response({'users': serializer.data, 'count': users.count()})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_user_delete(request, user_id):
    """DELETE /api/admin/users/{id}/ - Eliminar usuario"""
    try:
        user = Usuario.objects.get(id=user_id)
        username = user.username
        user.delete()
        return Response({'message': f'Usuario {username} eliminado exitosamente'})
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============ SPORTS MANAGEMENT ============

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_sports_list(request):
    """GET /api/admin/sports/ - Listar deportes"""
    try:
        sports = Deporte.objects.all()
        serializer = DeporteSerializer(sports, many=True)
        return Response({'sports': serializer.data, 'count': sports.count()})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_sport_create(request):
    """POST /api/admin/sports/ - Crear deporte"""
    try:
        nombre = request.data.get('nombre')
        if not nombre:
            return Response({'error': 'El nombre es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        sport = Deporte.objects.create(nombre=nombre, activo=True)
        serializer = DeporteSerializer(sport)
        return Response({'message': 'Deporte creado', 'sport': serializer.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_sport_delete(request, sport_id):
    """DELETE /api/admin/sports/{id}/ - Eliminar deporte"""
    try:
        sport = Deporte.objects.get(id=sport_id)
        nombre = sport.nombre
        sport.delete()
        return Response({'message': f'Deporte {nombre} eliminado'})
    except Deporte.DoesNotExist:
        return Response({'error': 'Deporte no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============ TEAMS MANAGEMENT ============

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_teams_list(request):
    """GET /api/admin/teams/ - Listar equipos"""
    try:
        teams = Equipo.objects.select_related('deporte').all()
        serializer = EquipoSerializer(teams, many=True)
        return Response({'teams': serializer.data, 'count': teams.count()})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_team_create(request):
    """POST /api/admin/teams/ - Crear equipo"""
    try:
        nombre = request.data.get('nombre')
        deporte_id = request.data.get('deporte_id')
        codigo = request.data.get('codigo')
        
        if not all([nombre, deporte_id, codigo]):
            return Response({'error': 'nombre, deporte_id y codigo son requeridos'}, status=status.HTTP_400_BAD_REQUEST)
        
        deporte = Deporte.objects.get(id=deporte_id)
        team = Equipo.objects.create(nombre=nombre, deporte=deporte, codigo=codigo)
        serializer = EquipoSerializer(team)
        return Response({'message': 'Equipo creado', 'team': serializer.data}, status=status.HTTP_201_CREATED)
    except Deporte.DoesNotExist:
        return Response({'error': 'Deporte no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_team_delete(request, team_id):
    """DELETE /api/admin/teams/{id}/ - Eliminar equipo"""
    try:
        team = Equipo.objects.get(id=team_id)
        nombre = team.nombre
        team.delete()
        return Response({'message': f'Equipo {nombre} eliminado'})
    except Equipo.DoesNotExist:
        return Response({'error': 'Equipo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============ MATCHES MANAGEMENT ============

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_matches_list(request):
    """GET /api/admin/matches/ - Listar partidos"""
    try:
        matches = Partido.objects.select_related('equipo_local', 'equipo_visitante').all().order_by('-fecha_hora')[:100]
        serializer = PartidoSerializer(matches, many=True)
        return Response({'matches': serializer.data, 'count': matches.count()})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_match_create(request):
    """POST /api/admin/matches/ - Crear partido"""
    try:
        from django.utils import timezone
        from datetime import datetime
        
        equipo_local_id = request.data.get('equipo_local_id')
        equipo_visitante_id = request.data.get('equipo_visitante_id')
        fecha_hora_str = request.data.get('fecha_hora')
        liga = request.data.get('liga', 'Liga')
        
        if not all([equipo_local_id, equipo_visitante_id, fecha_hora_str]):
            return Response({'error': 'Faltan campos requeridos'}, status=status.HTTP_400_BAD_REQUEST)
        
        equipo_local = Equipo.objects.get(id=equipo_local_id)
        equipo_visitante = Equipo.objects.get(id=equipo_visitante_id)
        fecha_hora = datetime.fromisoformat(fecha_hora_str.replace('Z', '+00:00'))
        
        match = Partido.objects.create(
            equipo_local=equipo_local,
            equipo_visitante=equipo_visitante,
            fecha_hora=fecha_hora,
            liga=liga,
            estado='PENDIENTE'
        )
        serializer = PartidoSerializer(match)
        return Response({'message': 'Partido creado', 'match': serializer.data}, status=status.HTTP_201_CREATED)
    except Equipo.DoesNotExist:
        return Response({'error': 'Equipo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def admin_match_update(request, match_id):
    """PUT /api/admin/matches/{id}/ - Actualizar partido"""
    try:
        match = Partido.objects.get(id=match_id)
        
        if 'estado' in request.data:
            match.estado = request.data['estado']
        if 'goles_local' in request.data:
            match.goles_local = request.data['goles_local']
        if 'goles_visitante' in request.data:
            match.goles_visitante = request.data['goles_visitante']
        if 'resultado_final' in request.data:
            match.resultado_final = request.data['resultado_final']
        
        match.save()
        serializer = PartidoSerializer(match)
        return Response({'message': 'Partido actualizado', 'match': serializer.data})
    except Partido.DoesNotExist:
        return Response({'error': 'Partido no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_match_delete(request, match_id):
    """DELETE /api/admin/matches/{id}/ - Eliminar partido"""
    try:
        match = Partido.objects.get(id=match_id)
        match.delete()
        return Response({'message': 'Partido eliminado'})
    except Partido.DoesNotExist:
        return Response({'error': 'Partido no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============ PREDICTIONS MANAGEMENT ============

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_predictions_list(request):
    """GET /api/admin/predictions/ - Listar predicciones"""
    try:
        predictions = Prediccion.objects.select_related('usuario', 'partido').all().order_by('-fecha_prediccion')[:100]
        serializer = PrediccionSerializer(predictions, many=True)
        return Response({'predictions': serializer.data, 'count': predictions.count()})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_prediction_delete(request, prediction_id):
    """DELETE /api/admin/predictions/{id}/ - Eliminar predicción"""
    try:
        prediction = Prediccion.objects.get(id=prediction_id)
        prediction.delete()
        return Response({'message': 'Predicción eliminada'})
    except Prediccion.DoesNotExist:
        return Response({'error': 'Predicción no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
