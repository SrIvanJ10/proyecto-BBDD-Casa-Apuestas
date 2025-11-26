from rest_framework import serializers
from .models import Usuario, Deporte, Equipo, Partido, Prediccion


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Usuario"""
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
<<<<<<< HEAD
<<<<<<< HEAD
                  'puntos_totales', 'nivel_experto', 'fecha_registro', 'avatar',
                  'tipo_suscripcion', 'is_staff', 'is_superuser']
=======
                  'puntos_totales', 'nivel_experto', 'fecha_registro', 'avatar']
>>>>>>> d381094 (v0.14)
=======
                  'puntos_totales', 'nivel_experto', 'fecha_registro', 'avatar',
                  'tipo_suscripcion', 'is_staff', 'is_superuser']
>>>>>>> 4e74b6e (v1.0)
        read_only_fields = ['id', 'fecha_registro', 'puntos_totales', 'nivel_experto']


class UsuarioRegistroSerializer(serializers.ModelSerializer):
    """Serializer para registro de usuario"""
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = Usuario
        fields = ['email', 'username', 'password', 'first_name', 'last_name']
    
    def create(self, validated_data):
        user = Usuario.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class DeporteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Deporte"""
    class Meta:
        model = Deporte
        fields = ['id', 'nombre', 'activo']


class EquipoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Equipo"""
    deporte = DeporteSerializer(read_only=True)
<<<<<<< HEAD
<<<<<<< HEAD
    deporte_nombre = serializers.CharField(source='deporte.nombre', read_only=True)
=======
>>>>>>> d381094 (v0.14)
=======
    deporte_nombre = serializers.CharField(source='deporte.nombre', read_only=True)
>>>>>>> 4e74b6e (v1.0)
    deporte_id = serializers.PrimaryKeyRelatedField(
        queryset=Deporte.objects.all(), 
        source='deporte', 
        write_only=True
    )
    
    class Meta:
        model = Equipo
<<<<<<< HEAD
<<<<<<< HEAD
        fields = ['id', 'nombre', 'deporte', 'deporte_nombre', 'deporte_id', 'logo_url', 'codigo']
=======
        fields = ['id', 'nombre', 'deporte', 'deporte_id', 'logo_url', 'codigo']
>>>>>>> d381094 (v0.14)
=======
        fields = ['id', 'nombre', 'deporte', 'deporte_nombre', 'deporte_id', 'logo_url', 'codigo']
>>>>>>> 4e74b6e (v1.0)


class EquipoSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple para Equipo (sin deporte anidado)"""
    deporte_nombre = serializers.CharField(source='deporte.nombre', read_only=True)
    
    class Meta:
        model = Equipo
        fields = ['id', 'nombre', 'codigo', 'logo_url', 'deporte_nombre']


class PartidoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Partido"""
    equipo_local = EquipoSimpleSerializer(read_only=True)
    equipo_visitante = EquipoSimpleSerializer(read_only=True)
<<<<<<< HEAD
<<<<<<< HEAD
    equipo_local_nombre = serializers.CharField(source='equipo_local.nombre', read_only=True)
    equipo_visitante_nombre = serializers.CharField(source='equipo_visitante.nombre', read_only=True)
=======
>>>>>>> d381094 (v0.14)
=======
    equipo_local_nombre = serializers.CharField(source='equipo_local.nombre', read_only=True)
    equipo_visitante_nombre = serializers.CharField(source='equipo_visitante.nombre', read_only=True)
>>>>>>> 4e74b6e (v1.0)
    equipo_local_id = serializers.PrimaryKeyRelatedField(
        queryset=Equipo.objects.all(),
        source='equipo_local',
        write_only=True
    )
    equipo_visitante_id = serializers.PrimaryKeyRelatedField(
        queryset=Equipo.objects.all(),
        source='equipo_visitante',
        write_only=True
    )
    
    class Meta:
        model = Partido
<<<<<<< HEAD
<<<<<<< HEAD
        fields = ['id', 'equipo_local', 'equipo_visitante', 'equipo_local_nombre', 
                  'equipo_visitante_nombre', 'equipo_local_id', 
=======
        fields = ['id', 'equipo_local', 'equipo_visitante', 'equipo_local_id', 
>>>>>>> d381094 (v0.14)
=======
        fields = ['id', 'equipo_local', 'equipo_visitante', 'equipo_local_nombre', 
                  'equipo_visitante_nombre', 'equipo_local_id', 
>>>>>>> 4e74b6e (v1.0)
                  'equipo_visitante_id', 'fecha_hora', 'resultado_final', 
                  'estado', 'liga', 'temporada',
                  'goles_local', 'goles_visitante',
                  'amarillas_local', 'amarillas_visitante', 'rojas_local', 'rojas_visitante',
                  'expulsiones_local', 'expulsiones_visitante', 'mvp_jugador']
        read_only_fields = ['id']


class PartidoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de partidos"""
    equipo_local = EquipoSimpleSerializer(read_only=True)
    equipo_visitante = EquipoSimpleSerializer(read_only=True)
    equipo_local_nombre = serializers.CharField(source='equipo_local.nombre', read_only=True)
    equipo_visitante_nombre = serializers.CharField(source='equipo_visitante.nombre', read_only=True)
    total_predicciones = serializers.SerializerMethodField()
    
    class Meta:
        model = Partido
        fields = ['id', 'equipo_local', 'equipo_visitante', 'equipo_local_nombre', 
                  'equipo_visitante_nombre', 'fecha_hora', 'resultado_final', 
                  'estado', 'liga', 'temporada', 'total_predicciones',
                  'goles_local', 'goles_visitante']
    
    def get_total_predicciones(self, obj):
        return obj.prediccion_set.count()


class PrediccionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Prediccion"""
    usuario = UsuarioSerializer(read_only=True)
<<<<<<< HEAD
<<<<<<< HEAD
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
=======
>>>>>>> d381094 (v0.14)
=======
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
>>>>>>> 4e74b6e (v1.0)
    partido = PartidoListSerializer(read_only=True)
    partido_id = serializers.PrimaryKeyRelatedField(
        queryset=Partido.objects.all(),
        source='partido',
        write_only=True
    )
    
    class Meta:
        model = Prediccion
<<<<<<< HEAD
<<<<<<< HEAD
        fields = ['id', 'usuario', 'usuario_username', 'partido', 'partido_id', 'prediccion', 
=======
        fields = ['id', 'usuario', 'partido', 'partido_id', 'prediccion', 
>>>>>>> d381094 (v0.14)
=======
        fields = ['id', 'usuario', 'usuario_username', 'partido', 'partido_id', 'prediccion', 
>>>>>>> 4e74b6e (v1.0)
                  'puntos_obtenidos', 'fecha_prediccion', 'correcta',
                  'pred_goles_local', 'pred_goles_visitante',
                  'pred_amarillas_local', 'pred_amarillas_visitante',
                  'pred_rojas_local', 'pred_rojas_visitante',
                  'pred_expulsiones_local', 'pred_expulsiones_visitante',
                  'pred_mvp_jugador',
                  'puntos_resultado', 'puntos_tarjetas', 'puntos_mvp', 'puntos_totales', 'evaluada']
        read_only_fields = ['id', 'usuario', 'puntos_obtenidos', 'fecha_prediccion', 'correcta',
                            'puntos_resultado', 'puntos_tarjetas', 'puntos_mvp', 'puntos_totales', 'evaluada']
    
    def validate_prediccion(self, value):
        """Validar formato de predicción antigua (ej: '2-1')"""
        if not value:
            return value
        try:
            parts = value.split('-')
            if len(parts) != 2:
                raise serializers.ValidationError("Formato inválido. Use 'X-Y' (ej: '2-1')")
            int(parts[0])
            int(parts[1])
            return value
        except (ValueError, AttributeError):
            raise serializers.ValidationError("Formato inválido. Use 'X-Y' (ej: '2-1')")


class PrediccionCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear predicciones (Legacy + Advanced)"""
    class Meta:
        model = Prediccion
        fields = ['partido_id', 'prediccion',
                  'pred_goles_local', 'pred_goles_visitante',
                  'pred_amarillas_local', 'pred_amarillas_visitante',
                  'pred_rojas_local', 'pred_rojas_visitante',
                  'pred_expulsiones_local', 'pred_expulsiones_visitante',
                  'pred_mvp_jugador']
    
    partido_id = serializers.PrimaryKeyRelatedField(
        queryset=Partido.objects.all(),
        source='partido'
    )
    prediccion = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        """Validaciones globales y límites"""
        # Validar límites
        if data.get('pred_goles_local') is not None and data['pred_goles_local'] > 200: # Cubre baloncesto y fútbol (límite superior)
             raise serializers.ValidationError({"pred_goles_local": "El valor excede el límite permitido"})
        
        if data.get('pred_amarillas_local') is not None and data['pred_amarillas_local'] > 16:
             raise serializers.ValidationError({"pred_amarillas_local": "Máximo 16 tarjetas amarillas permitidas"})
             
        if data.get('pred_rojas_local') is not None and data['pred_rojas_local'] > 5:
             raise serializers.ValidationError({"pred_rojas_local": "Máximo 5 tarjetas rojas permitidas"})
             
        if data.get('pred_expulsiones_local') is not None and data['pred_expulsiones_local'] > 5:
             raise serializers.ValidationError({"pred_expulsiones_local": "Máximo 5 expulsiones permitidas"})

        # Al menos una predicción debe existir
        has_legacy = bool(data.get('prediccion'))
        has_advanced = any([
            data.get('pred_goles_local') is not None,
            data.get('pred_mvp_jugador')
        ])
        
        if not has_legacy and not has_advanced:
            raise serializers.ValidationError("Debe realizar al menos una predicción")
            
        return data
