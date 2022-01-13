# **CAMP IN** 

hanghae99-ClassD-5team

<hr>

## **`✨프로젝트 소개`**


### Camping -> Camp Ing -> 🎉Camp In

Camp In이 제공하는 캠핑장의 위치와 정보를 확인하고, 게시판을 통해 정보를 교환하고 소통할 수 있습니다.

<hr>

## **`📽시연 영상`**
[📽유튜브📽](https://www.youtube.com/watch?v=Ggcz0dUmzeo)

<hr>

## **`👨‍💻프로젝트 기간`**
`2022/01/10 ~ 2022/01/13`

<hr>

## **`🔨기술 스택`**
- beautifulsoup4
- Jinja2
- JWT(Json Web Token)
- Flask
- MongoDB
- AWS EC2

<hr>

## **`💎WireFrame`**
![와이어프레임](https://user-images.githubusercontent.com/76610357/149290958-ad06d8a3-4b4d-4547-9d50-eccbb59ac709.PNG)

<hr>

## **`🎮주요 기능`**
- `캠핑장 정보`
  - 한국관광공사의 GoCamping사이트를 크롤링 하여 지역별로 캠핑장의 정보를 db에 저장하여 필요한 정보를 보여줍니다.
- `게시판 기능`
  - 게시판의 글은 모든 사람이 볼 수 있으나 로그인이 안되면 글쓰기 기능은 사용 불가능합니다.
- `회원가입/로그인 기능`
  - jwt방식을 이용하여 토큰을 쿠키에 저장하여 사용합니다.

<hr>

## **`📜요구사항`**
- `Serverside Rendering`
  - `장점` : 사용자가 보는 첫 페이지 로딩이 빨라집니다. 또한 HTML에 모든 컨텐츠가 담겨있기 때문에 SEO(검색엔진 최적화)에 효율적입니다.
  - `단점` : TTV(Time To View)와 TTI(Time To Interact)사이의 간격이 CSR(ClentSide Rendering)보다 큰것이 단점이며, 사용자가 상호작용시 서버에서 다시 전부 다운 받아 오기 때문에 서버 과부화되기가 쉽다는 단점도 있습니다.

- `JWT(Json Web Token)`
  - 인증에 필요한 정보들을 암호화시킨 토큰으로 인증하는 방식입니다.
  - 별도의 저장소가 필요한 `쿠키/세션`방식에 대비하여 별도의 저장소 관리가 불필요하며, 발급한 후 검증만 하면 되기 때문에 상태를 저장할 필요 없는 서버를 만드는 입장에서 확장, 유지, 보수 하는데 효율적이다는 장점이 있습니다.
  
<hr>

## **`🌠Trouble Shooting`**
1. 각자 기능 구현 후 합치면서 css가 통일이 안되어 있어서 ui가 불편함 -> 기능을 구현후 합치고나서 회의를 통해 css를 수정함
2. `repository`에 `push`, `pull`이 안되는 문제가 발생 -> 원격 저장소의 주소를 로컬저장소에 http 또는 ssh를 통해 등록하여 해결

