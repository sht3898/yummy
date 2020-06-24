# Sub PJT II 상세 기능 명세서

## BackEnd

### Req 1. 데이터 마이그레이션

* 한국관광공사 DB 작업
  * 공공 API를 이용하여 관광지 정보 확장

### Req 2. 웹 서비스 기능

* 여행 플랜 저장 기능 구현
  * 여행 플랜 스키마 구성
  * api 구현
* 여행 플랜 조회 기능 구현
  * api 구현

### Req 3. 웹서비스 유저 기능 구현

* 타 유저의 여행 플랜 조회 기능 구현
  * 타유저의 여행 플랜 조회 구현
  * 타 유저의 여행 플랜을 기반으로 유저의 새 플랜 작성 기능 구현

### Req 4. 유저 기능 구현

* 유저 수정/ 삭제 기능 구현
  * 유저 수정 기능 구현
  * 회원 탈퇴 기능 구현
* 소셜 로그인 구현
  * 구글 로그인 구현
  * 네이버 로그인 구현

### Req 5. KNN 알고리즘 구현

* KNN 알고리즘 학습 및 구현
  * 협업 필터링 추천 시스템 개발
  * User-Base 방식 구현
  * RMSE(Root Mean Square Error) 등 지표로 검증

### Req 6. TF-IDF 알고리즘 학습 및 구현

* TF-IDF(Term Frequency-Invese Document Frequency) 알고리즘 학습 및 구현
  * TF-IDF 알고리즘 이론적 학습
  * TF-IDF알고리즘을 적용하여 음식점 정보 벡터화
* KoNLPy를 이용한 TF-IDF 알고리즘 성능 향상
  * 한글 문장 형태소를 분석하기 위해 KoNLPy라이브러리 사용법 학습
  * KoNLPy를 이용하여 음식점 정보를 형태소 단위로 분해하고, 분해한 결과를 TF-IDF 알고리즘에 적용하여 TF-IDF 알고리즘 성능 향상

### Req 7. K-means 알고리즘 구현

* K-means 알고리즘의 이론적 내용 학습 및 구현
  * K-means 알고리즘의 이론적인 내용 학습
  * TF-IDF 알고리즘을 통해 벡터화된 음식점에 K-means알고리즘 적용 및 군집화

### Req 8. 컨텐츠 기반 필터링 추천 시스템 구현

* 유사 음식점 추천 기능 구현
  * 군집화된 음식점 목록을 사용하여, 특정 음식점에 대하여 유사한 음식점을 추천
* 하이브리드 추천 시스템 구현
  * User-base 추천 시스템과 Contents-base 추천 시스템을 적절한 방식으로 혼합해 하나의 알고리즘만을 사용할 때보다 더 성능이 좋은 추천 시스템 구현

### Req 9. 웹 서비스 배포

* 구현한 코드를 AWS에 배포하여 외부에서 사용할 수 있도록 함



## FrontEnd

### Req 1. 헤더 구현

* 로고 제작
  * 팀 이름을 바탕으로 로고 제작
* 로그인 폼 상세화
  * 사용자가 잘못된 요청을 하기 전 오류를 미리 파악 할 수 있게 구현
  * 사용자의 잘못된 요청시 오류 사항을 파악 할 수 있게 구현
  * 사용자의 올바른 요청시 이후 행동 구체화

### Req 2. 여행계획 작성 페이지 구현

* 검색을 통한 여행지 선택 구현
  * 검색을 통해 여행계획을 추가 할 수 있도록 구현
  * 여행계획 추가시 출발일, 머무는 날짜 구성할 수 있도록 구현
* 작성 완료 버튼 구현
  * 여행계획 완료시 여행계획 저장 구현
  * 여행계획 저장완료 후 여행계획 상세 페이지로 넘어 갈 수 있도록 구현

### Req 3. 여행계획 상세 구성 페이지 구현

* 저장 기능 구현
  * 여행계획을 저장할 수 있도록 구현
* 스케줄 추가 기능 구현
  * 상세 여행 계획 스케줄을 추가할 수 있도록 구현
* 스케줄 편집 기능 구현
  * 상세 여행계획 스케줄을 편집할 수 있도록 구현
* 여행계확 수정 기능 구현
  * 여행계획을 추가/삭제/수정할 수 있도록 여행계획 페이지로 돌아갈 수 있도록 구현

### Req 4. 유저 정보 페이지 구현

* 유저 정보 확인 기능 구현
  * 로그인된 유저 본인에 대해 자신의 정보를 볼 수 있는 기능 구현
* 유저 정보 편집 기능 구현
  * 로그인 된 유저 본인에 대해 자신의 정보를 수정할 수 있는 기능 구현
  * 정보 편집 전 비밀번호 확인 절차 갖도록 구성

### Req 5. 여행지 상세 페이지 구현

* 여행지 상세 정보 확인 기능 구현
  * 해당 여행지의 상세 정보 확인

### Req 6. 웹 서비스 배포

* 구현한 코드를 AWS에 배포하여 외부에서 사용할 수 있도록 함
* 프론트엔트 코드는 정적 파일로 빌드하여 사용하여야 함


