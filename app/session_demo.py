import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from app.agent import root_agent


load_dotenv()

APP_NAME = "banking_servicing_app"
USER_ID = "demo_user"
SESSION_ID = "demo_session"


async def run_turn(
    runner: Runner,
    message: str,
) -> None:
    user_message = Content(
        role="user",
        parts=[Part(text=message)],
    )

    print(f"\nUser: {message}")

    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print("Agent:")
                print(event.content.parts[0].text)


async def main():
    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    print("Initial state:")
    print(session.state)

    await run_turn(
        runner,
        "I'm a business customer.",
    )

    await run_turn(
        runner,
        "What KYC documents do I need?",
    )

    updated_session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    print("\nFinal session state:")
    print(updated_session.state)

    print("\nNumber of stored events:")
    print(len(updated_session.events))

    print("\nStored events:")

    for index, event in enumerate(updated_session.events, start=1):
        print(f"\n--- Event {index} ---")
        print(f"Author: {getattr(event, 'author', None)}")
        print(f"Content: {getattr(event, 'content', None)}")
        print(f"Actions: {getattr(event, 'actions', None)}")


if __name__ == "__main__":
    asyncio.run(main())