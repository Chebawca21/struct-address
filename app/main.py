from fastapi import FastAPI, BackgroundTasks
from app.models import Process, Status, Address
from app.groq_client import GroqClient
import asyncio

app = FastAPI()
groq = GroqClient()


processes = {}

async def ask_llm(address, uuid):
    process = processes[uuid]
    process.address = await groq.struct_address(address)
    process.status = Status.done
    processes[uuid] = process


@app.post("/struct")
async def struct_address(adr: str, background_tasks: BackgroundTasks):
    id = len(processes)
    process = Process(uuid=id, status=Status.pending)
    processes[id] = process
    background_tasks.add_task(ask_llm, adr, id)
    return {"adr": adr, "uuid": id}

@app.get("/result/{uuid}")
def read_result(uuid: int):
    if uuid in processes:
        return {"uuid": uuid,
                "status": processes[uuid].status,
                "imie_nazwisko": processes[uuid].address.name,
                "ulica": processes[uuid].address.street,
                "numer_domu": processes[uuid].address.house_number,
                "kod_pocztowy": processes[uuid].address.postcode,
                "miasto": processes[uuid].address.city,
                "wojewodztwo": processes[uuid].address.voivodeship
                }
    else:
        return {"uuid": uuid,
                "status": Status.unknown,
                "imie_nazwisko": None,
                "ulica": None,
                "numer_domu": None,
                "kod_pocztowy": None,
                "miasto": None,
                "wojewodztwo": None
                }