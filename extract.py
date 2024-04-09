import os
import datetime

from tqdm import tqdm

from dotenv import load_dotenv

from utils import api, endpoints, utils


load_dotenv()

DATE_FORMAT = os.getenv('DATE_FORMAT')
PROPS_FOLDER = os.getenv('PROPS_FOLDER')
PROPS_AUTHORS_FOLDER = os.getenv('PROPS_AUTHORS_FOLDER')
PROPS_TOPICS_FOLDER = os.getenv('PROPS_TOPICS_FOLDER')
TIMEDELTA = os.getenv('TIMEDELTA')


date_init = datetime.date(1988, 1, 1)
date_end = datetime.date(1988, 1, 31)

days = (datetime.date.today() - date_init).days

seen_props = os.listdir(PROPS_FOLDER)


pbar = tqdm(range(0 , days), desc='Dias', leave=True)
pbar2 = tqdm(range(0, ), desc='Baixando proposições', leave=True, position=1)

while True:
    params = {
        "dataApresentacaoInicio": date_init.strftime(DATE_FORMAT),
        "dataApresentacaoFim": date_end.strftime(DATE_FORMAT),
    }

    url = api.construct_url(api.HOST, endpoints.PROPOSICAO, params)

    props = api.request(url)
    
    pbar2.total = len(props)

    for prop in props:
        id_prop = str(prop.get('id'))
        uri = prop.get('uri')

        if id_prop + ".json" in seen_props:
            continue

        prop_det = api.request(uri)
        authors = api.request(uri + "/autores")
        topics = api.request(uri + "/temas")

        utils.save_json(PROPS_FOLDER, id_prop, prop_det)
        utils.save_json(PROPS_AUTHORS_FOLDER, id_prop, authors)
        utils.save_json(PROPS_TOPICS_FOLDER, id_prop, topics)

        pbar2.update(1)
    pbar2.reset()

    date_init = date_end + datetime.timedelta(1)
    date_end = date_init + datetime.timedelta(TIMEDELTA)

    pbar.update(TIMEDELTA)

    if date_init >= datetime.date.today():
        break