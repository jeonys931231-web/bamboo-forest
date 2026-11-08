/*
  피부관리사 대나무숲 설정 파일

  Firebase 콘솔 → 설정 → 프로젝트 설정 → 일반 → 내 앱(웹 앱)에 보이는
  firebaseConfig 값이에요. databaseURL이 꼭 들어 있어야 해요.

  이 값들은 원래 누구에게나 보이는 공개용 값이라 깃허브에 올려도 괜찮아요.
  실제 보호는 Firebase에 붙여 넣은 보안 규칙(database.rules.json)이 맡아요.

  apiKey가 비어 있으면 숲은 '혼자 걷기' 모드로 열려요.
*/
window.FOREST_CONFIG = {
  firebase: {
    apiKey: "AIzaSyDhUnEDEXQqLKzMIhn7QUQOKQiD1qMnWdk",
    authDomain: "bamboo-forest-300d1.firebaseapp.com",
    databaseURL: "https://bamboo-forest-300d1-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "bamboo-forest-300d1",
    appId: "1:669334021176:web:ae22ef177ad199e82332cd"
  },
  // 숲 이름(영문 소문자·숫자·-). 바꾸면 완전히 따로 노는 숲이 돼요. 예: "test"
  room: "main",
  // 숲 하나에 들어가는 사람 수. 꽉 차면 다음 사람은 '숲 2', '숲 3'…으로 안내돼요(숲은 8개까지).
  cap: 25,
  // 계절. "auto"면 날짜대로: 11~2월 눈 내리는 겨울 숲, 11~12월에는 트리·눈사람·캐롤까지.
  // 고정하려면 "christmas"(트리까지), "winter"(눈만), "off"(사계절 기본 숲) 중 하나로 바꿔요.
  season: "auto"
};
