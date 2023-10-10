// Importing the cloudant package
const Cloudant = require('@ibm-cloud/cloudant');

// Initializing the Cloudant client with provided credentials
const cloudant = Cloudant({
  url: process.env.COUCH_URL,
  plugins: { iamauth: { iamApiKey: process.env.IAM_API_KEY } }
});

// Accessing the 'dealerships' database
const db = cloudant.db.use('dealerships');

// IBM Cloud Function handler function
async function main(params) {
  try {
    // Extracting query parameters from the input 'params' object
    const stateFilter = params.state || null;
    const dealerIdFilter = params.dealerId || null;

    // Fetching a list of documents from the database
    const data = await db.list({ include_docs: true });

    // Handling the case where the database is empty
    if (data.rows.length === 0) {
      return {
        statusCode: 404,
        body: { message: 'The database is empty' }
      };
    }

    // Filtering and mapping the data based on the query parameters
    const dealerships = data.rows
      .filter(row => {
        if (stateFilter && dealerIdFilter) {
          return row.doc.state === stateFilter && row.doc.id === parseInt(dealerIdFilter);
        } else if (stateFilter) {
          return row.doc.state === stateFilter;
        } else if (dealerIdFilter) {
          return row.doc.id === parseInt(dealerIdFilter);
        } else {
          return true;
        }
      })
      .map(row => {
        const { id, city, state, st, address, zip, lat, long, short_name, full_name } = row.doc;
        return { id, city, state, st, address, zip, lat, long, short_name, full_name };
      });

    // Returning a successful response with the filtered and mapped data
    return {
      statusCode: 200,
      body: dealerships
    };
  } catch (error) {
    // Handling errors and returning a 500 status code with an error message
    return {
      statusCode: 500,
      body: { message: 'Something went wrong on the server', error: error.message }
    };
  }
}

// Exporting the main function for use in IBM Cloud Function
module.exports = { main };
