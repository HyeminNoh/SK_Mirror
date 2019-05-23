#구동확인 테스트 코드
import main

def test_index():
    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/')
    assert r.status_code == 200

    r = client.get('/static/main.css')
    assert r.status_code == 200