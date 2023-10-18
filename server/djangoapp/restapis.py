import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))

    response = None  # Define response outside the try block

    try:
        api_key = kwargs.get("api_key")
        params = {
            "text": kwargs.get("text", ""),  # Provide a default empty string if "text" is not in kwargs
            "version": kwargs.get("version", ""),
            "features": kwargs.get("features", []),
            "return_analyzed_text": kwargs.get("return_analyzed_text", False)
        }

        if api_key:
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                     auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)

        response.raise_for_status()  # Check for HTTP error

        json_data = response.json()  # Use response.json() to parse JSON directly

        return json_data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    finally:
        if response:
            response.close()


# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    response = requests.post(url, json=json_payload, **kwargs)
    return response


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)

    if json_result:
        # Iterate over each dealer object
        for dealer_doc in json_result:
            # Create a CarDealer object with values in `dealer_doc`
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                state=dealer_doc['state'],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)

    return results

def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)

    if json_result:
        # Iterate over each dealer object
        for dealer_doc in json_result:
            # Create a CarDealer object with values in `dealer_doc`
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                state=dealer_doc["state"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)

    print(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf (url, dealer_id):
# - Call get_request() with specified arguments
# - Parse JSON results into a Review object list
    results = []
    # params = {
    #     "dealerId": dealerId
    # }
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealer_id)

    if json_result:
        # Iterate over each Review object
        for review_doc in json_result:
            if review_doc["purchase"] is None or review_doc["purchase"] is False:
                purchase = False
            else:
                purchase = True

            # Create a Review object with values in `review_doc`
            # review_obj = DealerReview(
            #     dealership = review_doc["dealership"],
            #     name = review_doc["name"],
            #     purchase = purchase,
            #     review = review_doc["review"],
            #     id = review_doc["id"]
            # )
            review_obj = DealerReview(
                dealership=review_doc["dealership"],
                name=review_doc["name"],
                purchase=purchase,
                review=review_doc["review"],
                id=review_doc["id"]
            )
            if purchase:
                review_obj.purchase_date = review_doc["purchase_date"]
                review_obj.car_make = review_doc["car_make"]
                review_obj.car_model = review_doc["car_model"]
                review_obj.car_year = review_doc["car_year"]

            review_obj.sentiment = analyze_review_sentiments(review_doc["review"])
            print("sentiment:" + review_obj.sentiment)


            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):

    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/50c378ef-c9cf-44d1-985e-279d8c728372"
    api_key = ""
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(language='en',text=text,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result()

    # print("Watson NLU Response:" + response)

    if 'sentiment' in response and 'document' in response['sentiment']:
        sentiment_label = response['sentiment']['document']['label']
        return sentiment_label

    return None
