# Chat History Feature Specification
## Overview
Store and retrieve all user-AI conversations based on `current_user.id` in the `/support/chatkit` endpoint.

## Database Model
```python
class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_message"
    id: Optional[str] = Field(default=None, primary_key=True)
    userId: str
    role: str # "user" or "assistant"
    content: str
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

## Implementation Flow
### 1. When User Sends Message
- Save user message with `role="user"` and `userId=current_user.id`
### 2. When AI Responds
- Save AI response with `role="assistant"` and `userId=current_user.id`
### 3. Before Processing New Message
- Retrieve all previous messages for `current_user.id` ordered by `createdAt`
- Pass full history to AI

## Code Changes in `backend/app/main.py`
```python
@app.post("/support/chatkit")
async def chatkit_endpoint(
    request: Request,
    server: CustomerSupportServer = Depends(get_server),
    current_user: User = Depends(get_current_user),
    db: SQLSession = Depends(get_session)
) -> Response:
    # 1. Retrieve chat history
    chat_history = db.query(ChatMessage).filter(
        ChatMessage.userId == current_user.id
    ).order_by(ChatMessage.createdAt.asc()).all()

    # 2. Extract and save user message
    user_message = ChatMessage(
        userId=current_user.id,
        role="user",
        content=user_input_text
    )
    db.add(user_message)
    db.commit()

    # 3. Format history for AI
    formatted_history = [
        {"role": msg.role, "content": msg.content} for msg in chat_history
    ]

    # 4. Process with AI (pass history)
    result = await server.process(payload, {"chat_history": formatted_history})

    # 5. Save AI response
    assistant_message = ChatMessage(
        userId=current_user.id,
        role="assistant",
        content=ai_response_text
    )
    db.add(assistant_message)
    db.commit()

    return result
```

## Key Points
- Each user's messages stored with their `userId`
- Messages retrieved in chronological order
- AI gets full conversation history every time
- Two roles: `"user"` and `"assistant"`