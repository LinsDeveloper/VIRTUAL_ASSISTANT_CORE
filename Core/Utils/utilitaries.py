# Função para chamar a ferramenta com base na invocação

class CoreUtils(object):
    def call_tools(tool_invocation: dict, tool_map: dict) -> Union[str, Runnable]:
        tool = tool_map[tool_invocation["type"]]
        return RunnablePassthrough.assign(output=itemgetter("args") | tool)


    # Função para construir e executar a cadeia de processamento
    async def executor_chain(model_with_tools, tool_map, query):
        call_tool_func = lambda tool_invocation: chamar_ferramenta(tool_invocation, tool_map)
        call_tool_list = RunnableLambda(call_tool_func).map()
        chain = model_with_tools | JsonOutputToolsParser() | call_tool_list
        return chain.invoke(query)


    def carregar_modulos_e_ferramentas(nome_agente):
        session = create_db_session_admin()
        try:
            # Consultar o banco de dados para obter nomes de módulos, ferramentas e código do módulo do agente especificado
            agente = session.query(Agente).filter_by(nome_agente=nome_agente).first()
            ferramentas = agente.ferramentas

            # Carregar as ferramentas dinamicamente
            ferramentas_carregadas = []
            for ferramenta in ferramentas:
                codigo_modulo = ferramenta.modulo_python
                
                local_vars = {}
                global_vars = {}
                exec(codigo_modulo, global_vars, local_vars)

                ferramenta_carregada = local_vars.get(ferramenta.nome_rotina)

                if ferramenta_carregada:
                    ferramentas_carregadas.append(ferramenta_carregada)

            return ferramentas_carregadas
        finally:
            session.close()


    async def inicializar_agente_com_ferramentas_dinamicas(llm, nome_agente):
        ferramentas = carregar_modulos_e_ferramentas(nome_agente)
        #model_with_tools, tool_map = llm.bind(tools=[format_tool_to_openai_tool(t) for t in ferramentas]), {f.__name__: f for f in ferramentas}

        tool_map = {f.name: f.func for f in ferramentas}
        model_with_tools = llm.bind(tools=[format_tool_to_openai_tool(t) for t in ferramentas], tool_map=tool_map)
    
        return model_with_tools, tool_map


    async def chat_agent_dynamic(app_keys: AppKeys, app_params: AppParams, query: str) -> str:
        try:
            llm = ChatOpenAI(temperature=0, model=app_keys.OPENAI_MODEL, api_key=app_keys.OPENAI_API_KEY, verbose=app_keys.DEBUG(2))
            model_with_tools, tool_map = await inicializar_agente_com_ferramentas_dinamicas(llm, app_keys.NOME_AGENTE)
            resultado = await executar_cadeia(model_with_tools, tool_map, query)
            print(resultado)
            return resultado
        except Exception as e:
            print(f"Ocorreu um erro ao inicializar o ChatBot: {str(e)}")