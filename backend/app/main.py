from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from typing import Any, AsyncIterator, Optional
from fastapi import Header

from agents import RunConfig, Runner
from agents.model_settings import ModelSettings
from chatkit.agents import AgentContext, stream_agent_response
from chatkit.server import ChatKitServer, StreamingResult
from chatkit.types import (
    Action,
    AssistantMessageContent,
    AssistantMessageItem,
    Attachment,
    HiddenContextItem,
    ThreadItemDoneEvent,
    ThreadItemUpdated,
    ThreadMetadata,
    ThreadStreamEvent,
    UserMessageItem,
    WidgetItem,
    WidgetRootUpdated,
)
from fastapi import Depends, FastAPI, Query, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse
from openai.types.responses import (
    EasyInputMessageParam,
    ResponseInputContentParam,
    ResponseInputTextParam,
)
from sqlmodel import Session as SQLSession
from pydantic import ValidationError
from starlette.responses import JSONResponse

from .database import get_session, User, UserSession, ChatMessage, create_db_and_tables
from .auth import decode_jwt_token, get_email_from_token, InvalidTokenException

from .airline_state import AirlineStateManager, CustomerProfile
from .memory_store import MemoryStore
from .support_agent import state_manager, support_agent
from .thread_item_converter import CustomerSupportThreadItemConverter

DEFAULT_THREAD_ID = "demo_default_thread"
logger = logging.getLogger(__name__)


class CustomerSupportServer(ChatKitServer[dict[str, Any]]):
    def __init__(
        self,
        agent_state: AirlineStateManager,
    ) -> None:
        store = MemoryStore()
        super().__init__(store)
        self.store = store
        self.agent_state = agent_state
        self.agent = support_agent
        self.thread_item_converter = CustomerSupportThreadItemConverter()

    async def action(
        self,
        thread: ThreadMetadata,
        action: Action[str, Any],
        sender: WidgetItem | None,
        context: dict[str, Any],
    ) -> AsyncIterator[ThreadStreamEvent]:
        # Action handler removed - no meal preferences
        return
        yield  # Make it a generator

    async def respond(
        self,
        thread: ThreadMetadata,
        input_user_message: UserMessageItem | None,
        context: dict[str, Any],
    ) -> AsyncIterator[ThreadStreamEvent]:
        items_page = await self.store.load_thread_items(thread.id, None, 20, "desc", context)
        items = list(reversed(items_page.data))
        
        # Get chat history from context if available
        chat_history = context.get("chat_history", [])
        
        # Convert chat history to input items
        history_items = []
        if chat_history:
            print(f"🔄 Converting {len(chat_history)} messages from database history")
            for i, msg in enumerate(chat_history):
                print(f"  Message {i+1}: role={msg['role']}, content={msg['content'][:30]}...")
                
                if msg["role"] == "user":
                    history_items.append(
                        EasyInputMessageParam(
                            type="message",
                            role="user",
                            content=[ResponseInputTextParam(type="input_text", text=msg["content"])],
                        )
                    )
                elif msg["role"] == "assistant":
                    # Use output_text for assistant messages
                    from openai.types.responses import ResponseOutputTextParam
                    history_items.append(
                        EasyInputMessageParam(
                            type="message",
                            role="assistant",
                            content=[ResponseOutputTextParam(type="output_text", text=msg["content"])],
                        )
                    )
            print(f"✅ Converted {len(history_items)} history items for agent")
        
        # Use history items if available, otherwise use converted thread items
        if history_items:
            input_items = history_items
            print(f"📤 Sending to agent: {len(history_items)} history messages")
        else:
            converted_items = await self.thread_item_converter.to_agent_input(items)
            input_items = converted_items
            print(f"📤 Sending to agent: {len(converted_items)} thread messages")

        agent_context = AgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )
        result = Runner.run_streamed(
            self.agent,
            input_items,
            context=agent_context,
            run_config=RunConfig(model_settings=ModelSettings(temperature=0.4)),
        )

        async for event in stream_agent_response(agent_context, result):
            yield event

    async def _load_full_thread(self, thread_id: str, context: dict[str, Any]):
        from chatkit.types import Thread
        
        thread_meta = await self.store.load_thread(thread_id, context)
        thread_items_page = await self.store.load_thread_items(
            thread_id, None, 100, "asc", context
        )
        
        thread_dict = thread_meta.model_dump()
        thread_dict.pop('items', None)
        
        return Thread(**thread_dict, items=thread_items_page)

    async def to_message_content(self, _input: Attachment) -> ResponseInputContentParam:
        raise RuntimeError("File attachments are not supported in this demo.")


support_server = CustomerSupportServer(agent_state=state_manager)

app = FastAPI(title="ChatKit Customer Support API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000", 
    ],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
    expose_headers=["*"], 
)


