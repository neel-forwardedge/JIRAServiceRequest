import logging

import azure.functions as func
import os 
import base64
import requests
from datetime import datetime

#%% 
print("hi")
#%% 

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('JIRA service request function is processing a request.')

    summary = req.params.get('summary')
    description = req.params.get('description')

    if not summary:
        return func.HttpResponse(
             "Please pass parameters in the query string.",
             status_code=400
        )
    if not description:
        return func.HttpResponse(
            "Please pass parameters in the query string.",
            status_code=400
        )
    auth = str(base64.b64encode(bytes(os.environ["AUTH_KEY"], 'utf-8')))
    headers = {"Authorization": "Basic " + auth[2:len(auth)-1]}
    url = os.environ["JIRA_URL"]
    content = {
        "serviceDeskId": "1",
        "requestTypeId": "10002",
        "requestFieldValues": {
            "summary": summary,
            "description": description
        }
    }
    res = requests.post(url, json = content, headers=headers)
    print(res.text)
    return func.HttpResponse(
        res.text,
        status_code=200
    ) 