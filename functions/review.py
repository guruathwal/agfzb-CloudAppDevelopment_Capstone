#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import json
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = None
service = None

# Initialize Cloudant connection using the provided credentials
def initialize_authenticator_and_service(apikey, url):
    global authenticator, service
    authenticator = IAMAuthenticator(apikey)
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(url)

def list_reviews(dealer_id):
    global authenticator, service
    try:
        # Access the 'reviews' database
        db_name = 'reviews'
        database = service.post_all_docs(db=db_name,include_docs=True).get_result()

        # Initialize the result list
        result = []

        # If dealer_id is provided, filter by dealer_id
        if dealer_id is not None:
            for document in database['rows']:
                if document.get('doc', {}).get('dealership') == int(dealer_id):  # Check if 'doc' exists
                    result.append(document.get('doc'))
        else:
            # If no dealer_id is provided, list all items
            for document in database['rows']:
                result.append(document.get('doc'))

        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Something went wrong on the server: {str(e)}')
        }


def add_review(doc_data):
    global authenticator, service
    try:
        # Access the 'reviews' database
        db_name = 'reviews'
        db_information = service.get_database_information(db=db_name).get_result()

        # get total document count
        doc_count = db_information["doc_count"]

        # Insert the 'id' attribute
        doc_data["id"] = doc_count + 1
        # Insert the new document
        response = service.post_document(db=db_name, document=doc_data).get_result()

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Document added successfully', '_id': response['id']})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Something went wrong on the server: {str(e)}')
        }

def main(param_dict):
    try:
        api_key = param_dict['IAM_API_KEY']
        api_url = param_dict['COUCH_URL']

        initialize_authenticator_and_service(api_key, api_url)

        method = param_dict['__ow_method']

        if method == 'get':
            if 'dealerId' not in param_dict:
                return list_reviews(None)
            else:
                result = list_reviews(param_dict['dealerId'])

                # Check if dealer_id exists
                if result['statusCode'] == 200 and len(json.loads(result['body'])) == 0:
                    return {
                        'statusCode': 404,
                        'body': json.dumps('dealerId does not exist')
                    }
                else:
                    return result
        elif  method == "post":
            # Extract data from the request body
            request_doc = param_dict["review"]
            result = add_review(request_doc)
            return result
        else:
            return {
                'statusCode': 405,
                'body': json.dumps('Method not allowed')
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Something went wrong on the server: {str(e)}')
        }

