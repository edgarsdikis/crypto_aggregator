from drf_spectacular.utils import OpenApiExample
from drf_spectacular.generators import SchemaGenerator

class CustomSchemaGenerator(SchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        
        # Process all paths in the schema
        for path_key, path_item in schema['paths'].items():
            # Check for token endpoints
            if '/api/users/token/' in path_key:
                # Process each method (POST, GET, etc.)
                for method_key, operation in path_item.items():
                    # Replace the tags with 'Authentication'
                    operation['tags'] = ['Authentication']
                    
        return schema

# Common error responses
error_response = {
    "type": "object",
    "properties": {
        "error": {"type": "string"}
    }
}

validation_error_response = {
    "type": "object", 
    "properties": {
        "field_name": {
            "type": "array",
            "items": {"type": "string"}
        }
    }
}

# Common success messages
success_message_response = {
    "type": "object",
    "properties": {
        "message": {"type": "string"}
    }
}

# Wallet sync response schema
wallet_sync_response = {
    "type": "object",
    "properties": {
        "wallet": {"type": "object"},
        "token_count": {"type": "integer"}
    }
}

# Supported chains response
supported_chains_response = {
    "type": "object",
    "properties": {
        "supported_chains": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"}
                }
            }
        }
    }
}

# Common examples for testing
wallet_example = OpenApiExample(
    'Sample Wallet',
    value={
        'address': '0x1234567890abcdef1234567890abcdef12345678',
        'chain': 'eth',
        'balance_usd': 1234.56,
        'synced_at': '2025-05-08T14:30:00Z'
    }
)
