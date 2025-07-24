# agent.py

from dotenv import load_dotenv
import os
import httpx
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel
import inspect

# ===== PATCH: Make supports_language and unlikely_threshold async if they're not already ======
if not hasattr(MultilingualModel, "__supports_language_asyncified"):
    orig = MultilingualModel.supports_language
    if not inspect.iscoroutinefunction(orig):
        async def supports_language_async(self, lang): return orig(self, lang)
        MultilingualModel.supports_language = supports_language_async
        MultilingualModel.__supports_language_asyncified = True

if not hasattr(MultilingualModel, "__unlikely_threshold_asyncified"):
    orig_ut = MultilingualModel.unlikely_threshold
    if not inspect.iscoroutinefunction(orig_ut):
        async def unlikely_threshold_async(self, lang): return orig_ut(self, lang)
        MultilingualModel.unlikely_threshold = unlikely_threshold_async
        MultilingualModel.__unlikely_threshold_asyncified = True
# ====================================================================

# Load environment variables from .env
load_dotenv()
SPRING_BOOT_BASE = os.getenv("SPRING_BOOT_API", "http://localhost:8080/api")

async def fetch_last_order(user_id: int):
    url = f"{SPRING_BOOT_BASE}/order-history/user/{user_id}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list) and data:
            return data[0]
        return None

async def fetch_all_orders():
    url = f"{SPRING_BOOT_BASE}/order-history"
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()

def format_order(order: dict) -> str:
    if not order:
        return "I couldn't find any recent orders for you."
    items = ", ".join([item.get("productName", "item") for item in order.get("items", [])])
    status = order.get("status", "unknown")
    total = order.get("total", "unknown")
    order_id = order.get("id", "unknown")
    order_date = order.get("orderDate", "recently")
    return (
        f"Your last order (Order ID: {order_id}) placed on {order_date} "
        f"includes: {items}. Order status is {status}. Total amount is ${total}."
    )

def orders_summary(orders):
    if not orders:
        return "You have no orders on file."
    summary_lines = []
    for order in orders[:5]:
        items = ", ".join(item.get("productName", "item") for item in order.get("items", []))
        line = f"Order ID {order.get('id')}, {order.get('orderDate')}, items: {items}, status: {order.get('status')}."
        summary_lines.append(line)
    return "\n".join(summary_lines)

class Assistant(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are an EVA Customer Support Agent. Answers should be crisp and short."
        )
        self._my_llm = None

    async def on_llm_start(self, llm):
        self._my_llm = llm

    async def on_transcription(self, event, **kwargs):
        text = event.text.lower().strip()
        user_id = 1  # Replace with actual ID retrieval as needed

        if "all my orders" in text or "order summary" in text:
            try:
                orders = await fetch_all_orders()
                print(f"Fetched orders: {orders}")
                context = orders_summary(orders)
                prompt = (
                    "You are the EVA assistant. Use the following real order data to answer any questions about orders. "
                    "NEVER ask the user to log in, and ALWAYS answer from the provided info.\n"
                    f"ORDER DATA:\n{context}\n"
                    f"USER QUESTION: {event.text}\n"
                    "Your answer:"
                )
                print("=== LLM PROMPT ===")
                print(prompt)
                print("==================")
                return await self._my_llm.ask(prompt=prompt)
            except Exception as e:
                print("Error fetching all orders:", e)
                return "I couldn't retrieve the list of all orders right now."

        if "last order" in text or "recent order" in text or "show my last order" in text:
            try:
                order = await fetch_last_order(user_id)
                return format_order(order)
            except Exception as e:
                print("Error fetching last order:", e)
                return "Sorry, I couldn't retrieve your last order details right now."

        # Fallback: LLM
        return None

async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=deepgram.STT(
            model=os.getenv("DEEPGRAM_MODEL"),
            language=os.getenv("DEEPGRAM_LANGUAGE"),
            api_key=os.getenv("DEEPGRAM_API_KEY"),
        ),
        llm=openai.LLM(
            model=os.getenv("OPENAI_MODEL"),
            api_key=os.getenv("OPENAI_API_KEY"),
        ),
        tts=cartesia.TTS(
            model=os.getenv("CARTESIA_MODEL"),
            voice=os.getenv("CARTESIA_VOICE"),
            api_key=os.getenv("CARTESIA_API_KEY"),
        ),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )
    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )
    await ctx.connect()

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
