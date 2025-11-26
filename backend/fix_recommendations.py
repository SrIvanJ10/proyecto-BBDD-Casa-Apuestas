import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportpredict.settings')
django.setup()

from sportpredict.models import Usuario, Prediccion, Partido
from sportpredict.db.neo4j_utils import Neo4jClient

def fix_data():
    print("Starting recommendation system fix...")
    client = Neo4jClient()
    
    # 1. Get Users
    try:
        dios = Usuario.objects.get(username='dios')
        test_user = Usuario.objects.get(username='TestUser123')
        print(f"Found users: {dios.username} (ID: {dios.id}) and {test_user.username} (ID: {test_user.id})")
    except Usuario.DoesNotExist as e:
        print(f"Error: Could not find users. {e}")
        return

    # 2. Sync Users to Neo4j
    print("Syncing users to Neo4j...")
    client.create_user(dios.id, dios.username, dios.email)
    client.create_user(test_user.id, test_user.username, test_user.email)

    # 3. Create Friendship
    print("Creating friendship...")
    # First check if they are already friends
    if client.are_friends(dios.id, test_user.id):
        print("Users are already friends in Neo4j.")
    else:
        # Create friendship directly
        print("Establishing friendship...")
        # We can use the client methods to simulate the flow
        client.send_friend_request(dios.id, test_user.id)
        client.accept_friend_request(dios.id, test_user.id)
        print("Friendship created!")

    # 4. Sync Dios's Predictions
    print(f"Syncing predictions for {dios.username}...")
    predictions = Prediccion.objects.filter(usuario=dios)
    print(f"Found {predictions.count()} predictions in Postgres.")

    for pred in predictions:
        match = pred.partido
        print(f"Syncing match {match.id}: {match.equipo_local} vs {match.equipo_visitante}")
        
        # Ensure match exists in Neo4j
        client.create_match(
            match.id,
            match.equipo_local.nombre,
            match.equipo_visitante.nombre,
            match.equipo_local.deporte.nombre,
            match.fecha_hora
        )
        
        # Create prediction relationship
        # Format prediction string if needed (e.g., "2-1")
        pred_value = ""
        if pred.pred_goles_local is not None and pred.pred_goles_visitante is not None:
            pred_value = f"{pred.pred_goles_local}-{pred.pred_goles_visitante}"
            
        client.create_prediction(dios.id, match.id, pred_value)
        print(f"Synced prediction for match {match.id}")

    print("\nFix completed! Recommendations should now work.")

if __name__ == '__main__':
    fix_data()
