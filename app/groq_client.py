import asyncio
from langchain_groq import ChatGroq
from app.models import Address

class GroqClient:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.0,
            max_retries=2
        )
        self.llm = self.llm.with_structured_output(Address)

    async def struct_address(self, address):
        messages=[
                ("system", "Transform the address of the person to JSON format with fields: name, street, house_number, postcode, city and voivodeship. Your response should only contain the JSON."),
                ("human", address)
        ]

        ai_msg = await self.llm.ainvoke(messages)
        return ai_msg
