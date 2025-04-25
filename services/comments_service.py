from py2neo import Graph, NodeMatcher, Node
from datetime import datetime
from resources.comment_dto import CreateCommentDto, UpdateCommentDto
from database.databaseConnector import graph

class CommentsService:
    def __init__(self):
        self.graph   = graph
        self.matcher = NodeMatcher(self.graph)

    def get_post_comments(self, post_id):
        q   = (
            'MATCH (p:Post)-[:HAS_COMMENT]->(c:Commentaire) '
            'WHERE id(p)=$pid RETURN c'
        )
        res = self.graph.run(q, pid=post_id)
        return [
            {
                'id':           r['c'].identity,
                'content':      r['c']['content'],
                'created_at':   r['c']['created_at']
            }
            for r in res
        ]

    def add_comment(self, post_id, dto: CreateCommentDto):
        # 1) Build and persist the new comment node
        created_at = datetime.utcnow().isoformat()
        comment_node = Node(
            "Commentaire",
            content     = dto.content,
            created_at  = created_at
        )
        self.graph.create(comment_node)

        # 2) Link it to user and post
        self.graph.run(
            '''
            MATCH (u:Utilisateur),(p:Post),(c:Commentaire)
            WHERE id(u)=$uid AND id(p)=$pid AND id(c)=$cid
            MERGE (u)-[:CREATED]->(c)
            MERGE (p)-[:HAS_COMMENT]->(c)
            ''',
            uid = dto.user_id,
            pid = post_id,
            cid = comment_node.identity
        )

        return {'id': comment_node.identity}

    def delete_comment(self, post_id, comment_id):
        q = (
            'MATCH (p:Post)-[hc:HAS_COMMENT]->(c:Commentaire) '
            'WHERE id(p)=$pid AND id(c)=$cid DELETE hc, c'
        )
        self.graph.run(q, pid=post_id, cid=comment_id)
        return {'success': True}

    def get_all_comments(self):
        nodes = self.matcher.match('Commentaire')
        return [
            {
                'id':         n.identity,
                'content':    n['content'],
                'created_at': n['created_at']
            }
            for n in nodes
        ]

    def get_comment(self, comment_id):
        node = self.matcher.get(comment_id)
        if not node or 'Commentaire' not in node.labels:
            return {}
        return {
            'id':         node.identity,
            'content':    node['content'],
            'created_at': node['created_at']
        }

    def update_comment(self, comment_id, dto: UpdateCommentDto):
        node = self.matcher.get(comment_id)
        if not node or 'Commentaire' not in node.labels:
            return {'success': False}
        if dto.content is not None:
            node['content'] = dto.content
        self.graph.push(node)
        return {'success': True}

    def comment_delete_only(self, comment_id):
        node = self.matcher.get(comment_id)
        if not node or 'Commentaire' not in node.labels:
            return {'success': False}
        self.graph.delete(node)
        return {'success': True}

    def like_comment(self, comment_id, user_id):
        self.graph.run(
            '''
            MATCH (u:Utilisateur),(c:Commentaire)
            WHERE id(u)=$uid AND id(c)=$cid
            MERGE (u)-[:LIKES]->(c)
            ''',
            uid = user_id,
            cid = comment_id
        )
        return {'success': True}

    def unlike_comment(self, comment_id, user_id):
        self.graph.run(
            '''
            MATCH (u:Utilisateur)-[r:LIKES]->(c:Commentaire)
            WHERE id(u)=$uid AND id(c)=$cid
            DELETE r
            ''',
            uid = user_id,
            cid = comment_id
        )
        return {'success': True}
