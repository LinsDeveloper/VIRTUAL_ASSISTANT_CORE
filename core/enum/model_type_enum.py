from enum import Enum
import os
from dotenv import load_dotenv

load_dotenv()

class ModelTypeEnum(str, Enum):
    LLAMA3 = os.getenv("LLAMA3_8B_MODEL_NAME")
