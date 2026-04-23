# 04. 시트 스키마 설정

이 워크플로우는 **5개 활성 시트**를 중심으로 설계됐습니다. 각 시트는 명확한 용도가 있고, 전용 툴이 최적화돼 있어요.

## 활성 시트 5개

| 시트 | 용도 | 주 컬럼 |
|---|---|---|
| **daily** | 일반 표현·단어·구동사 | date, source, expression, meaning_kr, example1-3, note |
| **corrections** | 내 영어 → 교정 | date, topic, my_version, corrected, reason, pronunciation_tip |
| **pronunciation** | 발음·억양 팁 | date, source, word_or_phrase, phonetic, tip |
| **assertions** | 시험 대비 주장+근거 | unit, assertion, grounds |
| **translation** | 영상 번역 연습 | date, link, timestamp, original, my_try, correct_translation, comment |

## 1. 파일 생성

```bash
cp config/sheets_registry.example.yaml config/sheets_registry.yaml
```

## 2. Spreadsheet ID 찾기

Google Sheets URL 구조:
```
https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit#gid=0
                                       └─── 이 부분 ───┘
```

`sheets_registry.yaml` 의 `spreadsheet_id` 값으로 입력.

## 3. 시트 준비

**옵션 A: 재구성된 엑셀 파일 업로드 (추천)**

제공된 `english_study_restructured.xlsx`를 Google Drive에 업로드 → Google Sheets로 변환. 5개 활성 시트가 모두 올바른 헤더와 함께 준비돼 있어요. 아카이브(`_archive_*`) 시트도 참조용으로 포함.

**옵션 B: 빈 시트에 직접 생성**

Google Sheets에서 각 탭을 만들고 1행에 다음 헤더를 입력:

- **daily**: `date`, `source`, `expression`, `meaning_kr`, `example1`, `example2`, `example3`, `note`
- **corrections**: `date`, `topic`, `my_version`, `corrected`, `reason`, `pronunciation_tip`
- **pronunciation**: `date`, `source`, `word_or_phrase`, `phonetic`, `tip`
- **assertions**: `unit`, `assertion`, `grounds`
- **translation**: `date`, `link`, `timestamp`, `original`, `my_try`, `correct_translation`, `comment`

탭 이름은 `sheets_registry.yaml`의 `tab_name` 값과 **대소문자까지 정확히** 일치해야 합니다.

## 4. registry.yaml 이해하기

스키마 파일의 키 설명:

| 키 | 의미 |
|---|---|
| `spreadsheet_id` | Google Sheets 파일 ID |
| `sheets.<별명>` | Claude가 인식할 시트 별명 |
| `tab_name` | 실제 시트 탭 이름 (대소문자 정확히) |
| `columns[].name` | 내부 정규 이름 |
| `columns[].aliases` | Claude가 다양하게 부를 별칭들 (한국어 가능) |
| `columns[].required` | 비어있으면 저장 시 에러 |
| `columns[].auto_fill: today` | 오늘 날짜 자동 입력 |

### 별칭(alias)의 의미

`example1`의 aliases에 `["example1", "ex1", "예문1"]`이 있으면, Claude가 다음 중 어떤 키로 데이터를 보내도 `example1` 컬럼에 저장됩니다:
- `"example1": "..."`
- `"ex1": "..."`
- `"예문1": "..."`

## 5. 시트 커스터마이즈

### 컬럼 추가
```yaml
# 예: daily에 난이도 컬럼 추가
- name: difficulty
  aliases: ["difficulty", "난이도", "level"]
```
구글 시트에도 같은 이름의 헤더를 추가해야 해요.

### 새 시트 추가
1. Google Sheets에 새 탭 + 1행 헤더
2. `sheets_registry.yaml`에 항목 추가
3. Claude Desktop 재시작 (MCP가 설정 다시 읽음)

### 시트 제거
`sheets_registry.yaml`에서 항목만 빼면 Claude가 접근 안 함. 구글 시트의 실제 탭은 안 지워져요.

## 6. 아카이브 시트 처리

재구성된 엑셀에는 `_archive_` prefix 시트들이 있습니다 (기존 scripts docs, 영단어 등). 이것들은:

- **registry.yaml에 등록하지 않음** → MCP가 수정·삭제 못함
- 참조가 필요하면 사람이 직접 Google Sheets에서 열어서 봄
- 원하면 registry에 읽기 전용 항목으로 추가해서 Claude가 검색만 할 수 있게 확장 가능
