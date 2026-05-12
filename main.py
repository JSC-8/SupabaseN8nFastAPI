from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

app = FastAPI(title="Lead-O-Matic API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
# Conexión a Supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.post("/nuevo-lead/")
async def crear_lead(nombre: str, email: str, empresa: str = None):
    data = {"nombre": nombre, "email": email, "empresa": empresa}
    
    # Insertar en Supabase
    response = supabase.table("leads").insert(data).execute()
    
    if len(response.data) == 0:
        raise HTTPException(status_code=400, detail="Error al guardar el lead")
        
    return {"status": "success", "lead_id": response.data[0]['id']}