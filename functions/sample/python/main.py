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
import requests


def main(dict):
    databaseName = "dealerships"
    secret = {
        "COUCH_URL":"https://c8eb5a3f-130c-4cd1-b168-14aa6ad3da10-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY":"Z90P54UqWQ8qulUEc0NOkDCWzi_XJrQYEvDQJqCUwOAD",
        "COUCH_USERNAME":"c8eb5a3f-130c-4cd1-b168-14aa6ad3da10-bluemix",
    }
    try:
        client = Cloudant.iam(
            account_name=secret["COUCH_USERNAME"],
            api_key=secret["IAM_API_KEY"],
            
            connect=True,
        )
        print("Databases: {0}".format(client.all_dbs()))
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}
