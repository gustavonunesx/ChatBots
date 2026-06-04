from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

# ─── Insira sua API Key da ExchangeRate-API aqui ───────────────────────────────
API_KEY = "SUA_API_KEY_AQUI"
API_URL = "https://v6.exchangerate-api.com/v6/{key}/pair/{origem}/{destino}/{valor}"

# ─── Normalização de nomes de moedas para código ISO ──────────────────────────
MOEDAS = {
    # Real
    "real": "BRL", "reais": "BRL", "real brasileiro": "BRL",
    "reais brasileiros": "BRL", "brl": "BRL",

    # Dólar
    "dolar": "USD", "dólar": "USD", "dolares": "USD", "dólares": "USD",
    "dolar americano": "USD", "dólares americanos": "USD",
    "usd": "USD", "us dollar": "USD",

    # Euro
    "euro": "EUR", "euros": "EUR", "eur": "EUR",

    # Libra
    "libra": "GBP", "libras": "GBP", "libra esterlina": "GBP",
    "libras esterlinas": "GBP", "gbp": "GBP",

    # Iene
    "iene": "JPY", "ienes": "JPY", "yen": "JPY", "jpy": "JPY",

    # Peso
    "peso": "ARS", "pesos": "ARS", "peso argentino": "ARS", "ars": "ARS",
    "peso mexicano": "MXN", "mxn": "MXN",

    # Franco
    "franco": "CHF", "francos": "CHF", "franco suico": "CHF",
    "franco suíço": "CHF", "chf": "CHF",

    # Dólar canadense
    "dolar canadense": "CAD", "dólares canadenses": "CAD", "cad": "CAD",

    # Dólar australiano
    "dolar australiano": "AUD", "dólares australianos": "AUD", "aud": "AUD",

    # Yuan
    "yuan": "CNY", "renminbi": "CNY", "cny": "CNY",

    # Bitcoin
    "bitcoin": "BTC", "btc": "BTC",
}

MOEDAS_LISTADAS = {
    "BRL": "Real Brasileiro 🇧🇷",
    "USD": "Dólar Americano 🇺🇸",
    "EUR": "Euro 🇪🇺",
    "GBP": "Libra Esterlina 🇬🇧",
    "JPY": "Iene Japonês 🇯🇵",
    "ARS": "Peso Argentino 🇦🇷",
    "MXN": "Peso Mexicano 🇲🇽",
    "CHF": "Franco Suíço 🇨🇭",
    "CAD": "Dólar Canadense 🇨🇦",
    "AUD": "Dólar Australiano 🇦🇺",
    "CNY": "Yuan Chinês 🇨🇳",
}


def normalizar_moeda(nome: str) -> str:
    """Converte nome natural para código ISO da moeda."""
    if not nome:
        return None
    chave = nome.lower().strip()
    return MOEDAS.get(chave, nome.upper())


class ActionConverterMoeda(Action):

    def name(self) -> Text:
        return "action_converter_moeda"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        valor       = tracker.get_slot("valor")
        moeda_orig  = tracker.get_slot("moeda_origem")
        moeda_dest  = tracker.get_slot("moeda_destino")

        # ── Dados faltantes ────────────────────────────────────────────────────
        if not valor:
            dispatcher.utter_message(response="utter_pedir_valor")
            return []

        if not moeda_orig:
            dispatcher.utter_message(response="utter_pedir_moeda_origem")
            return []

        if not moeda_dest:
            dispatcher.utter_message(response="utter_pedir_moeda_destino")
            return []

        # ── Normalização ───────────────────────────────────────────────────────
        codigo_orig = normalizar_moeda(moeda_orig)
        codigo_dest = normalizar_moeda(moeda_dest)

        # ── Chamada à API ──────────────────────────────────────────────────────
        try:
            url = API_URL.format(
                key=API_KEY,
                origem=codigo_orig,
                destino=codigo_dest,
                valor=valor,
            )
            resposta = requests.get(url, timeout=10)
            dados = resposta.json()

            if dados.get("result") == "success":
                resultado     = dados.get("conversion_result", 0)
                taxa          = dados.get("conversion_rate", 0)

                dispatcher.utter_message(
                    text=(
                        f"💱 *Conversão de câmbio:*\n"
                        f"➡️  {valor} {codigo_orig} = *{resultado:.2f} {codigo_dest}*\n"
                        f"📊 Taxa atual: 1 {codigo_orig} = {taxa:.4f} {codigo_dest}\n\n"
                        f"_Cotação em tempo real via ExchangeRate-API_"
                    )
                )
            else:
                erro = dados.get("error-type", "desconhecido")
                dispatcher.utter_message(
                    text=(
                        f"❌ Não consegui realizar a conversão.\n"
                        f"Erro: {erro}\n"
                        f"Verifique se as moedas informadas são válidas."
                    )
                )

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="❌ Sem conexão com a internet. Verifique sua rede e tente novamente."
            )
        except requests.exceptions.Timeout:
            dispatcher.utter_message(
                text="⏱️ A API demorou para responder. Tente novamente em instantes."
            )
        except Exception as e:
            dispatcher.utter_message(
                text=f"❌ Ocorreu um erro inesperado: {str(e)}"
            )

        return []


class ActionListarMoedas(Action):

    def name(self) -> Text:
        return "action_listar_moedas"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        lista = "\n".join(
            f"• {codigo} — {nome}"
            for codigo, nome in MOEDAS_LISTADAS.items()
        )

        dispatcher.utter_message(
            text=(
                f"💱 *Moedas suportadas pelo CambioBot:*\n\n"
                f"{lista}\n\n"
                f"Para converter, diga algo como:\n"
                f"'Converta 100 dólares para reais'"
            )
        )

        return []
