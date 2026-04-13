from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

# ── URL base da Open Library API (sem chave de API) ───────────────────────────
BASE_URL = "https://openlibrary.org/search.json"


def formatar_livros(docs, limite=5):
    """Formata os resultados da API em texto legível."""
    if not docs:
        return None

    resultado = ""
    for i, livro in enumerate(docs[:limite], 1):
        titulo    = livro.get("title", "Título desconhecido")
        autores   = livro.get("author_name", ["Autor desconhecido"])
        ano       = livro.get("first_publish_year", "Ano desconhecido")
        edicoes   = livro.get("edition_count", 0)
        chave     = livro.get("key", "")
        link      = f"https://openlibrary.org{chave}" if chave else "Link indisponível"

        resultado += (
            f"\n {i}. *{titulo}*\n"
            f"     Autor(es): {', '.join(autores[:2])}\n"
            f"    Ano: {ano} | Edições: {edicoes}\n"
            f"    {link}\n"
        )

    return resultado


class ActionBuscarTitulo(Action):

    def name(self) -> Text:
        return "action_buscar_titulo"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        titulo = tracker.get_slot("titulo")

        if not titulo:
            dispatcher.utter_message(response="utter_pedir_titulo")
            return []

        dispatcher.utter_message(text=f" Buscando livros com o título: *{titulo}*...")

        try:
            resposta = requests.get(
                BASE_URL,
                params={"title": titulo, "lang": "por", "limit": 5},
                timeout=10,
            )
            dados = resposta.json()
            docs  = dados.get("docs", [])

            if docs:
                texto = formatar_livros(docs)
                dispatcher.utter_message(
                    text=f"Encontrei {dados.get('numFound', 0)} resultado(s). Aqui estão os principais:\n{texto}"
                )
            else:
                dispatcher.utter_message(
                    text=f" Não encontrei livros com o título '{titulo}'. Tente verificar a ortografia."
                )

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(text=" Sem conexão com a internet. Verifique sua rede.")
        except requests.exceptions.Timeout:
            dispatcher.utter_message(text="⏱ A API demorou para responder. Tente novamente.")
        except Exception as e:
            dispatcher.utter_message(text=f" Erro inesperado: {str(e)}")

        return []


class ActionBuscarAutor(Action):

    def name(self) -> Text:
        return "action_buscar_autor"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        autor = tracker.get_slot("autor")

        if not autor:
            dispatcher.utter_message(response="utter_pedir_autor")
            return []

        dispatcher.utter_message(text=f" Buscando livros do autor: *{autor}*...")

        try:
            resposta = requests.get(
                BASE_URL,
                params={"author": autor, "limit": 5},
                timeout=10,
            )
            dados = resposta.json()
            docs  = dados.get("docs", [])

            if docs:
                texto = formatar_livros(docs)
                dispatcher.utter_message(
                    text=f" Encontrei {dados.get('numFound', 0)} obra(s) de *{autor}*:\n{texto}"
                )
            else:
                dispatcher.utter_message(
                    text=f" Não encontrei livros do autor '{autor}'. Tente o nome completo."
                )

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(text="❌ Sem conexão com a internet.")
        except requests.exceptions.Timeout:
            dispatcher.utter_message(text=" A API demorou. Tente novamente.")
        except Exception as e:
            dispatcher.utter_message(text=f"❌ Erro: {str(e)}")

        return []


class ActionBuscarAssunto(Action):

    def name(self) -> Text:
        return "action_buscar_assunto"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        assunto = tracker.get_slot("assunto")

        if not assunto:
            dispatcher.utter_message(response="utter_pedir_assunto")
            return []

        dispatcher.utter_message(text=f" Buscando livros sobre: *{assunto}*...")

        try:
            resposta = requests.get(
                BASE_URL,
                params={"subject": assunto, "limit": 5},
                timeout=10,
            )
            dados = resposta.json()
            docs  = dados.get("docs", [])

            if docs:
                texto = formatar_livros(docs)
                dispatcher.utter_message(
                    text=f" Encontrei {dados.get('numFound', 0)} livro(s) sobre *{assunto}*:\n{texto}"
                )
            else:
                # Tenta busca geral se assunto não retornar resultado
                resposta2 = requests.get(
                    BASE_URL,
                    params={"q": assunto, "limit": 5},
                    timeout=10,
                )
                dados2 = resposta2.json()
                docs2  = dados2.get("docs", [])

                if docs2:
                    texto = formatar_livros(docs2)
                    dispatcher.utter_message(
                        text=f" Resultados relacionados a *{assunto}*:\n{texto}"
                    )
                else:
                    dispatcher.utter_message(
                        text=f" Não encontrei livros sobre '{assunto}'. Tente outro assunto."
                    )

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(text=" Sem conexão com a internet.")
        except requests.exceptions.Timeout:
            dispatcher.utter_message(text=" A API demorou. Tente novamente.")
        except Exception as e:
            dispatcher.utter_message(text=f" Erro: {str(e)}")

        return []
