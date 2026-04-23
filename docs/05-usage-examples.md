# 05. 사용 예시

8개 툴 × 5개 활성 시트 조합의 실제 대화 예시.

---

## 🟢 기본 표현 학습 (daily 시트)

```
나: "pick someone's brain 이 표현 뭐야?"

Claude: "누군가의 뇌를 집어든다"는 아니고, 어떤 분야에 밝은 사람에게
조언·아이디어를 얻고 싶다는 정중한 표현이에요. 캐주얼하면서도 프로페셔널.

예문:
1. Can I pick your brain about the new marketing strategy?
2. I'd love to pick your brain over coffee sometime.
3. He picked my brain for an hour about startup fundraising.

비슷한 표현: "get your input on", "tap into your expertise"

나: "daily에 정리해줘"

Claude: [search_expressions로 중복 체크 → add_expression]
✅ daily 시트 111행에 추가했어요.
  • expression: pick someone's brain
  • meaning_kr: (조언을) 얻어내다, 머리를 빌리다
  • example1-3: (3개 모두 저장)
  • note: 정중하고 캐주얼. 조언 요청 시.
  • date: 2026-04-22
```

---

## 🟡 영어 교정 (corrections 시트)

`correct_expression` 전용 툴이 한 번에 4개 컬럼을 채워줍니다.

```
나: "이 문장 자연스러워? 'I should write the paper more specifically 
so I can 기준을 수립하다'"

Claude: 자연스러운 교정:
"I need to be more specific in my paper so I can establish the criteria."

바뀐 포인트:
- should → need to (의무감 약화, 자연스러움)
- write ~ specifically → be more specific in ~ (관용적)
- 기준을 수립하다 → establish the criteria

발음 팁: "Es-tab-lish"의 'tab'에 강세 주세요.

나: "저장해줘"

Claude: [correct_expression 호출]
✅ corrections 시트 19행에 교정 저장.
  • Before: I should write the paper more specifically so I can 기준을 수립하다
  • After:  I need to be more specific in my paper so I can establish the criteria
  • 이유: should→need to, establish the criteria 사용
```

---

## 🔵 발음 전용 (pronunciation 시트)

```
나: "won't와 want 발음 차이 알려줘"

Claude: [설명...] 
won't: /woʊnt/ - (으)워운트, o 장모음
want: /wɑːnt/ - 워언트, a 소리

팁: won't는 t 직전에 숨을 끊어서 "워운-" 느낌.

나: "pronunciation 시트에 정리해줘"

Claude: [add_expression with sheet='pronunciation']
✅ pronunciation 시트 5행에 추가.
```

---

## 🟣 Assertion + Grounds (assertions 시트)

시험 대비용 주장과 근거 저장.

```
나: "Unit 3.1 Risk Management에 대해 assertion 하나 만들어줘"

Claude: Assertion: "Risk management cannot predict genuinely novel risks, 
as demonstrated by the Millennium Bridge wobble."

Grounds:
- The Millennium Bridge's side-to-side sway was unprecedented in suspension bridge history
- Engineers had a risk register but "bridge wobble" wasn't on it
- ...

나: "assertions 시트에 저장"

Claude: [add_expression with sheet='assertions']
✅ assertions 시트 101행에 추가.
```

---

## 🟠 번역 연습 (translation 시트)

`add_translation_row` 전용 툴 사용.

```
나: "이 영상 구간 번역 연습할게. URL: youtube.com/watch?v=XXX, 
00:05:30, 영어: 'I'm thinking back to who I was at the time.' 
내 번역: '당시 내가 누구였는지 생각하면'"

Claude: 자연스러운 번역: "당시의 저를 떠올려 보면"

차이:
- "누구였는지" → "저를" (관계대명사 풀어쓰기보다 명사로)
- "생각하면" → "떠올려 보면" (thinking back의 회상 뉘앙스 살림)

나: "translation 시트에 기록해줘"

Claude: [add_translation_row]
✅ translation 시트 168행에 번역 기록 저장.
```

