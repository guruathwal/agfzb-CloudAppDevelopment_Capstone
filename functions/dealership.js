/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {

    const authenticator = new IamAuthenticator({apikey: params.IAM_API_KEY});
    const service = new CloudantV1({ authenticator });
    service.setServiceUrl(params.COUCH_URL);

    const state = params.state;

    try {
        const inputDocuments = await service.postAllDocs({
            db: 'dealerships',
            includeDocs: true
        });

        const rows = inputDocuments.result.rows;

        if (rows.length === 0){
            return {statusCode: 404, body: "The database is empty"};
        }

        const outputArray = rows.map(({ doc }) => {
            if (state === undefined || doc.state === state){
                return {
                    id: doc.id,
                    city: doc.city,
                    state: doc.state,
                    st: doc.st,
                    address: doc.address,
                    zip: doc.zip,
                    lat: doc.lat,
                    long: doc.long
                };
            }
            return null; // Filter out unwanted items
        }).filter(item => item !== null);

        if(outputArray.length === 0){
            return {statusCode: 404, body: "The state does not exist"};
        }

        return {statusCode: 200, body: outputArray };
    } catch (error) {
        return {statusCode: 500, body: "Something went wrong on the server"};
    }
}

module.exports = { main };
