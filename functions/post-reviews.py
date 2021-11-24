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
from cloudant.document import Document
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
    
    # Create document
    try:
        with Document(db) as doc:
            doc['name'] = params['name']
            doc['dealership'] = params['dealership']
            doc['review'] = params['review']
            doc['car_make'] = params['car_make']
            doc['car_model'] = params['car_model']
            doc['car_year'] = params['car_year']
    except:
        return {"error": {
            "code": 500,
            "message": "Something went wrong on the server."
        } }
    return { 
        "code": 200,
        "message": "Post created successfully.",
        "data": eval(doc.json())
    }