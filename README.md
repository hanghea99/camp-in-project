# CAMP IN 

hanghae99-ClassD-5team

<hr>

## `✨프로젝트 소개`


###`Camping -> Camp ing -> 🎉camp in`

Camp In이 제공하는 캠핑장의 위치와 정보를 확인하고, 게시판을 통해 정보를 교환하고 소통할 수 있습니다.

<hr>

##`🔨기술 스택`
- beautifulsoup4
- Jinja2
- JWT(Json Web Token)
- Flask
- MongoDB
- AWS EC2

<hr>

## `🎮주요 기능`
- `캠핑장 정보`
  - 한국관광공사의 GoCamping사이트를 크롤링 하여 지역별로 캠핑장의 정보를 db에 저장하여 필요한 정보를 보여줍니다.
- `게시판 기능`
  - 게시판의 글은 모든 사람이 볼 수 있으나 로그인이 안되면 글쓰기 기능은 사용 불가능합니다.
- `회원가입/로그인 기능`
  - jwt방식을 이용하여 토큰을 쿠키에 저장하여 사용합니다.

<hr>

## `📜요구사항`
- Serverside Rendering
  - `장점` : 사용자가 보는 첫 페이지 로딩이 빨라집니다. 또한 HTML에 모든 컨텐츠가 담겨있기 때문에 SEO(검색엔진 최적화)에 효율적입니다.
  - `단점` : TTV(Time To View)와 TTI(Time To Interact)사이의 간격이 CSR(ClentSide Rendering)보다 큰것이 단점이며, 사용자가 상호작용시 서버에서 다시 전부 다운 받아 오기 때문에 서버 과부화되기가 쉽다는 단점도 있습니다.
- JWT
