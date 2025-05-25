from django.db import models

class Propriete(models.Model):
    STATUT_CHOICES = [
        ('disponible', 'Disponible'),
        ('louee', 'Louée'),
        ('vendue', 'Vendue'),
        ('masquee', 'Masquée'),
    ]

    OPTION_CHOICES = [
        ('vente', 'Vente'),
        ('location', 'Location'),
    ]

    TYPE_CHOICES = [
        ('maison', 'Maison'),
        ('appartement', 'Appartement'),
        ('terrain', 'Terrain'),
        # Tu peux ajouter plus de types ici selon ton besoin
    ]

    USAGE_CHOICES = [
        ('residentiel', 'Résidentiel'),
        ('commercial', 'Commercial'),
        # Ou autres usages selon les cas
    ]

    # Attributs de la propriété
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    usage = models.CharField(max_length=30, choices=USAGE_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='masquee')
    localisation = models.CharField(max_length=255)
    superficie = models.FloatField()
    prix = models.DecimalField(max_digits=12, decimal_places=2)
    option = models.CharField(max_length=10, choices=OPTION_CHOICES)
    
    # Date de création/modification
    date_ajout = models.DateTimeField(auto_now_add=True)
    last_date_modification = models.DateTimeField(auto_now=True)

    # Images associées (relation 1-N)
    # On gère ça via un modèle Image séparé (voir ci-dessous)

    def __str__(self):
        return f"{self.type} - {self.localisation} ({self.option})"
