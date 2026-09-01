import os, yaml
from dotenv import load_dotenv
load_dotenv()

def load_config() -> dict:
    with open("topics.yaml","r") as f:
        config = yaml.safe_load(f)
    
    config["hf_token"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    if not config["hf_token"]:
        raise ValueError("HUgging face token not found")
    return config

if __name__ == "__main__":
    config = load_config()
    print("Topics:", config["topics"])
    print("Top N:", config["top_n"])
    print("Schedule:", config["schedule"])
    print("config.py OK")