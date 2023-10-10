import os
import json
from cloudant.client import Cloudant

api_user = os.environ['COUCH_USERNAME']
api_password = os.environ['IAM_API_PASSWORD']
api_url = os.environ['COUCH_URL']

def list_reviews(dealer_id=None):
    # Initialize Cloudant connection using the provided credentials
    client = Cloudant(api_user, api_password, url=api_url)
    client.connect()

    # Access the 'reviews' database
    database = client['reviews']

    # Initialize the result list
    result = []

    # If dealer_id is provided, filter by 'dealership'
    if dealer_id is not None:
        for document in database:
            if document.get('dealership') == int(dealer_id):
                result.append(document)
    else:
        # If no dealer_id is provided, list all items
        for document in database:
            result.append(document)

    # Disconnect from Cloudant
    client.disconnect()

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }

def add_review(data):
    try:
        # Initialize Cloudant connection using the provided credentials
        client = Cloudant(api_user, api_password, url=api_url)
        client.connect()

        # Access the 'reviews' database
        database = client['reviews']

        # Insert the new document
        doc = database.create_document(data['review'])

        # Disconnect from Cloudant
        client.disconnect()

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Document added successfully', '_id': doc['_id']})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Something went wrong on the server: {str(e)}')
        }

def main(arg):
    try:
        if arg.get('httpMethod') == "GET":
            if arg.get('queryStringParameters') == None:
                return list_reviews()
            else:
                query_parameters = arg.get('queryStringParameters')
                if query_parameters.get('dealerId') == None:
                    return list_reviews()
                else:
                    dealer_id = query_parameters.get('dealerId')
                    result = list_reviews(dealer_id)

                    if result['statusCode'] == 200 and len(json.loads(result['body'])) == 0:
                        return {
                            'statusCode': 404,
                            'body': json.dumps('dealerId does not exist')
                        }
                    else:
                        return result
        elif arg.get('httpMethod') == "POST":
            request_body = json.loads(arg.get('body'))
            result = add_review(request_body)
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
