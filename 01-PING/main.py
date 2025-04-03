
## On demande à l'utilisateur une idresse ip a ping
import platform
import subprocess

ip = input("Entrez une adresse ip/url")
#On detecte le system d'exploitation pour adapter la commande
param = "-n" if platform.system().lower() == "windows" else "-c"
# Construire la commande ping
commande = ["ping", param, "1", ip]
print("Ping en cours...")

#On execute la ping
try:
    result = subprocess.run(commande, stdout = subprocess.DEVNULL)
    if result.returncode == 0:
        print("cible est en ligne")
    else:
        print("Aucune réponse")
except Exception as e:
    print(f"Erreur lors du ping : {e}")