@app.on_event("startup")
async def on_startup():
    """Initialize database tables on application startup"""
    print("🚀 Creating database tables...")
    try:
        create_db_and_tables()
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        import traceback
        traceback.print_exc()


def get_server() -> CustomerSupportServer:
    return support_server


async def get_current_user(
    authorization: str = Header(...), db: SQLSession = Depends(get_session)
) -> User:
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise InvalidTokenException("Invalid authentication scheme.")
        
        print(f"🔑 Token received: {token[:20]}...")
        
        user = None
        
        if '.' in token and token.count('.') == 2:
            print("📧 JWT token detected, extracting email...")
            email = get_email_from_token(token)
            user = db.query(User).filter(User.email == email).first()
            
            if not user:
                print(f"👤 User not found with email: {email}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"error": "User not found with provided email", "status": 404},
                )
            
            active_sessions = db.query(UserSession).filter(
                UserSession.userId == user.id, 
                UserSession.expiresAt > datetime.now(timezone.utc)
            ).first()
            
            if not active_sessions:
                print(f"🔗 No active sessions found for user: {user.email}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"error": "No active sessions found for user", "status": 404},
                )
        else:
            print("🎫 Session token detected, looking up in database...")
            
            session = db.query(UserSession).filter(
                UserSession.token == token
            ).first()
            
            if not session:
                print(f"🔍 Token not found, checking if it's a userId...")
                user = db.query(User).filter(User.id == token).first()
                
                if not user:
                    print(f"❌ Neither session token nor userId found")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail={"error": "Invalid authentication token", "status": 401},
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                
                active_session = db.query(UserSession).filter(
                    UserSession.userId == user.id,
                    UserSession.expiresAt > datetime.now(timezone.utc)
                ).first()
                
                if not active_session:
                    print(f"❌ No active session for user")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail={"error": "No active session found", "status": 401},
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                
                print(f"✅ User found via userId: {user.email}")
            else:
                print(f"✅ Session found! Expires: {session.expiresAt}")
                current_time = datetime.now(timezone.utc)
                
                if session.expiresAt <= current_time:
                    print(f"❌ Session expired")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail={"error": "Session has expired", "status": 401},
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                
                user = db.query(User).filter(User.id == session.userId).first()
                
                if not user:
                    print(f"👤 User not found for session")
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail={"error": "User not found", "status": 404},
                    )

        print(f"✅ User authenticated: {user.email} (ID: {user.id})")
        return user
        
    except InvalidTokenException as e:
        print(f"❌ JWT Validation Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": str(e), "status": 401},
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValueError as e:
        print(f"❌ Authorization header malformed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid Authorization header format", "status": 401},
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ An unexpected error occurred during authentication: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "An unexpected error occurred during authentication", "status": 500},
        )


@app.options("/support/chatkit")
async def chatkit_options():
    return Response(status_code=200)


