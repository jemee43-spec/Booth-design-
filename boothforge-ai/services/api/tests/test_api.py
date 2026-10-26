import os, tempfile
os.environ['DATA_DIR']=tempfile.mkdtemp()
from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_project_lifecycle():
    payload={'name':'Mahaseel Expo','client':'Mahaseel','industry':'Agriculture','length_m':8,'width_m':6,'height_m':4,'open_sides':2}
    r=client.post('/projects',json=payload)
    assert r.status_code==201
    assert r.json()['area_m2']==48
    pid=r.json()['id']
    assert client.get(f'/projects/{pid}').status_code==200
    assert client.post(f'/projects/{pid}/concepts',json={'count':3}).status_code==501
