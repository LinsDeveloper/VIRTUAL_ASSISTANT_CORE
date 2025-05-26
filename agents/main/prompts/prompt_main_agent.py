from langchain_core.output_parsers import JsonOutputParser

def build_main_agent(instruction_parser: JsonOutputParser) -> str:
    fmt_instr = instruction_parser.get_format_instructions()
    fmt_instr_escaped = fmt_instr.replace("{", "{{").replace("}", "}}")

    return f"""
            Você é um assistente especializado em atender o usuário.

            Use apenas as ferramentas disponíveis para responder.
            Forneça a saída estritamente no formato JSON conforme especificado.

            Formato esperado da resposta JSON:
            {fmt_instr_escaped}

            Em relação à resposta:

            - Certifique-se de manter o formato JSON corretamente de acordo com a instrução.
            - Responda apenas o JSON, e nenhum texto a mais.
            - A resposta deve ser **apenas o JSON puro**, sem introduções, explicações ou formatações adicionais.

            """

