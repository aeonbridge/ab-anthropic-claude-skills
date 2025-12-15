#!/usr/bin/env python3
"""
WhatsApp Knowledge Bot with Temporal Memory

This bot combines three Claude Skills:
1. Evolution API - WhatsApp integration
2. Dify - LLM processing with RAG
3. Graphiti - Temporal knowledge graph for memory

Architecture:
- Receives WhatsApp messages via Evolution API webhooks
- Retrieves conversation context from Graphiti temporal graph
- Processes with Dify's RAG pipeline for intelligent responses
- Stores interaction in Graphiti for future context
- Sends response back through Evolution API
"""

import os
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Optional

import httpx
from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
from graphiti_core import Graphiti
from graphiti_core.nodes import EntityNode, EpisodeNode
from neo4j import AsyncGraphDatabase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment configuration
EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "http://evolution-api:8080")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY")
EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE", "whatsapp-bot")

DIFY_API_URL = os.getenv("DIFY_API_URL", "http://dify-api:5001")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# Initialize FastAPI app
app = FastAPI(title="WhatsApp Knowledge Bot")

# Initialize Graphiti for temporal knowledge graph
graphiti_client = None


class WhatsAppMessage(BaseModel):
    """WhatsApp message model"""
    phone: str
    message: str
    timestamp: int
    message_id: str


