# Utiliser une image Python légère
FROM python:3.10-slim

# Définir le dossier de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le reste du code
COPY . .

# Exposer le port 5000 (celui de Flask)
EXPOSE 5000

# Commande de démarrage
CMD ["python", "app.py"]