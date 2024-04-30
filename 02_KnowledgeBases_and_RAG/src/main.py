import json
import logging

from llm import LLM
from retriever import Retriever
from prompt_template import PromptConfig
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():
    kb_id = "JWZYVDJFCU"
    region = "us-west-2"
    config_path = "./config/claude_cofig.yaml"
    template_path = "./config/prompt_template.yaml"

    prompt_conf = PromptConfig(config_path, template_path)
    retriever = Retriever(kb_id, region)
    llm = LLM(region)

    retrieval_results = retriever.retrieve(prompt_conf.query)
    contexts = retriever.get_contexts(retrieval_results)
    prompt_conf.format_prompt({"contexts": contexts, "query": prompt_conf.query})
    prompt_conf.format_message({"prompt": prompt_conf.prompt})

    try:
        body = json.dumps(prompt_conf.config)
        response_body = llm.generate_message(body, prompt_conf.model_id)
        print(response_body["content"][0]["text"])
    except ClientError as err:
        message=err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
            format(message))


if __name__ == "__main__":
    main()
