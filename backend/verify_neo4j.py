import os
import sys
import django
from datetime import datetime

# Setup Django environment
sys.path.append('/home/debian/luis/proyecto-BBDD-Casa-Apuestas/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportpredict.settings')
django.setup()

from sportpredict.db.neo4j_utils import Neo4jClient
from sportpredict.models import Usuario, Partido, Prediccion

def verify_neo4j():
    print("Verifying Neo4j Integration...")
    client = Neo4jClient()
    
    # 1. Test Connectivity
    if client.verify_connectivity():
        print("[OK] Neo4j Connection Successful")
    else:
        print("[FAIL] Neo4j Connection Failed")
        return

    # 2. Test Node Creation (User)
    try:
        print("Testing User Node Creation...")
        client.create_user("test_user_id", "test_user", "test@example.com")
        print("[OK] User Node Created")
    except Exception as e:
        print(f"[FAIL] User Node Creation: {e}")

    # 3. Test Node Creation (Match)
    try:
        print("Testing Match Node Creation...")
        client.create_match("test_match_id", "TeamA", "TeamB", "Soccer", datetime.now())
        print("[OK] Match Node Created")
    except Exception as e:
        print(f"[FAIL] Match Node Creation: {e}")

    # 4. Test Relationship (Prediction)
    try:
        print("Testing Prediction Relationship...")
        client.create_prediction("test_user_id", "test_match_id", "HOME")
        print("[OK] Prediction Relationship Created")
    except Exception as e:
        print(f"[FAIL] Prediction Relationship: {e}")

    # 5. Test Recommendations Query
    try:
        print("Testing Recommendations Query...")
        recs = client.get_recommended_matches("test_user_id")
        print(f"[OK] Recommendations Query executed (Result count: {len(recs)})")
    except Exception as e:
        print(f"[FAIL] Recommendations Query: {e}")

    client.close()
    print("Verification Complete.")

if __name__ == "__main__":
    verify_neo4j()
