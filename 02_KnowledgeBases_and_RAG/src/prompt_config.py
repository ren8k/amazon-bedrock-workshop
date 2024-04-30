import copy
import yaml
from typing import Any


class PromptConfig():
    def __init__(self, config_path, template_path):
        self.config = self._load_config(config_path)
        self.config_org = copy.deepcopy(self.config)
        self.template = self._load_config(template_path)["template"]
        self.query = self.config.pop("query")
        self.model_id = self.config.pop("modelId")
        self.prompt = ""

    def _load_config(self, config_path):
        with open(config_path, "r") as file:
            return yaml.safe_load(file)

    def format_prompt(self, args):
        self.prompt = self.template.format(**args)

    def format_message(self, args):
        message = self.config["messages"][0]["content"][0]["text"]
        self.config["messages"][0]["content"][0]["text"] = message.format(**args)
