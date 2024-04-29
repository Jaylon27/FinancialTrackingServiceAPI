import json
import jwt
import azure.functions as func

def main(req: func.HttpRequest, account: func.SqlRowList) -> func.HttpResponse:
    # Convert SqlRowList to list of dictionaries
    rows = list(map(lambda r: json.loads(r.to_json()), account))

    # Check for Authorization header
    auth_header = req.headers.get('Authorization')
    if not auth_header:
        # Return error response if Authorization header is missing
        return func.HttpResponse("Authorization header is missing", status_code=400)

    try:
        # Get ID from request parameters
        id = req.params.get('id')

        if not id:
            # Return error response if ID is missing in the request parameters
            return func.HttpResponse("ID is missing in the request parameters", status_code=400)
        
        # Check if the ID exists in the rows
        if any(row.get('id') == id for row in rows):
            # Return error response if the ID exists
            return func.HttpResponse("Failed to delete account.", status_code=500)
        else:
            # Return success response if the ID doesn't exist
            return func.HttpResponse("Account deleted successfully", status_code=200)
        

    except jwt.ExpiredSignatureError:
        # Return error response if token has expired
        return func.HttpResponse("Token has expired", status_code=401)
    except jwt.InvalidTokenError:
        # Return error response if token is invalid
        return func.HttpResponse("Invalid token", status_code=401)
    except Exception as e:
        # Return error response for other exceptions
        return func.HttpResponse(f"Error decoding token: {str(e)}", status_code=500)


