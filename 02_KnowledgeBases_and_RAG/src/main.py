import json
import logging

from botocore.exceptions import ClientError
from llm import LLM
from prompt_config import PromptConfig
from retriever import Retriever

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    kb_id = "7BVHEOMVBK"
    region = "us-west-2"
    config_path = "./config/claude-3_cofig.yaml"
    template_path = "./config/prompt_template.yaml"
    query_path = "./config/query.yaml"

    prompt_conf = PromptConfig(config_path, template_path, query_path)
    retriever = Retriever(kb_id, region)
    llm = LLM(region)

    retrieval_results = retriever.retrieve(prompt_conf.query)
    contexts = retriever.get_contexts(retrieval_results)
    prompt_conf.format_prompt({"contexts": contexts, "query": prompt_conf.query})
    prompt_conf.format_message({"prompt": prompt_conf.prompt})
    body = json.dumps(prompt_conf.config)

    try:
        llm.generate(body, prompt_conf.model_id, prompt_conf.is_streaming)
    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " + format(message))


if __name__ == "__main__":
    main()