---

## ✏️ 기존 행 수정 (update_expression)

```
나: "방금 저장한 pick someone's brain 행에 예문 하나 더 추가해줘. 
'Mind if I pick your brain for a second?'"

Claude: [update_expression with find_by_column='expression', 
         find_by_value='pick someone's brain',
         updates={'note': '추가 예문: Mind if I pick your brain for a second?'}]
         
✅ daily 시트 111행 업데이트.
  • note: 정중하고 캐주얼... | 추가 예문: Mind if I pick your brain...
```

> 💡 **팁**: example1~3 슬롯이 이미 차있으면 Claude는 note에 합쳐요. 
> 원하면 "example3을 이걸로 바꿔줘" 라고 지정 가능.

---

## 📊 주간 복습 (weekly_review)

```
나: "이번 주 뭐 배웠어?"

Claude: [weekly_review(days=7) 호출 → raw 데이터 받음 → Claude가 직접 분석]

📊 지난 7일 학습 요약

총 학습량:
- daily: 15개 표현
- corrections: 3건 교정
- pronunciation: 2건

🎯 반복 패턴 포착:
비즈니스 관련 표현이 집중적(8/15). 특히 **정중한 요청** 표현이 많음:
"pick someone's brain", "circle back", "touch base"

💡 이번 주 가장 유용한 표현 Top 3:
1. pick someone's brain - 조언 요청에 즉시 쓸 수 있음
2. get the ball rolling - 미팅 시작 시 유용
3. circle back - 후속 논의 예고

⚠️ 약한 영역 (교정 기록에서):
'기준을 수립하다'류 한국어를 영어로 옮길 때 어색함. 
'establish the criteria', 'set the standard' 같은 관용구 암기 필요.

🔍 다음 주 추천: formal 표현이 부족함. 이메일/회의 표현 집중 학습 권장.

나: "좋아, 그 Top 3로 퀴즈 내줘"

Claude: [quiz_random 호출 대신 직접 weekly_review 데이터로 퀴즈 구성]
한국어 뜻만 볼게요. 영어 표현 맞춰보세요:
1. (조언을) 얻어내다, 머리를 빌리다
2. 일단 시작하다, 착수하다
3. (대화로) 확인해보다
```

---

## 🔍 중복 확인 + 조회

```
나: "beat around the bush 이미 있어?"

Claude: [search_expressions(sheet='daily', query='beat around')]
네, daily 시트 12행에 있어요:
  • meaning: 빙 둘러 말하다, 핵심 회피
  • example1: Stop beating around the bush...
  • date: 2026-03-15
```

```
나: "daily 시트 최근 5개 보여줘"

Claude: [search_expressions(sheet='daily', limit=5, query=None)]
최근 5개:
1. pick someone's brain (111행, 2026-04-22)
2. circle back (110행, 2026-04-21)
...
```

---

## 🗂 시트 구조 조회

```
나: "내 시트 뭐뭐 있어?"

Claude: [list_sheets]
등록된 활성 시트 5개:
- daily (110행): 일반 학습
- corrections (18행): 교정
- pronunciation (4행): 발음
- assertions (100행): 시험용
- translation (167행): 번역
```

---

## 💡 조합 활용 팁

### 한 대화에서 여러 시트 활용
```
나: "circle back 알려주고, 내 문장도 교정해줘: 
'I will circle back you tomorrow'"

Claude: [설명 + 교정]
circle back의 의미는... [설명]
교정: "I'll circle back with you tomorrow." (전치사 with 필요)

나: "circle back은 daily에, 내 문장 교정은 corrections에 각각 저장해줘"

Claude: [add_expression + correct_expression 연속 호출]
✅ 둘 다 저장 완료.
```

### 주간 복습 후 다음 목표 설정
```
나: "이번 주 복습해주고, 다음 주 공부 방향 추천해줘"
→ weekly_review로 데이터 → Claude가 약점 분석 → 다음 주 학습 플랜 제시
```