class KnowledgeBot:
    """Main bot class integrating all three skills"""

    def __init__(self):
        self.http_client = httpx.AsyncClient(timeout=30.0)
        self.graphiti = None

    async def initialize(self):
        """Initialize Graphiti connection"""
        try:
            driver = AsyncGraphDatabase.driver(
                NEO4J_URI,
                auth=(NEO4J_USER, NEO4J_PASSWORD)
            )
            self.graphiti = Graphiti(driver)
            await self.graphiti.build_indices()
            logger.info("✅ Graphiti initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Graphiti: {e}")
            raise

    async def get_conversation_context(
        self,
        phone: str,
        limit: int = 5
    ) -> List[Dict]:
        """
        Retrieve conversation context from Graphiti temporal graph

        Uses Graphiti skill to query temporal knowledge graph
        for previous interactions with this user.
        """
        try:
            # Search for user entity
            search_results = await self.graphiti.search(
                query=f"user {phone} conversations",
                num_results=limit
            )

            context = []
            for result in search_results:
                if isinstance(result, EpisodeNode):
                    context.append({
                        'timestamp': result.created_at,
                        'content': result.content,
                        'relevance': result.score if hasattr(result, 'score') else 1.0
                    })

            logger.info(f"📚 Retrieved {len(context)} context items for {phone}")
            return context

        except Exception as e:
            logger.error(f"❌ Error retrieving context: {e}")
            return []

    async def process_with_dify(
        self,
        message: str,
        context: List[Dict],
        phone: str
    ) -> str:
        """
        Process message using Dify's RAG pipeline

        Uses Dify skill to:
        1. Build context-aware prompt
        2. Query knowledge base
        3. Generate intelligent response
        """
        try:
            # Build context string
            context_str = "\n".join([
                f"[{ctx['timestamp']}] {ctx['content']}"
                for ctx in context[-3:]  # Last 3 interactions
            ])

            # Prepare Dify request
            payload = {
                "inputs": {
                    "phone": phone,
                    "conversation_history": context_str
                },
                "query": message,
                "response_mode": "blocking",
                "user": phone,
                "conversation_id": f"whatsapp_{phone}"
            }

            # Call Dify API
            response = await self.http_client.post(
                f"{DIFY_API_URL}/v1/chat-messages",
                headers={
                    "Authorization": f"Bearer {DIFY_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=payload
            )

            if response.status_code == 200:
                result = response.json()
                answer = result.get('answer', 'Desculpe, não consegui processar sua mensagem.')
                logger.info(f"✅ Dify response generated for {phone}")
                return answer
            else:
                logger.error(f"❌ Dify API error: {response.status_code}")
                return "Desculpe, ocorreu um erro ao processar sua mensagem."

        except Exception as e:
            logger.error(f"❌ Error processing with Dify: {e}")
            return "Desculpe, não foi possível processar sua mensagem no momento."

    async def store_interaction(
        self,
        phone: str,
        user_message: str,
        bot_response: str,
        timestamp: datetime
    ):
        """
        Store interaction in Graphiti temporal knowledge graph

        Uses Graphiti skill to:
        1. Create/update user entity
        2. Store conversation episode
        3. Link entities and episodes
        4. Maintain temporal relationships
        """
        try:
            # Create episode content
            episode_content = f"""
            User ({phone}): {user_message}
            Bot: {bot_response}
            """

            # Add episode to Graphiti
            episodes = await self.graphiti.add_episode(
                name=f"whatsapp_conversation_{phone}_{timestamp.timestamp()}",
                episode_body=episode_content,
                source_description=f"WhatsApp conversation with {phone}",
                reference_time=timestamp
            )

            logger.info(f"💾 Stored interaction in Graphiti for {phone}")

        except Exception as e:
            logger.error(f"❌ Error storing interaction: {e}")

    async def send_whatsapp_message(self, phone: str, message: str) -> bool:
        """
        Send message via Evolution API

        Uses Evolution API skill to send WhatsApp message
        """
        try:
            payload = {
                "number": phone,
                "text": message
            }

            response = await self.http_client.post(
                f"{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_INSTANCE}",
                headers={
                    "apikey": EVOLUTION_API_KEY,
                    "Content-Type": "application/json"
                },
                json=payload
            )

            if response.status_code in [200, 201]:
                logger.info(f"📤 Message sent to {phone}")
                return True
            else:
                logger.error(f"❌ Failed to send message: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"❌ Error sending message: {e}")
            return False

    async def handle_message(self, phone: str, message: str, timestamp: int):
        """
        Main message handler - orchestrates all three skills

        Flow:
        1. Get context from Graphiti (Skill 3)
        2. Process with Dify RAG (Skill 2)
        3. Send response via Evolution API (Skill 1)
        4. Store interaction in Graphiti (Skill 3)
        """
        try:
            logger.info(f"📨 Processing message from {phone}: {message}")

            # Step 1: Retrieve context from Graphiti
            context = await self.get_conversation_context(phone)

            # Step 2: Process with Dify
            response = await self.process_with_dify(message, context, phone)

            # Step 3: Send response via Evolution API
            sent = await self.send_whatsapp_message(phone, response)

            if sent:
                # Step 4: Store interaction in Graphiti
                await self.store_interaction(
                    phone=phone,
                    user_message=message,
                    bot_response=response,
                    timestamp=datetime.fromtimestamp(timestamp / 1000)
                )

            logger.info(f"✅ Message handled successfully for {phone}")

        except Exception as e:
            logger.error(f"❌ Error handling message: {e}")


# Global bot instance
bot = KnowledgeBot()


@app.on_event("startup")
async def startup_event():
    """Initialize bot on startup"""
    logger.info("🚀 Starting WhatsApp Knowledge Bot...")
    await bot.initialize()
    logger.info("✅ Bot ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Shutting down bot...")
    await bot.http_client.aclose()


@app.post("/webhook")
async def webhook_handler(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Evolution API webhook endpoint

    Receives WhatsApp messages and processes them asynchronously
    """
    try:
        data = await request.json()
        logger.info(f"📥 Webhook received: {data.get('event')}")

        # Handle different event types
        event = data.get('event')

        if event == 'messages.upsert':
            # Extract message data
            message_data = data.get('data', {})
            message_info = message_data.get('message', {})

            # Check if it's a text message and not from us
            if 'conversation' in message_info and not message_data.get('key', {}).get('fromMe'):
                phone = message_data.get('key', {}).get('remoteJid', '').split('@')[0]
                message_text = message_info.get('conversation', '')
                timestamp = message_data.get('messageTimestamp', 0)

                # Process message in background
                background_tasks.add_task(
                    bot.handle_message,
                    phone,
                    message_text,
                    int(timestamp) * 1000
                )

        return {"status": "success"}

    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        return {"status": "error", "message": str(e)}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "evolution_api": EVOLUTION_API_URL,
            "dify": DIFY_API_URL,
            "neo4j": NEO4J_URI
        }
    }


@app.get("/stats/{phone}")
async def get_user_stats(phone: str):
    """Get conversation statistics for a user"""
    try:
        context = await bot.get_conversation_context(phone, limit=100)
        return {
            "phone": phone,
            "total_interactions": len(context),
            "recent_interactions": context[:5]
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "bot:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
