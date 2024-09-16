from jsonschema import Draft7Validator

def generate_dynamic_schema(extracted_data):
    schema = {
        "type": "object",
        "properties": {
            "description": {"type": "string"},
            "metadata": {
                "type": "object",
                "properties": {}
            },
            "extracted_features": {
                "type": "array",
                "items": {"type": "object", "properties": {}}
            },
        }
    }
    
    if "metadata" in extracted_data:
        schema["properties"]["metadata"]["properties"]["authors"] = {"type": "array", "items": {"type": "string"}}
        schema["properties"]["metadata"]["properties"]["publication_date"] = {"type": "string"}
        schema["properties"]["metadata"]["properties"]["journal"] = {"type": "string"}
    
    for feature in extracted_data.get("extracted_features", []):
        if "description" in feature:
            schema["properties"]["extracted_features"]["items"]["properties"]["description"] = {"type": "string"}
        if "value" in feature:
            schema["properties"]["extracted_features"]["items"]["properties"]["value"] = {"type": "string"}
    
    return schema

def validate_json_output(json_output):
    schema = generate_dynamic_schema(json_output)
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(json_output), key=lambda e: e.path)
    
    if errors:
        for error in errors:
            print(f"Validation error: {error.message}")
        return False
    return True
