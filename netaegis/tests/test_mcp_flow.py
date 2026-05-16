from fastapi.testclient import TestClient
from server.main_mcp.app import app as main_app
from server.operational_mcp.app import app as op_app


def test_auth_login_and_me():
    main = TestClient(main_app)
    ok = main.post('/api/auth/login', json={'username':'admin','password':'admin'})
    assert ok.status_code == 200
    assert ok.json()['access_token']
    me = main.get('/api/auth/me')
    assert me.status_code == 200


def test_websocket_live_echo():
    main = TestClient(main_app)
    with main.websocket_connect('/ws/live') as ws:
        first = ws.receive_json()
        assert first['type'] == 'welcome'
        ws.send_text('ping')
        echo = ws.receive_json()
        assert echo['type'] == 'echo'


def test_main_sync_creates_incident_with_actions():
    main = TestClient(main_app)
    resp = main.post('/api/op/sync', json={'source_mcp': 'op-1', 'events': [{'type':'failed_login','payload':{'ip':'1.1.1.1','count':7}}]})
    assert resp.status_code == 200
    incidents = main.get('/api/incidents/').json()
    assert incidents[-1]["severity"] == "high"


def test_incident_acknowledge_flow():
    main = TestClient(main_app)
    main.post('/api/op/sync', json={'source_mcp': 'op-1', 'events': [{'type':'http_5xx','payload':{'status':'503'}}]})
    incidents = main.get('/api/incidents/').json()
    incident_id = incidents[-1]["id"]
    ack = main.post(f'/api/incidents/{incident_id}/acknowledge')
    assert ack.json()["ok"] is True


def test_operational_agent_endpoints_and_registry():
    op = TestClient(op_app)
    assert op.post('/api/agents/metrics', json={'agent_id':'netpulse-1','name':'cpu_percent','value':25.0}).status_code == 200
    assert op.post('/api/agents/heartbeat', json={'agent_id':'netpulse-1','name':'NetPulse Agent'}).status_code == 200
    agents = op.get('/api/agents/').json()
    assert 'netpulse-1' in agents


def test_main_actions_queue_and_health():
    main = TestClient(main_app)
    enqueue = main.post('/api/actions/enqueue', json={'source_mcp':'op-1','target':'fw-1','action_type':'block_ip','params':{'ip':'9.9.9.9'}})
    assert enqueue.status_code == 200
    actions = main.get('/api/actions/').json()
    assert len(actions) >= 1
    health = main.get('/api/realtime/health').json()
    assert health['main_mcp'] == 'ok'


def test_predictions_and_status_endpoints():
    main = TestClient(main_app)
    op = TestClient(op_app)
    pred = main.get('/api/predictions/incidents')
    assert pred.status_code == 200
    assert 'forecast' in pred.json()
    status = op.get('/api/status/')
    assert status.status_code == 200
    assert 'node_id' in status.json()


def test_policies_recommendations_and_buffer():
    main = TestClient(main_app)
    op = TestClient(op_app)

    p = main.post('/api/policies/', json={
        'name': 'block-bruteforce',
        'enabled': True,
        'conditions': {'type': 'failed_login', 'count_gte': 5},
        'actions': [{'action_type': 'block_ip'}],
    })
    assert p.status_code == 200
    assert len(main.get('/api/policies/').json()) >= 1

    main.post('/api/op/sync', json={'source_mcp':'op-1','events':[{'type':'failed_login','payload':{'ip':'6.6.6.6','count':6}}]})
    recs = main.get('/api/recommendations/').json()
    assert len(recs) >= 1

    buffer_resp = op.get('/api/buffer')
    assert buffer_resp.status_code == 200
    assert 'events_buffered' in buffer_resp.json()
