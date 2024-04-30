import boto3
import json

class LLM():
    def __init__(self, region) -> None:
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name = region)

    def generate_message(self, body, model_id):
        response = self.bedrock_runtime.invoke_model(body=body, modelId=model_id)
        response_body = json.loads(response.get("body").read())
        return response_body
