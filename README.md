## fastapi 패키지 설치
```bash
pip install requirements.txt
uvicorn sql_app.main:app
```

## powershell에서 다음 명령어 실행
```bash
Start-Job { Invoke-WebRequest http://127.0.0.1:8000/sync }
Start-Job { Invoke-WebRequest http://127.0.0.1:8000/sync }
```

<hr/>

## FastAPI의 sync, async 비교
1. 먼저 동기로 작성되었을 때 저렇게 거의 동시에 2개의 요청이 들어오면, `uvicorn`은 저 요청들을 각각의 
   스레드에 할당<br/>때문에 Hello 문구가 처리와 동시에 처리되는 것이 아닌 들어온 요청 2개가 출력됨.<br/><br/>
2. 각각의 스레드로 받은 요청을 스레드 풀로 처리. <br/>
   또한 각각의 요청이 들어온 순서에 따라서 순차적으로 실행.</br>
   때문에 Bye 뒤에 찍히는 스레드 id가 요청이 순차적으로 들어온 순서로 출력됨.<br/> 
   결과적으로 비동기로 처리하는 것 처럼 보여짐.

결국 동기(sync) 방식은 요청이 들어온 개수만큼의 스레드를 스레드풀에 넣고 실행함.


다만 비동기로 작성된 함수는 uvicorn에서 '이벤트 루프'라는 곳에서 실행됨.<br/>
이 이벤트 루프는 요청이 들어오는 것을 '싱글 스레드'로 모아서 처리하고, 싱글 스레드로 동작하기 때문에 이 요청은 비동기로 처리될 수 있음.