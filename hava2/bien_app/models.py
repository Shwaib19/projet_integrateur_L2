from django.db import models

# Pour gérer les choix possibles dans certains champs

TYPE_CHOICES = [
        ("APPART", 'Appartement'),
        ("VILLA", 'Villa'),
        ("MAISON", 'Terrain'),
        ("LOCAL", 'Local commercial'),
        ("PARKING", 'Parking'),
    ]

STATUT_CHOICES = [
    ('disponible', 'Disponible'),
    ('louee', 'Louée'),
    ('vendue', 'Vendue'),
    ('masque', 'Masqué'),
]

OPTION_CHOICES = [
    ('vente', 'Vente'),
    ('location', 'Location'),
]

class Propriete(models.Model):

    type = models.CharField(max_length=30, choices=TYPE_CHOICES)  # Ex: Appartement, Villa...
    usage = models.CharField(max_length=100)  # Ex: Habitation, Commercial...
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='disponible')
    localisation = models.CharField(max_length=255)
    superficie = models.DecimalField(max_digits=10, decimal_places=2)  # en m²
    prix = models.DecimalField(max_digits=15, decimal_places=2)  # en FCFA ou autre
    option = models.CharField(max_length=10, choices=OPTION_CHOICES)
    bailleur = models.ForeignKey(
        'auth_app.CustomUser',  # entre guillemets = pas d'import
        on_delete=models.SET_NULL,
        limit_choices_to={'user_type': 'BAILLEUR'},
        null=True, blank=True,
        related_name='proprietes'
    )



    
    def __str__(self):
        return f"{self.type} à {self.localisation} - {self.option}"

class Image(models.Model):
    propriete = models.ForeignKey(Propriete, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='proprietes/')

    def __str__(self):
        return f"Image de {self.propriete}"
