from pydantic import BaseModel, Field

class OutputBaseModel(BaseModel):
    """
    Base model for output parsers.
    """

    success: bool = Field(description="Indica se deu sucesso ou não.")
    message: str = Field(description="message de retorno.")
    data: dict = Field(
        description="Retorna dados, caso não tem, deve ficar vazio."
    )
    error: str = Field(
        default=None,
        description="Indica motivo do erro caso não tenha sucesso.",
    )