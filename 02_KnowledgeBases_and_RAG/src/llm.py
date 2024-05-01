import boto3
import json


class LLM():
    def __init__(self, region) -> None:
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name = region)

    def generate_message(self, body, model_id):
        response = self.bedrock_runtime.invoke_model(body=body, modelId=model_id)
        response_body = json.loads(response.get("body").read())
        print(response_body["content"][0]["text"])


    def generate_stream_message(self, body, model_id):
        response = self.bedrock_runtime.invoke_model_with_response_stream(
            body=body, modelId=model_id)

        for event in response.get("body"):
            chunk = json.loads(event["chunk"]["bytes"])

            if chunk['type'] == 'message_delta':
                print("\n")
                # print(f"\nStop reason: {chunk['delta']['stop_reason']}")
                # print(f"Stop sequence: {chunk['delta']['stop_sequence']}")
                # print(f"Output tokens: {chunk['usage']['output_tokens']}")

            if chunk['type'] == 'content_block_delta':
                if chunk['delta']['type'] == 'text_delta':
                    print(chunk['delta']['text'], end="")

    def generate(self, body, model_id, is_streaming=False):
        if is_streaming:
            return self.generate_stream_message(body, model_id)
        else:
            return self.generate_message(body, model_id)
