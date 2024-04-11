import os
from span_marker import SpanMarkerModel

from tqdm import tqdm

from dotenv import load_dotenv

from utils import utils


load_dotenv()

PROPS_FOLDER = os.getenv("PROPS_FOLDER")
NER_FOLDER = os.getenv("NER_FOLDER")


seen_props = os.listdir(NER_FOLDER)

model = SpanMarkerModel.from_pretrained(
    "lxyuan/span-marker-bert-base-multilingual-uncased-multinerd",
    language="pt",
)
model.try_cuda()

for prop in tqdm(os.listdir(PROPS_FOLDER)):
    if prop in seen_props:
        continue

    prop_data = utils.open_json(PROPS_FOLDER, prop)

    ementa = prop_data[0].get("ementa")

    if not ementa:
        continue

    ner = model.predict(ementa)

    utils.save_json(NER_FOLDER, prop.split('.')[0], ner)
