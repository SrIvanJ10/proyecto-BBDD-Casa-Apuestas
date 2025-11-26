from neo4j import GraphDatabase
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Neo4jClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Neo4jClient, cls).__new__(cls)
            cls._instance._driver = None
        return cls._instance

    def __init__(self):
        if self._driver is None:
            try:
                self._driver = GraphDatabase.driver(
                    settings.NEO4J_URI,
                    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
                )
            except Exception as e:
                logger.error(f"Failed to connect to Neo4j: {e}")

    def close(self):
        if self._driver:
            self._driver.close()
            self._driver = None

    def verify_connectivity(self):
        try:
            self._driver.verify_connectivity()
            return True
        except Exception as e:
            logger.error(f"Neo4j connectivity check failed: {e}")
            return False

    def create_user(self, user_id, username, email):
        """Create or update a User node in Neo4j"""
        query = """
        MERGE (u:User {id: $user_id})
        SET u.username = $username,
            u.email = $email,
            u.last_updated = datetime()
        RETURN u
        """
        try:
            with self._driver.session() as session:
                session.run(query, user_id=str(user_id), username=username, email=email)
                logger.info(f"Synced User {username} to Neo4j")
        except Exception as e:
            logger.error(f"Error creating user in Neo4j: {e}")

    def create_match(self, match_id, team_home, team_away, sport, date):
        """Create or update a Match node in Neo4j"""
        query = """
        MERGE (m:Match {id: $match_id})
        SET m.team_home = $team_home,
            m.team_away = $team_away,
            m.sport = $sport,
            m.date = $date,
            m.last_updated = datetime()
        
        MERGE (h:Team {name: $team_home})
        MERGE (a:Team {name: $team_away})
        MERGE (s:Sport {name: $sport})
        
        MERGE (h)-[:PLAYS_IN]->(m)
        MERGE (a)-[:PLAYS_IN]->(m)
        MERGE (h)-[:BELONGS_TO]->(s)
        MERGE (a)-[:BELONGS_TO]->(s)
        """
        try:
            with self._driver.session() as session:
                session.run(query, 
                           match_id=str(match_id), 
                           team_home=team_home, 
                           team_away=team_away, 
                           sport=sport,
                           date=str(date))
                logger.info(f"Synced Match {match_id} to Neo4j")
        except Exception as e:
            logger.error(f"Error creating match in Neo4j: {e}")

    def create_prediction(self, user_id, match_id, prediction):
        """Create a PREDICTED relationship with supported_team"""
        supported_team = None
        try:
            if prediction and '-' in prediction:
                parts = prediction.split('-')
                home_score = int(parts[0])
                away_score = int(parts[1])
                
                # Fetch match details to get team names (this is a bit expensive, but necessary if we don't pass names)
                # Alternatively, we can fetch the match node from Neo4j first
                with self._driver.session() as session:
                    result = session.run("MATCH (m:Match {id: $match_id}) RETURN m.team_home, m.team_away", match_id=str(match_id))
                    record = result.single()
                    if record:
                        if home_score > away_score:
                            supported_team = record["m.team_home"]
                        elif away_score > home_score:
                            supported_team = record["m.team_away"]
        except Exception as e:
            logger.warning(f"Could not determine supported team: {e}")

        query = """
        MATCH (u:User {id: $user_id})
        MATCH (m:Match {id: $match_id})
        MERGE (u)-[r:PREDICTED]->(m)
        SET r.prediction = $prediction,
            r.supported_team = $supported_team,
            r.timestamp = datetime()
        RETURN r
        """
        try:
            with self._driver.session() as session:
                session.run(query, user_id=str(user_id), match_id=str(match_id), prediction=prediction, supported_team=supported_team)
                logger.info(f"Synced Prediction user={user_id} match={match_id} to Neo4j (Supported: {supported_team})")
        except Exception as e:
            logger.error(f"Error creating prediction in Neo4j: {e}")

    def get_recommended_matches(self, user_id, limit=10):
        """
        Friend-Based Filtering: Recommend matches that friends have bet on
        Only shows matches with estado='PENDIENTE' (not started yet)
        """
        query = """
        // 1. Find all friends of the user
        MATCH (u:User {id: $user_id})-[:FRIENDS]-(friend:User)
        
        // 2. Find matches where friends have placed predictions
        MATCH (friend)-[:PREDICTED]->(m:Match)
        WHERE NOT (u)-[:PREDICTED]->(m) // Exclude already predicted by user
        
        // 3. Count how many friends bet on each match
        WITH m, count(DISTINCT friend) as friend_count
        
        RETURN m.id as match_id, friend_count
        ORDER BY friend_count DESC, m.date ASC
        LIMIT $limit
        """
        try:
            with self._driver.session() as session:
                result = session.run(query, user_id=str(user_id), limit=limit)
                return [record["match_id"] for record in result]
        except Exception as e:
            logger.error(f"Error getting recommendations: {e}")
            return []

    def get_similar_users(self, user_id, limit=10):
        """
        Find users who predicted same matches with same outcomes
        """
        query = """
        MATCH (u:User {id: $user_id})-[r1:PREDICTED]->(m:Match)<-[r2:PREDICTED]-(other:User)
        WHERE r1.prediction = r2.prediction
        RETURN other.id as user_id, count(m) as similarity
        ORDER BY similarity DESC
        LIMIT $limit
        """
        try:
            with self._driver.session() as session:
                result = session.run(query, user_id=str(user_id), limit=limit)
                return [record["user_id"] for record in result]
        except Exception as e:
            logger.error(f"Error getting similar users: {e}")
            return []

    # ========== FRIEND RELATIONSHIP METHODS ==========
    
    def send_friend_request(self, from_user_id, to_user_id):
        """
        Send a friend request from one user to another
        Creates a FRIEND_REQUEST relationship with status PENDING
        """
        query = """
        MATCH (from:User {id: $from_user_id})
        MATCH (to:User {id: $to_user_id})
        
        // Check if relationship already exists
        OPTIONAL MATCH (from)-[existing:FRIEND_REQUEST|FRIENDS]-(to)
        
        WITH from, to, existing
        WHERE existing IS NULL
        
        CREATE (from)-[r:FRIEND_REQUEST {
            status: 'PENDING',
            created_at: datetime()
        }]->(to)
        
        RETURN r
        """
        try:
            with self._driver.session() as session:
                result = session.run(query, from_user_id=str(from_user_id), to_user_id=str(to_user_id))
                record = result.single()
                if record:
                    logger.info(f"Friend request sent from {from_user_id} to {to_user_id}")
                    return True
                else:
                    logger.warning(f"Friend request already exists between {from_user_id} and {to_user_id}")
                    return False
        except Exception as e:
            logger.error(f"Error sending friend request: {e}")
            return False

    def accept_friend_request(self, from_user_id, to_user_id):
        """
        Accept a friend request
        Converts FRIEND_REQUEST to bidirectional FRIENDS relationship
        """
        query = """
        MATCH (from:User {id: $from_user_id})-[req:FRIEND_REQUEST {status: 'PENDING'}]->(to:User {id: $to_user_id})
        
        // Delete the request
        DELETE req
        
        // Create bidirectional FRIENDS relationship
        CREATE (from)-[:FRIENDS {created_at: datetime()}]->(to)
        CREATE (to)-[:FRIENDS {created_at: datetime()}]->(from)
        
        RETURN from, to
        """
        try:
            with self._driver.session() as session:
                result = session.run(query, from_user_id=str(from_user_id), to_user_id=str(to_user_id))
                record = result.single()
                if record:
                    logger.info(f"Friend request accepted: {from_user_id} and {to_user_id} are now friends")
                    return True
                else:
                    logger.warning(f"No pending friend request found from {from_user_id} to {to_user_id}")
                    return False
        except Exception as e:
            logger.error(f"Error accepting friend request: {e}")
            return False

    def reject_friend_request(self, from_user_id, to_user_id):
        """
        Reject a friend request
        Deletes the FRIEND_REQUEST relationship
        """
        query = """
        MATCH (from:User {id: $from_user_id})-[req:FRIEND_REQUEST {status: 'PENDING'}]->(to:User {id: $to_user_id})
        DELETE req
        RETURN count(req) as deleted
        """
        try:
            with self._driver.session() as session:
                result = session.run(query, from_user_id=str(from_user_id), to_user_id=str(to_user_id))
                record = result.single()
                if record and record["deleted"] > 0:
                    logger.info(f"Friend request rejected from {from_user_id} to {to_user_id}")
                    return True
                else:
                    logger.warning(f"No pending friend request found from {from_user_id} to {to_user_id}")
                    return False
        except Exception as e:
            logger.error(f"Error rejecting friend request: {e}")
            return False

    def remove_friend(self, user_id1, user_id2):
        """
        Remove a friend relationship
        Deletes both directions of the FRIENDS relationship
        """
        query = """
        MATCH (u1:User {id: $user_id1})-[f:FRIENDS]-(u2:User {id: $user_id2})
        DELETE f
        RETURN count(f) as deleted
        """
        try:
            with self._driver.session() as session:
                result = session.run(query, user_id1=str(user_id1), user_id2=str(user_id2))
                record = result.single()
                if record and record["deleted"] > 0:
                    logger.info(f"Friendship removed between {user_id1} and {user_id2}")
                    return True
                else:
                    logger.warning(f"No friendship found between {user_id1} and {user_id2}")
                    return False
        except Exception as e:
            logger.error(f"Error removing friend: {e}")
            return False

    def get_friends(self, user_id):
        """
        Get all friends of a user
        Returns list of user IDs
        """
        query = """
        MATCH (u:User {id: $user_id})-[:FRIENDS]->(friend:User)
        RETURN friend.id as user_id, friend.username as username, friend.email as email
        ORDER BY friend.username
        """
        try:
            with self._driver.session() as session:
                result = session.run(query, user_id=str(user_id))
                return [{"user_id": record["user_id"], "username": record["username"], "email": record["email"]} 
                        for record in result]
        except Exception as e:
            logger.error(f"Error getting friends: {e}")
            return []

    def get_pending_requests(self, user_id):
        """
        Get all pending friend requests received by a user
        Returns list of user IDs who sent the requests
        """
        query = """
        MATCH (from:User)-[req:FRIEND_REQUEST {status: 'PENDING'}]->(to:User {id: $user_id})
        RETURN from.id as user_id, from.username as username, from.email as email, req.created_at as created_at
        ORDER BY req.created_at DESC
        """
        try:
            with self._driver.session() as session:
                result = session.run(query, user_id=str(user_id))
                return [{"user_id": record["user_id"], "username": record["username"], 
                        "email": record["email"], "created_at": record["created_at"]} 
                        for record in result]
        except Exception as e:
            logger.error(f"Error getting pending requests: {e}")
            return []

    def get_sent_requests(self, user_id):
        """
        Get all pending friend requests sent by a user
        Returns list of user IDs to whom requests were sent
        """
        query = """
        MATCH (from:User {id: $user_id})-[req:FRIEND_REQUEST {status: 'PENDING'}]->(to:User)
        RETURN to.id as user_id, to.username as username, to.email as email, req.created_at as created_at
        ORDER BY req.created_at DESC
        """
        try:
            with self._driver.session() as session:
                result = session.run(query, user_id=str(user_id))
                return [{"user_id": record["user_id"], "username": record["username"], 
                        "email": record["email"], "created_at": record["created_at"]} 
                        for record in result]
        except Exception as e:
            logger.error(f"Error getting sent requests: {e}")
            return []

    def are_friends(self, user_id1, user_id2):
        """
        Check if two users are friends
        Returns True if they are friends, False otherwise
        """
        query = """
        MATCH (u1:User {id: $user_id1})-[:FRIENDS]-(u2:User {id: $user_id2})
        RETURN count(*) > 0 as are_friends
        """
        try:
            with self._driver.session() as session:
                result = session.run(query, user_id1=str(user_id1), user_id2=str(user_id2))
                record = result.single()
                return record["are_friends"] if record else False
        except Exception as e:
            logger.error(f"Error checking friendship: {e}")
            return False

    def get_friend_request_status(self, from_user_id, to_user_id):
        """
        Get the status of a friend request between two users
        Returns: 'friends', 'pending_sent', 'pending_received', 'none'
        """
        query = """
        MATCH (from:User {id: $from_user_id})
        MATCH (to:User {id: $to_user_id})
        
        OPTIONAL MATCH (from)-[f:FRIENDS]-(to)
        WITH from, to, f IS NOT NULL as are_friends
        
        OPTIONAL MATCH (from)-[req_sent:FRIEND_REQUEST {status: 'PENDING'}]->(to)
        OPTIONAL MATCH (to)-[req_received:FRIEND_REQUEST {status: 'PENDING'}]->(from)
        
        RETURN are_friends, 
               req_sent IS NOT NULL as has_sent_request,
               req_received IS NOT NULL as has_received_request
        """
        try:
            with self._driver.session() as session:
                result = session.run(query, from_user_id=str(from_user_id), to_user_id=str(to_user_id))
                record = result.single()
                
                if record:
                    if record["are_friends"]:
                        return "friends"
                    elif record["has_sent_request"]:
                        return "pending_sent"
                    elif record["has_received_request"]:
                        return "pending_received"
                
                return "none"
        except Exception as e:
            logger.error(f"Error getting friend request status: {e}")
            return "none"
