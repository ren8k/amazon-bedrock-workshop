import yaml
from typing import Any


class PromptTemplate():
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        self.template = self.config.pop("template")
        self.query = self.config.pop("query")
        self.model_id = self.config.pop("modelId")

    def _load_config(self, config_path):
        with open(config_path, "r") as file:
            return yaml.safe_load(file)

    def format_prompt(self, args):
        return self.template.format(**args)

    def format_message(self, prompt):
        # print(self.config["messages"][0]["content"][0]["text"])
        self.config["messages"][0]["content"][0]["text"] = prompt
        print(self.config["messages"][0]["content"][0]["text"])


if __name__ == "__main__":
    path = "/home/renya/Develop/aws/amazon-bedrock-workshop/02_KnowledgeBases_and_RAG/src/config/claude_cofig.yaml"
    prompt = PromptTemplate()
    prompt.load_config(path)
    prompt.set_template()
    print(prompt)
