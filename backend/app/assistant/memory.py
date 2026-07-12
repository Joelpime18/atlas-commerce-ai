from pydantic import BaseModel, Field


class ConversationSession(BaseModel):
    customer_id: str
    flow: str | None = None
    step: str | None = None
    data: dict[str, str] = Field(default_factory=dict)


class ConversationMemory:
    _sessions: dict[str, ConversationSession] = {}

    @classmethod
    def get(cls, customer_id: str) -> ConversationSession:
        if customer_id not in cls._sessions:
            cls._sessions[customer_id] = ConversationSession(customer_id=customer_id)

        return cls._sessions[customer_id]

    @classmethod
    def start(cls, customer_id: str, flow: str, step: str) -> ConversationSession:
        session = ConversationSession(customer_id=customer_id, flow=flow, step=step)
        cls._sessions[customer_id] = session
        return session

    @classmethod
    def clear(cls, customer_id: str) -> None:
        cls._sessions.pop(customer_id, None)

    @classmethod
    def clear_all(cls) -> None:
        cls._sessions.clear()
