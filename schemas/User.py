from datetime import datetime
from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
from database.databaseConnector import graph

graph.run(
    "CREATE CONSTRAINT IF NOT EXISTS "
    "FOR (u:Utilisateur) "
    "REQUIRE u.email IS UNIQUE"
)
graph.run(
    "CREATE INDEX IF NOT EXISTS "
    "FOR (u:Utilisateur) "
    "ON (u.created_at)"
)
graph.run(
    "CREATE INDEX IF NOT EXISTS "
    "FOR (p:Post) "
    "ON (p.title)"
)
graph.run(
    "CREATE INDEX IF NOT EXISTS "
    "FOR (p:Post) "
    "ON (p.created_at)"
)
graph.run(
    "CREATE INDEX IF NOT EXISTS "
    "FOR (c:Commentaire) "
    "ON (c.created_at)"
)

class Utilisateur(GraphObject):
    __primarylabel__ = "Utilisateur"
    __primarykey__   = "email"

    name       = Property()    # Nom
    email      = Property()    # Email (clé primaire)
    created_at = Property()    # Date de création

    # Relations
    # un user a créé des posts et des commentaires
    created_posts    = RelatedTo("Post",        "CREATED")
    created_comments = RelatedTo("Commentaire", "CREATED")

    # amitiés avec d'autres utilisateurs
    friends = RelatedTo("Utilisateur", "FRIENDS_WITH")

    # likes sur posts et commentaires
    likes_posts    = RelatedTo("Post",        "LIKES")
    likes_comments = RelatedTo("Commentaire", "LIKES")
    