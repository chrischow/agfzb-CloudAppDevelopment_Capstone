/**
 * Get all dealerships
 */

const Cloudant = require('@cloudant/cloudant');


async function main(params) {
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });
    
    // Find documents where state = state
    let selector = {}
    if (params.state) {
        selector = { st: { $eq: params.state } };
    }
    
    const query = {
      "selector": selector,
      "fields": [ "id", "city", "state", "st", "address", "zip", "lat", "long" ]
    };
    
    try {
        dealerships = cloudant.use('dealerships');
        let dealershipList = await dealerships.find(query)
        if (dealershipList.docs.length === 0) {
            return { "error": {
                "code": 404,
                "message": "The state does not exist."
            } }
        }
        return { "dealerships": dealershipList.docs };
    } catch (error) {
        return { "error": {
            "code": 500,
            "message": "Something went wrong on the server."
        } };
    }
}