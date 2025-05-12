from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

class Info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')

    phone = PhoneNumberField()

    BACHELORS = [
        ("administracion", "Administración"),
        ("economia", "Economía"),
        ("gobierno", "Gobierno y Asuntos Públicos"),
        ("biologia", "Biología"),
        ("fisica", "Física"),
        ("geociencias", "Geociencias"),
        ("matematicas", "Matemáticas"),
        ("microbiologia", "Microbiología"),
        ("quimica", "Química"),
        ("medicina", "Medicina"),
        ("arquitectura", "Arquitectura"),
        ("arte", "Arte"),
        ("diseno", "Diseño"),
        ("historia_arte", "Historia del Arte"),
        ("literatura", "Literatura"),
        ("musica", "Música"),
        ("narrativas", "Narrativas Digitales"),
        ("ing_ambiental", "Ingeniería Ambiental"),
        ("ing_biomedica", "Ingeniería Biomédica"),
        ("ing_civil", "Ingeniería Civil"),
        ("ing_electrica", "Ingeniería Eléctrica"),
        ("ing_electronica", "Ingeniería Electrónica"),
        ("ing_industrial", "Ingeniería Industrial"),
        ("ing_mecanica", "Ingeniería Mecánica"),
        ("ing_quimica", "Ingeniería Química"),
        ("ing_alimentos", "Ingeniería de Alimentos"),
        ("ing_sistemas", "Ingeniería de Sistemas y Computación"),
        ("antropologia", "Antropología"),
        ("ciencia_politica", "Ciencia Política"),
        ("derecho", "Derecho"),
        ("estudios_globales", "Estudios Globales"),
        ("filosofia", "Filosofía"),
        ("historia", "Historia"),
        ("lenguas", "Lenguas y Cultura"),
        ("psicologia", "Psicología"),
        ("lic_artes", "Lic. en Artes"),
        ("lic_biologia", "Lic. en Biología"),
        ("lic_infantil", "Lic. en Educación Infantil"),
        ("lic_espanol", "Lic. en Español y Filología"),
        ("lic_filosofia", "Lic. en Filosofía"),
        ("lic_fisica", "Lic. en Física"),
        ("lic_historia", "Lic. en Historia"),
        ("lic_matematicas", "Lic. en Matemáticas"),
        ("lic_quimica", "Lic. en Química"),
        ("estudios_dirigidos", "Estudios Dirigidos"),
    ]
    
    bachelor = models.CharField(default="", max_length=100, choices=BACHELORS)  

    rating = models.FloatField(
        default=5.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )

    user_reviews = models.IntegerField(default=0)

    def add_review(self, rating : float) -> None:
        """
        Adds a review to the user.
        """
        self.rating = (self.rating * self.user_reviews + rating) / (self.user_reviews + 1)
        self.user_reviews += 1
        self.save()

    def __str__(self):
        return f"{self.user.username} Info"
