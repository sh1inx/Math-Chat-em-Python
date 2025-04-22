import gradio as gr
from gradio_client import Client
from deep_translator import GoogleTranslator
import re

tradutor = GoogleTranslator(source="en", target="pt")

def limpar_resposta(texto):
    texto = texto.replace("\n", "<br>")
    texto = re.sub(r"{'Role': 'Assistant', 'Content': '(.*)}", r"\1", texto)
    texto = texto.replace("Resposta:", "<b>Resposta:</b>").replace("Ferramenta usada:", "<b>Ferramenta usada:</b>").replace("raciocínio:", "<b>Raciocínio:</b>")
    return texto.strip()

def processar_expressao(valor):
    client = Client("eribur/Basic_math_agent")
    result = client.predict(
        message=valor,
        api_name="/chat"
    )
    
    traducao = tradutor.translate(result)
    resposta_formatada = f"<b>Expressão:</b> {valor}<br><br>"
    resposta_formatada += f"<b>Detalhes:</b><br>{limpar_resposta(traducao)}"

    return resposta_formatada

def criar_interface():
    interface = gr.Interface(
        fn=processar_expressao,
        inputs=gr.Textbox(label="Digite sua expressão matemática", placeholder="Ex: Vinte e 2 mais cinqueta e 4"),
        outputs=gr.HTML(label="Resultado"),
        title="CHATBOT DE EXPRESSÕES MATEMÁTICAS",
        description="Digite uma expressão matemática para obter o resultado e a explicação em português.",
        theme="compact"
    )

    interface.launch()

if __name__ == "__main__":
    criar_interface()