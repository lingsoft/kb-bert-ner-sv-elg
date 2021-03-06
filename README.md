# ELG API for BERT base fine-tuned for Swedish NER

This git repository contains [ELG compatible](https://european-language-grid.readthedocs.io/en/stable/all/A3_API/LTInternalAPI.html) Flask based REST API for the BERT base fine-tuned for Swedish NER

[KB Swedish bert models](https://github.com/Kungbib/swedish-bert-models) contains a list of BERT and ALBERT base fine-tuned models for NLP tasks, of which the model name **"bert-base-swedish-cased-ner"** is fine-tuned on the [SUC 3.0](https://spraakbanken.gu.se/en/resources/suc3) datatset for NER task and this ELG API was developed based on it.
Original author: The National Library of Sweden / KBLab, published under CC0 license.


This ELG API was developed in EU's CEF project: [Microservices at your service](https://www.lingsoft.fi/en/microservices-at-your-service-bridging-gap-between-nlp-research-and-industry)

## Local development

Setup virtualenv, dependencies
```
python3 -m venv kb-ner-elg-venv
source kb-ner-elg-venv/bin/activate
python3 -m pip install -r requirements.txt
```

The model can be downloaded to local (optional), because the transformers library downloads and caches the model anyway.
```
python3 load_model.py
```

Run the development mode flask app
```
FLASK_ENV=development flask run --host 0.0.0.0 --port 8000
```

## Building the docker image

```
docker build -t kb-ner-elg .
```


Or pull directly ready-made image `docker pull lingsoft/kb-bert-ner-sv:tagname`.

## Deploying the service

```
docker run -d -p <port>:8000 --init --memory="2g" --restart always kb-ner-elg
```

## REST API

### Call pattern

#### URL

```
http://<host>:<port>/process
```

Replace `<host>` and `<port>` with the host name and port where the 
service is running.

#### HEADERS

```
Content-type : application/json
```

#### BODY

For text request
```
{
  "type":"text",
  "content": text to be analyzed for NER task
}
```
#### RESPONSE

```
{
  "response":{
    "type":"annotations",
    "annotations":{
      "<NER notation>":[ // list of tokens that were recognized
        {
          "start":number,
          "end":number,
          "features":{ "word": str, "score": float }
        },
      ],
    }
  }
}
```

### Response structure

- `start` and `end` (int)
  - the indices of the token in the send request
- `word` (str)
  - word/phrase that is recognized with entities
- `score` (float)
  - confidence score of the entity, log likelihood probability.

### Example call

```
curl -d '{"type":"text","content":"Engelbert tar Volvon till Tele2 Arena f??r att titta p?? Djurg??rden IF som spelar fotboll i VM klockan tv?? p?? kv??llen."}' -H "Content-Type: application/json" -X POST http://localhost:8000/process
```

### Response should be

```json
{
    "response": {
        "type": "annotations",
        "annotations": {
            "PER": [
                {
                    "start": 0,
                    "end": 9,
                    "features": {
                        "word": "Engelbert",
                        "score": "1.000"
                    }
                }
            ],
            "LOC": [
                {
                    "start": 26,
                    "end": 37,
                    "features": {
                        "word": "Tele2 Arena",
                        "score": "0.998"
                    }
                }
            ],
            "ORG": [
                {
                    "start": 55,
                    "end": 68,
                    "features": {
                        "word": "Djurg??rden IF",
                        "score": "0.998"
                    }
                }
            ],
            "EVN": [
                {
                    "start": 90,
                    "end": 92,
                    "features": {
                        "word": "VM",
                        "score": "0.999"
                    }
                }
            ],
            "TME": [
                {
                    "start": 93,
                    "end": 115,
                    "features": {
                        "word": "klockan tv?? p?? kv??llen",
                        "score": "0.999"
                    }
                }
            ]
        }
    }
}
```

