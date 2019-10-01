### to run:
```shell
pip install -r requirements.txt
pip install -e ./
```

```shell
cp ./.env.template ./.env
```

```shell
gunicorn -w 1 capytcha_server.app:create_app --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker --reload
```