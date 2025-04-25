from datetime import datetime
from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
from database.databaseConnector import graph

schema = graph.schema

class Commentaire(GraphObject):
    __primarylabel__ = "Commentaire"
    __primarykey__   = None   # Si vous voulez un id, ajoutez une propriété uuid

    content    = Property()  # Contenu
    created_at = Property()  # Date de création

    # Relations
    # l'auteur du commentaire
    author   = RelatedFrom("Utilisateur", "CREATED")
    # le post parent ( chaque commentaire doit être rattaché à un Post )
    post     = RelatedFrom("Post", "HAS_COMMENT")
    # qui a aimé ce commentaire
    liked_by = RelatedFrom("Utilisateur", "LIKES")
