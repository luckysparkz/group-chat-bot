from dataclasses import dataclass


@dataclass
class ChatMessage:
    id: int
    user_id: int
    user_full_name: str
    content: str
    sent_at: int
