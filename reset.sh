#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

echo "#### Importando variáveis de ambiente..."
source .env

echo "#### Recriandbo banco de dados..."
sudo -u postgres dropdb --if-exists "${DB_NAME}"
sudo -u postgres createdb "${DB_NAME}"

echo "#### Criando usuário, se não existir..."
cat <<EOF | sudo -u postgres psql
DO
\$do\$
BEGIN
   IF NOT EXISTS ( SELECT FROM pg_roles WHERE rolname = '${DB_USER}' ) THEN
      CREATE USER ${DB_USER} WITH SUPERUSER PASSWORD '${DB_PWD}';
   END IF;
END
\$do\$;
EOF

echo "#### Aplicação dos migrations iniciais no banco de dados..."
python manage.py makemigrations
python manage.py migrate

if [ -n "${DJANGO_SUPERUSER_USERNAME}" ]; then
echo "#### Criação do superusuário do Django Admin..."
cat <<EOF | python manage.py shell
from django.contrib.auth.models import User as DjangoAdminUser;
from django.contrib.auth.hashers import make_password; 
DjangoAdminUser.objects.create(
    is_staff=True, 
    is_superuser=True, 
    username='${DJANGO_SUPERUSER_USERNAME}', 
    email='${DJANGO_SUPERUSER_EMAIL}', 
    password=make_password('${DJANGO_SUPERUSER_PASSWORD}')
)
EOF
fi

echo "#### Criação de um usuário no Helios..."
cat <<EOF | python manage.py shell
from helios_auth.models import User as HeliosUser
HeliosUser.objects.create(
    user_type='password', 
    name='Dudu', 
    user_id='vndmtrx@duck.com', 
    info={
        'name':'Dudu', 
        'password':'semsenha'
    }
)
EOF
