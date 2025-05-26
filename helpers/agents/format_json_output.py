from models.AgentResponseModel import ResponseModel

def get_result_message_output(result: any) -> str:
    """
    This function formats the result string to be used in the output message.
    """
    intermediate_steps = result["intermediate_steps"]
    first_observation = intermediate_steps[0][1]
    
    parsed_response = ResponseModel.model_validate(first_observation)
    return parsed_response.response if parsed_response.success else "Comando executado, mas não houve uma resposta clara do assistente."