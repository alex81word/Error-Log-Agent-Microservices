from langchain_openai import ChatOpenAI

from error_log_agent_microservices.openai_client import create_chat_model


def test_create_chat_model_uses_chat_openai(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    model = create_chat_model(model="gpt-4.1-mini", temperature=0.2)

    assert isinstance(model, ChatOpenAI)
    assert model.temperature == 0.2
