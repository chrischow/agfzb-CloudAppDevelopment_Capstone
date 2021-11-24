#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.query import Query
import requests


def main(params):
    
    try:
        client = Cloudant.iam(
            account_name = None,
            url = params["COUCH_URL"],
            api_key=params["IAM_API_KEY"],
            connect=True,
        )
        
    except:
        print("Unable to connect.")
        return {"error": {
            "code": 500,
            "message": "Something went wrong on the server."
        } }
    
    # Open reviews database
    db = client["reviews"]
    if not "dealerId" in params.keys():
        return {
            "error": {
                "code": 404,
                "message": f"dealerId does not exist."
            }
        }
    
    selector = {
        "dealership": { "$eq": int(params["dealerId"]) }
    }
    response = Query(db, selector=selector)
    data = response()['docs']
    
    if len(data) == 0:
        return {
            "error": {
                "code": 404,
                "message": "dealerId does not exist."
            }
        }
    return { 
        "code": 200,
        "data": data
    }

