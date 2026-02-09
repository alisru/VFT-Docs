import json
import jsonschema

schema_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\7x7x7_kanon_schema.json"
template_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\7x7x7_kanon_template.json"

with open(schema_path, "r") as f:
    schema = json.load(f)

with open(template_path, "r") as f:
    template = json.load(f)

try:
    jsonschema.validate(instance=template, schema=schema)
    print("Validation successful: Template conforms to Schema.")
except jsonschema.exceptions.ValidationError as e:
    print(f"Validation failed: {e}")