@app.post("/support/chatkit")
async def chatkit_endpoint(
    request: Request, 
    server: CustomerSupportServer = Depends(get_server),
    current_user: User = Depends(get_current_user),
    db: SQLSession = Depends(get_session)
) -> Response:
    import uuid
    import json
    import re
    
    try:
        print(f"📥 Processing chatkit request for user: {current_user.email} (userId: {current_user.id})")
        
        # Get the request body
        body = await request.body()
        
        # Parse the incoming request to extract user message
        user_input = ""
        try:
            payload_json = json.loads(body)
            print(f"📦 Full Payload: {json.dumps(payload_json, indent=2)}")
            
            # ChatKit sends messages in a specific format
            if isinstance(payload_json, dict):
                # Method 1: params.input.content structure (ChatKit threads.create)
                if "params" in payload_json and isinstance(payload_json["params"], dict):
                    params = payload_json["params"]
                    if "input" in params and isinstance(params["input"], dict):
                        input_data = params["input"]
                        if "content" in input_data and isinstance(input_data["content"], list):
                            for content_item in input_data["content"]:
                                if isinstance(content_item, dict) and content_item.get("type") == "input_text":
                                    user_input = content_item.get("text", "")
                                    print(f"✅ Found message in params.input.content structure")
                                    break
                
                # Method 2: Direct message
                if not user_input and "message" in payload_json:
                    user_input = payload_json["message"]
                    print(f"✅ Found message in 'message' key")
                
                # Method 3: Item structure (ChatKit format)
                if not user_input and "item" in payload_json:
                    item = payload_json["item"]
                    if isinstance(item, dict):
                        # Check if it's a user_message type
                        if item.get("type") == "user_message":
                            content = item.get("content", [])
                            if isinstance(content, list):
                                for content_item in content:
                                    if isinstance(content_item, dict) and content_item.get("type") == "input_text":
                                        user_input = content_item.get("text", "")
                                        print(f"✅ Found message in item.content structure")
                                        break
                        # Also check content directly
                        elif "content" in item:
                            content = item["content"]
                            if isinstance(content, list):
                                for content_item in content:
                                    if isinstance(content_item, dict) and content_item.get("type") == "input_text":
                                        user_input = content_item.get("text", "")
                                        print(f"✅ Found message in item.content (alt)")
                                        break
                
                # Method 4: Top-level content
                if not user_input and "content" in payload_json:
                    content = payload_json["content"]
                    if isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict) and item.get("type") == "input_text":
                                user_input = item.get("text", "")
                                print(f"✅ Found message in top-level content")
                                break
                    elif isinstance(content, str):
                        user_input = content
                        print(f"✅ Found message as string content")
                
                # Method 5: Direct input
                if not user_input and "input" in payload_json:
                    input_val = payload_json["input"]
                    if isinstance(input_val, str):
                        user_input = input_val
                        print(f"✅ Found message in 'input' key")
                    elif isinstance(input_val, dict) and "content" in input_val:
                        content = input_val["content"]
                        if isinstance(content, list):
                            for item in content:
                                if isinstance(item, dict) and item.get("type") == "input_text":
                                    user_input = item.get("text", "")
                                    print(f"✅ Found message in input.content")
                                    break
                
                # Method 6: Text field
                if not user_input and "text" in payload_json:
                    user_input = payload_json["text"]
                    print(f"✅ Found message in 'text' key")
            
            # Save user message to database
            if user_input and user_input.strip():
                user_msg = ChatMessage(
                    id=str(uuid.uuid4()),
                    userId=current_user.id,
                    role="user",
                    content=user_input.strip()
                )
                db.add(user_msg)
                db.commit()
                print(f"💾 Saved user message: {user_input[:50]}...")
            else:
                print(f"⚠️ No user input found in payload")
            
        except json.JSONDecodeError as e:
            print(f"⚠️ Could not parse JSON payload: {e}")
        
        # Get chat history
        chat_history = db.query(ChatMessage).filter(
            ChatMessage.userId == current_user.id
        ).order_by(ChatMessage.createdAt.asc()).all()
        
        formatted_history = [
            {"role": msg.role, "content": msg.content}
            for msg in chat_history
        ]
        
        print(f"📚 Retrieved {len(chat_history)} messages from history")
        
        # Process the request
        result = await server.process(
            body, 
            {
                "request": request,
                "chat_history": formatted_history,
                "current_user": current_user
            }
        )
        
        if isinstance(result, StreamingResult):
            async def save_response_wrapper():
                collected_text = ""
                
                async for chunk in result:
                    # Yield chunk to client
                    yield chunk
                    
                    # Parse SSE data to extract assistant message
                    if chunk:
                        try:
                            chunk_str = chunk.decode() if isinstance(chunk, bytes) else str(chunk)
                            
                            # Extract text deltas from SSE events
                            for line in chunk_str.split('\n'):
                                if line.startswith('data: '):
                                    data_str = line[6:]  # Remove 'data: ' prefix
                                    try:
                                        data = json.loads(data_str)
                                        
                                        # Look for text delta updates
                                        if data.get("type") == "thread.item.updated":
                                            update = data.get("update", {})
                                            if update.get("type") == "assistant_message.content_part.text_delta":
                                                delta = update.get("delta", "")
                                                collected_text += delta
                                        
                                        # Or look for complete message in done event
                                        elif data.get("type") == "thread.item.done":
                                            item = data.get("item", {})
                                            if item.get("type") == "assistant_message":
                                                content = item.get("content", [])
                                                for content_item in content:
                                                    if content_item.get("type") == "output_text":
                                                        text = content_item.get("text", "")
                                                        if text and not collected_text:
                                                            collected_text = text
                                    
                                    except json.JSONDecodeError:
                                        continue
                        except Exception as e:
                            print(f"⚠️ Error parsing chunk: {e}")
                
                # Save the collected assistant response
                if collected_text:
                    assistant_msg = ChatMessage(
                        id=str(uuid.uuid4()),
                        userId=current_user.id,
                        role="assistant",
                        content=collected_text
                    )
                    db.add(assistant_msg)
                    db.commit()
                    print(f"💾 Saved assistant response: {collected_text[:100]}...")
            
            return StreamingResponse(save_response_wrapper(), media_type="text/event-stream")
        
        if hasattr(result, "json"):
            return Response(content=result.json, media_type="application/json")
        
        return JSONResponse(result)
        
    except Exception as e:
        print(f"❌ Error in chatkit_endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise


@app.get("/support/customer")
async def customer_snapshot(
    thread_id: str | None = Query(None, description="ChatKit thread identifier"),
    server: CustomerSupportServer = Depends(get_server),
) -> dict[str, Any]:
    key = thread_id or DEFAULT_THREAD_ID
    data = server.agent_state.to_dict(key)
    return {"customer": data}


@app.get("/support/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}