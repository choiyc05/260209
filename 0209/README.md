# 0209

 ## 숙제... dockerfile 내 EXPOSE 역할
- dockerfile 구성 요소
  ### Dockerfile 설명
```
FROM        : 기본 대상 이미지를 정의하는 속성
MAINTAINER  : 작성자의 정보를 기록하는 속성
RUN         : FROM의 기반 이미지 위에서 실행될 명령어 정의
COPY        : 도커 컨테이너의 경로로 파일을 복사할 때 사용하는 속성
COPY 로컬:컨테이너
COPY ./index.html:/usr/share/nginx/html/index.html
ENV         : 도커 컨테이너의 환경변수를 정의하는 속성
EXPOSE      : 연결할 포트 번호 정의
ENTRYPOINT  : 도커 컨테이너 생성 후 실행될 명령어 (1회 실행)
CMD         : 도커 컨테이너 시작 이후 실행될 명령어
```
- EXPOSE는 실제로 포트를 개방(Open)하는 기능이 아니라 '문서화'와 '자동화'를 위한 힌트.
```
    EXPOSE가 Dockerfile에 있든 없든, docker run -p 80:8000을 실행하면 도커 엔진은 호스트의 80번 포트와 컨테이너의 8000번 포트를 강제로 연결(Mapping)해 버립니다. 
    실행 시점에 명령어로 내리는 지시가 설계도(EXPOSE)보다 우선순위가 높기 때문입니다.
```
- 컨테이너끼리의 통신
```
동일한 사용자 정의 네트워크(User-defined Network) 안에 있다면: 사실 EXPOSE가 없어도 컨테이너 이름이나 IP를 통해 모든 포트로 서로 통신이 가능합니다. 
(도커가 기본적으로 내부망을 열어주기 때문입니다.)
하지만! EXPOSE는 다른 도구와의 연동에서 빛을 발합니다.

NGINX나 Proxy 서버: "Upstream" 설정을 자동화할 때 EXPOSE된 정보를 읽어와서 자동으로 설정해주는 도구들이 있습니다.
Kubernetes(쿠버네티스): 쿠버네티스의 서비스(Service) 설정에서도 EXPOSE된 포트 정보가 일종의 가이드라인 역할을 합니다.
[아직 잘 모르겠다...]
```

- 자동 포트 매핑 (-P 옵션)
```
docker run을 할 때 포트를 일일이 지정하기 귀찮아서 -P (대문자) 옵션을 주면, Dockerfile에 EXPOSE로 명시된 모든 포트를 호스트의 랜덤한 포트에 자동으로 연결해 줍니다.
```

 ## Postman
```
API 테스트 (Request/Response): 서버에 데이터를 보내고(GET, POST, PUT, DELETE 등), 서버가 돌려주는 응답(성공, 실패, 데이터 내용)을 한눈에 확인할 수 있습니다.
=>
fastapi 스웨거로 대체 가능
```

 ## Authorize and Authorization
 