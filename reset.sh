#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.
sudo -u postgres dropdb --if-exists helios
sudo -u postgres createdb helios
sudo -u postgres psql -c "CREATE USER helios WITH SUPERUSER PASSWORD 'heliosteste';"

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

cat <<EOF | python manage.py shell
from helios_auth.models import User
User.objects.create(
    user_type='password', 
    name='Dudu', 
    user_id='vndmtrx@duck.com', 
    info={
        'name':'Dudu', 
        'password':'semsenha'
    }
)
EOF
