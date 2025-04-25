from datetime import datetime
from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
from database.databaseConnector import graph

schema = graph.schema

class Post(GraphObject):
    __primarylabel__ = "Post"
    __primarykey__   = "title"

    title      = Property()  # Titre
    content    = Property()  # Contenu
    created_at = Property()  # Date de création

    # Relations
    # l'auteur d'un post (inverse de CREATED)
    author    = RelatedFrom("Utilisateur", "CREATED")
    # liens vers les commentaires
    comments  = RelatedTo("Commentaire", "HAS_COMMENT")
    # qui a aimé ce post
    liked_by  = RelatedFrom("Utilisateur", "LIKES")
