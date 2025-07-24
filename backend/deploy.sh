#!/bin/bash

echo "🔁 Pulling latest code from Git..."
git pull

echo "📦 Activating virtual environment..."
source env/bin/activate

echo "📦 Installing dependencies..."
pip install --break-system-packages -r requirements.txt

echo "🛠️ Running migrations..."
python manage.py migrate

echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Restarting Gunicorn..."
sudo systemctl restart jetlux_gunicorn

echo "✅ Deployment complete!"
