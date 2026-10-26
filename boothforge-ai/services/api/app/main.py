import os, uuid, json
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI(title='BOOTHFORGE AI API', version='0.1.0')
app.add_middleware(CORSMiddleware, allow_origins=os.getenv('CORS_ORIGINS','http://localhost:3000').split(','), allow_methods=['*'], allow_headers=['*'])
DATA = Path(os.getenv('DATA_DIR','/tmp/boothforge'))
DATA.mkdir(parents=True, exist_ok=True)
PROJECTS = DATA/'projects.json'

def load():
    return json.loads(PROJECTS.read_text()) if PROJECTS.exists() else {}
def save(data):
    temp=PROJECTS.with_suffix('.tmp'); temp.write_text(json.dumps(data,ensure_ascii=False,indent=2)); temp.replace(PROJECTS)

class Requirements(BaseModel):
    reception: int = Field(default=1,ge=0,le=20)
    screens: int = Field(default=1,ge=0,le=50)
    meeting_rooms: int = Field(default=0,ge=0,le=20)
    storage: bool = False
    notes: str = Field(default='',max_length=4000)
class ProjectIn(BaseModel):
    name: str = Field(min_length=2,max_length=120)
    client: str = Field(min_length=2,max_length=120)
    industry: str = Field(min_length=2,max_length=120)
    length_m: float = Field(gt=0,le=100)
    width_m: float = Field(gt=0,le=100)
    height_m: float = Field(gt=0,le=20)
    open_sides: int = Field(ge=1,le=4)
    requirements: Requirements = Field(default_factory=Requirements)
class GenerateRequest(BaseModel):
    count: Literal[3,6]
    provider: Literal['openai','google','mixed']='mixed'

@app.get('/health')
def health(): return {'status':'ok','version':'0.1.0'}
@app.get('/projects')
def list_projects(): return list(load().values())
@app.post('/projects',status_code=201)
def create_project(payload:ProjectIn):
    db=load(); project={'id':str(uuid.uuid4()),**payload.model_dump(),'area_m2':round(payload.length_m*payload.width_m,2),'status':'draft','concepts':[],'brand':None,'created_at':datetime.now(timezone.utc).isoformat()}; db[project['id']]=project;save(db);return project
@app.get('/projects/{project_id}')
def get_project(project_id:str):
    project=load().get(project_id)
    if not project: raise HTTPException(404,'Project not found')
    return project
@app.post('/projects/{project_id}/brand')
async def upload_brand(project_id:str,file:UploadFile=File(...)):
    db=load()
    if project_id not in db: raise HTTPException(404,'Project not found')
    allowed={'image/png','image/jpeg','image/svg+xml','application/pdf'}
    if file.content_type not in allowed: raise HTTPException(415,'Unsupported brand file')
    content=await file.read(5*1024*1024+1)
    if len(content)>5*1024*1024: raise HTTPException(413,'Maximum 5 MB')
    folder=DATA/'uploads'/project_id;folder.mkdir(parents=True,exist_ok=True)
    suffix={'image/png':'.png','image/jpeg':'.jpg','image/svg+xml':'.svg','application/pdf':'.pdf'}[file.content_type]
    path=folder/f'{uuid.uuid4()}{suffix}';path.write_bytes(content)
    db[project_id]['brand']={'filename':file.filename,'stored_as':path.name,'mime':file.content_type,'analysis_status':'pending'};save(db)
    return db[project_id]['brand']
@app.post('/projects/{project_id}/concepts')
def generate(project_id:str, request:GenerateRequest):
    db=load()
    if project_id not in db: raise HTTPException(404,'Project not found')
    # No fake images: providers are deliberately disabled until authenticated adapters are configured.
    raise HTTPException(501,detail={'code':'AI_PROVIDER_NOT_CONFIGURED','message':'Image generation requires a verified provider adapter and API credentials. No concepts were generated.','requested':request.model_dump()})
