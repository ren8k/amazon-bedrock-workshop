import json
import logging

from llm import LLM
from retriever import Retriever
from prompt_template import PromptTemplate
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():
    kb_id = "JWZYVDJFCU"
    region = "us-west-2"
    path = "./config/claude_cofig.yaml"
    prompt_template = PromptTemplate(path)


    retriever = Retriever(kb_id, region)
    llm = LLM(region)

    retrieval_results = retriever.retrieve(prompt_template.query)
    contexts = retriever.get_contexts(retrieval_results)
    prompt = prompt_template.format_prompt({"contexts": contexts, "query": prompt_template.query})
    # print(prompt)
    prompt_template.format_message(prompt)


    try:
        body = json.dumps(prompt_template.config)
        response_body = llm.generate_message(body, prompt_template.model_id)
        print(response_body["content"][0]["text"])
    except ClientError as err:
        message=err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
            format(message))


if __name__ == "__main__":
    main()
