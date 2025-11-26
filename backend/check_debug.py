
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportpredict.settings')
django.setup()

from sportpredict.models import Usuario, Partido, Prediccion
from sportpredict.db.neo4j_utils import Neo4jClient

def check_state():
    try:
        dios = Usuario.objects.get(username='dios')
        rodri = Usuario.objects.get(username='RodriBdO')
        print(f"Dios ID: {dios.id}")
        print(f"Rodri ID: {rodri.id}")
    except Usuario.DoesNotExist:
        print("Users not found in Postgres")
        return

    client = Neo4jClient()
    
    # Check friendship
    are_friends = client.are_friends(dios.id, rodri.id)
    print(f"Are friends in Neo4j: {are_friends}")

    # Check Rodri's predictions in Postgres
    rodri_preds = Prediccion.objects.filter(usuario=rodri)
    print(f"Rodri has {rodri_preds.count()} predictions in Postgres")
    
    for p in rodri_preds:
        print(f" - Match {p.partido.id} ({p.partido.equipo_local} vs {p.partido.equipo_visitante}), Status: {p.partido.estado}")

    # Check Rodri's predictions in Neo4j
    with client._driver.session() as session:
        query = """
        MATCH (u:User {id: $user_id})-[:PREDICTED]->(m:Match)
        RETURN m.id as match_id
        """
        result = session.run(query, user_id=str(rodri.id))
        neo4j_preds = [record["match_id"] for record in result]
        print(f"Rodri has {len(neo4j_preds)} predictions in Neo4j: {neo4j_preds}")

    # Check recommendations for Dios
    recs = client.get_recommended_matches(dios.id)
    print(f"Recommendations for Dios from Neo4j: {recs}")

if __name__ == '__main__':
    check_state()
