pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py loaddata pokemon/fixtures/pokemon.json
python3 manage.py loaddata pokemon/fixtures/type-matchups.json
python3 manage.py createcachetable
