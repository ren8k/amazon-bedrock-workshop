import copy
from typing import Any

import yaml


class PromptConfig:
    def __init__(self, config_path, template_path, query_path):
        self.config = self._load_config(config_path)
        self.config_org = copy.deepcopy(self.config)
        self.template = self._load_config(template_path)["template"]
        self.query = self._load_config(query_path)["query"]
        self.model_id = self.config.pop("model_id")
        self.prompt = ""
        self.is_stream = self.config.pop("stream")

    def _load_config(self, config_path):
        with open(config_path, "r") as file:
            return yaml.safe_load(file)

    def format_prompt(self, args):
        self.prompt = self.template.format(**args)

    def format_message(self, args):
        if "claude-3" in self.model_id:
            self._format_message_claude3(args)
        elif "command-r-plus" in self.model_id:
            self._format_message_command_r_plus(args)

    def _format_message_claude3(self, args):
        message = self.config["messages"][0]["content"][0]["text"]
        self.config["messages"][0]["content"][0]["text"] = message.format(**args)

    def _format_message_command_r_plus(self, args):
        message = self.config["message"]
        self.config["message"] = message.format(**args)
