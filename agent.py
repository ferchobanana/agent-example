import getpass
import os

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Configura la API key de OpenAI en tus variables de entorno")

# Establecemos el modelo de lenguaje que usaremos
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o-mini")

# =================
# Definimos las herramientas para el agente
# El nombre de la funcion, el docstring y el tipo de dato de los argumentos
# son parte del prompt que el framework le da al Agente, asi que es importante ser precisos
def get_stripe_link(amount: int) -> str:
    """Obten el enlace de un stripe checkout a partir de un monto

    Args:
        amount: el monto total del pago que se debe generar en el checkout
    """
    # =================================================== 
    # Aqui implementamos toda la lógica de la herramienta
    # ===================================================
    return "https://buy.stripe.com/SDFG74F44SD"

# Y podemos agregar mas herramientas de la misma manera

tools = [get_stripe_link]

# =================
# Creamos el agente
from langgraph.prebuilt import create_react_agent

agent_executor = create_react_agent(model, tools)

# =================
# Corremos el agente
from langchain_core.messages import HumanMessage, SystemMessage

# Forma 1:
# Asi obtendriamos un arreglo con todos los mensajes tanto de input, 
# como los de llamado de herramientas y los de outputs
response = agent_executor.invoke({"messages": [
        SystemMessage(content="Eres un asistente virtual para la empresa ... tu objetivo es ..."),
        HumanMessage(content="Hola!")
    ]})
response["messages"]

# Forma 2:
# De esta manera obtendriamos un streaming de mensajes según se vayan generando
# se imprimiria en consola cada mensaje según los vaya generando el agente y no en un solo arreglo
for chunk in agent_executor.stream(
    {"messages": [
        SystemMessage(content="Eres un asistente virtual para la empresa ... tu objetivo es ..."),
        HumanMessage(content="Hola")
    ]}
):
    print("-- Nuevo mensaje: --")
    print(chunk)