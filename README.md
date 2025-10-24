## 📋 Estado del Proyecto

Para repartir las tareas del proyecto y organizarnos hemos utilizado [Trello](https://trello.com/b/Ssf3yjV7/casino).

También puedes ver la [wiki](https://github.com/SrIvanJ10/proyecto-BBDD-Casa-Apuestas/wiki) donde vamos a poner más documentación del proyecto y también la usaremos para coordinarnos a la hora de poner nomenclaturas para funciones, variables, ... , con el objetivo de hacer que el código sea más coherente incluso entre las bases de datos, backend y frontend.

Para explicarme mejor, pongo este ejemplo:

``` python
# Luis escribe:
def obtener_usuario(id):
    usuario = Usuario.objects.get(id=id)
    return usuario

# Iván escribes:
def get_user(user_id):
    return User.objects.filter(id=user_id).first()

# Rodrii espera: ¿cuál API usar?
```

Para no descoordinarnos mucho y hacer que el código sea más fácil de mantener
