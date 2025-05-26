from pydantic import BaseModel
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class ResponseModel(BaseModel):
    success: bool = Field(..., description="Indica se a operação foi bem-sucedida (True) ou não (False).")
    response: str = Field(..., description="Retorno da operação.")



class AgentResponseModel(BaseModel):
    thought: str
    action: str
    action_input: Optional[str]
    output_response: ResponseModel
