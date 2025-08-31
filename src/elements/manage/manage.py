import yaml

class ModelManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.model_config = self.load_model_config()

    def load_model_config(self):
        with open(self.config_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get_model_name(self):
        return self.model_config["model_name"]
    

model_manager = ModelManager("src/config/models.yaml")

      



class PromptManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.prompt_config = self.load_prompt_config()

    def load_prompt_config(self):
        with open(self.config_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get_prompt(self, category, key, **kwargs):
        prompt = self.prompt_config.get(category, {}).get(key, "")
        return prompt.format(**kwargs)
    

prompt_manager = PromptManager("src/config/prompts.yaml")
if __name__ =="__main__":
    print(prompt_manager.get_prompt("ch_to_en_chat", "chat", **{"current_task":""}))