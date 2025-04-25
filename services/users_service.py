from py2neo import Graph, NodeMatcher, Node
from datetime import datetime
from resources.user_dto import CreateUserDto, UpdateUserDto
from database.databaseConnector import graph

class UsersService:
    def __init__(self):
        self.graph = graph
        self.matcher = NodeMatcher(self.graph)

    def get_all_users(self):
        nodes = self.matcher.match('Utilisateur')
        return [
            {'id': n.identity, 'name': n['name'], 'email': n['email'], 'created_at': n['created_at']}
            for n in nodes
        ]

    def create_user(self, dto: CreateUserDto):
        # 1) build a Node object
        created_at = datetime.utcnow().isoformat()
        user_node  = Node(
            "Utilisateur",
            name       = dto.name,
            email      = dto.email,
            created_at = created_at
        )
        # 2) persist it
        self.graph.create(user_node)
        # 3) return the new identity
        return {
            "id":          user_node.identity,
            "name":        user_node["name"],
            "email":       user_node["email"],
            "created_at":  user_node["created_at"]
        }

    def get_user(self, user_id):
        node = self.matcher.get(user_id)
        if not node or 'Utilisateur' not in node.labels:
            return None
        return {'id': node.identity, 'name': node['name'], 'email': node['email'], 'created_at': node['created_at']}

    def update_user(self, user_id, dto: UpdateUserDto):
        node = self.matcher.get(user_id)
        if not node or 'Utilisateur' not in node.labels:
            return None
        if dto.name is not None:
            node['name'] = dto.name
        if dto.email is not None:
            node['email'] = dto.email
        self.graph.push(node)
        return {'id': node.identity, 'email': node['email']}

    def delete_user(self, user_id):
        node = self.matcher.get(user_id)
        if not node or 'Utilisateur' not in node.labels:
            return False
        self.graph.delete(node)
        return True

    def get_friends(self, user_id):
        query = '''
        MATCH (u:Utilisateur)-[:FRIENDS_WITH]-(f:Utilisateur)
        WHERE id(u)=$id RETURN f
        '''
        res = self.graph.run(query, id=user_id)
        return [
            {'id': r['f'].identity, 'name': r['f']['name'], 'email': r['f']['email']}
            for r in res
        ]

    def add_friend(self, user_id, friend_id):
        query = '''
        MATCH (u:Utilisateur), (f:Utilisateur)
        WHERE id(u)=$uid AND id(f)=$fid
        MERGE (u)-[:FRIENDS_WITH]->(f)
        '''
        self.graph.run(query, uid=user_id, fid=friend_id)
        return {'success': True}

    def remove_friend(self, user_id, friend_id):
        query = '''
        MATCH (u:Utilisateur)-[r:FRIENDS_WITH]-(f:Utilisateur)
        WHERE id(u)=$uid AND id(f)=$fid
        DELETE r
        '''
        self.graph.run(query, uid=user_id, fid=friend_id)
        return {'success': True}

    def are_friends(self, user_id, friend_id):
        query = '''
        MATCH (u:Utilisateur)-[:FRIENDS_WITH]-(f:Utilisateur)
        WHERE id(u)=$uid AND id(f)=$fid
        RETURN count(*)>0 AS areFriends
        '''
        val = self.graph.run(query, uid=user_id, fid=friend_id).evaluate()
        return {'areFriends': bool(val)}

    def mutual_friends(self, user_id, other_id):
        query = '''
        MATCH (u:Utilisateur)-[:FRIENDS_WITH]-(m:Utilisateur)-[:FRIENDS_WITH]-(o:Utilisateur)
        WHERE id(u)=$uid AND id(o)=$oid
        RETURN DISTINCT m
        '''
        res = self.graph.run(query, uid=user_id, oid=other_id)
        return [
            {'id': r['m'].identity, 'name': r['m']['name'], 'email': r['m']['email']}
            for r in res
        ]