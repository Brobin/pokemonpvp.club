# pokemonpvp.club

Leaderboard and Resource site for the Pokemon Go PvP Discord server.

Running:
* install python3: https://realpython.com/installing-python/
* install git: https://git-scm.com/downloads
* clone this repo: git clone https://github.com/efenderbosch/pokemonpvp.club.git
* install pip3: ???
* pip3 install -r requirements.txt
* python3 manage.py migrate
* python3 manage.py loaddata pokemon/fixtures/pokemon.json
* python3 manage.py loaddata pokemon/fixtures/type-matchups.json
* python3 manage.py createcachetable
* run python3 manage.py runserver
* cd base/assets
* access at http://127.0.0.1:8000/pvp/iv

If you want the site to look nice:
* npm install -g bower (might need sudo?)
* npm install -g sass (might need sudo?)
* cd base/assets
* bower install
* cd ../..
* ln -s base/assets/bower_components static
* cd base/assets/css
* sass site.scss site.css
