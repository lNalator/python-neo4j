from py2neo import Graph, NodeMatcher, Node
from datetime import datetime
from resources.post_dto import CreatePostDto, UpdatePostDto
from database.databaseConnector import graph

class PostsService:
    def __init__(self):
        self.graph   = graph
        self.matcher = NodeMatcher(self.graph)

    def get_all_posts(self):
        nodes = self.matcher.match('Post')
        return [
            {
                'id':         n.identity,
                'title':      n['title'],
                'content':    n['content'],
                'created_at': n['created_at']
            }
            for n in nodes
        ]

    def get_post(self, post_id):
        node = self.matcher.get(post_id)
        if not node or 'Post' not in node.labels:
            return None
        return {
            'id':         node.identity,
            'title':      node['title'],
            'content':    node['content'],
            'created_at': node['created_at']
        }

    def get_posts_by_user(self, user_id):
        q   = (
            'MATCH (u:Utilisateur)-[:CREATED]->(p:Post) '
            'WHERE id(u)=$uid RETURN p'
        )
        res = self.graph.run(q, uid=user_id)
        return [
            {
                'id':      r['p'].identity,
                'title':   r['p']['title'],
                'content': r['p']['content']
            }
            for r in res
        ]

    def create_post(self, user_id, dto: CreatePostDto):
        # 1) build the Post node
        created_at = datetime.utcnow().isoformat()
        post_node  = Node(
            "Post",
            title       = dto.title,
            content     = dto.content,
            created_at  = created_at
        )
        # 2) persist it
        self.graph.create(post_node)

        # 3) link creator → post
        self.graph.run(
            '''
            MATCH (u:Utilisateur),(p:Post)
            WHERE id(u)=$uid AND id(p)=$pid
            MERGE (u)-[:CREATED]->(p)
            ''',
            uid = user_id,
            pid = post_node.identity
        )

        return {'id': post_node.identity}

    def update_post(self, post_id, dto: UpdatePostDto):
        node = self.matcher.get(post_id)
        if not node or 'Post' not in node.labels:
            return {'success': False}
        if dto.title is not None:
            node['title'] = dto.title
        if dto.content is not None:
            node['content'] = dto.content
        self.graph.push(node)
        return {'success': True}

    def delete_post(self, post_id):
        node = self.matcher.get(post_id)
        if not node or 'Post' not in node.labels:
            return {'success': False}
        self.graph.delete(node)
        return {'success': True}

    def like_post(self, post_id, user_id):
        self.graph.run(
            '''
            MATCH (u:Utilisateur),(p:Post)
            WHERE id(u)=$uid AND id(p)=$pid
            MERGE (u)-[:LIKES]->(p)
            ''',
            uid = user_id,
            pid = post_id
        )
        return {'success': True}

    def unlike_post(self, post_id, user_id):
        self.graph.run(
            '''
            MATCH (u:Utilisateur)-[r:LIKES]->(p:Post)
            WHERE id(u)=$uid AND id(p)=$pid
            DELETE r
            ''',
            uid = user_id,
            pid = post_id
        )
        return {'success': True}
