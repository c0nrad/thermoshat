import requests
import datetime

secret = open('SECRET', mode='r').read().strip()
git_version = open('GIT_VERSION', mode='r').read().strip()


def save_metric(key, value):
    db = "thermoshat"
    collection = "metrics"
    u = "https://webhooks.mongodb-realm.com/api/client/v2.0/app/thermoshat-lhrjy/service/ingest/incoming_webhook/ingest?secret=%s&db=%s&collection=%s" % (
        secret, db, collection)

    body = {
        'version': git_version,
        'ts': datetime.datetime.now().isoformat(),
        'name': key
    }
    body[key] = value

    r = requests.post(u, json=body)
    if r.status_code != 200:
        print(r.status_code, r.reason, r.text)
