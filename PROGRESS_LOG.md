# PROGRESS_LOG.md

이 저장소의 의미 있는 작업 이력을 시간순으로 누적하는 append-only log다. 현재 목표·계획·상태는 `PLAN.md`, 기본 작업 규칙은 `AGENTS.md`에서 관리한다.

시간대: Asia/Seoul (KST, UTC+9).
기록 표제: `## YYYY-MM-DD HH:mm:ss KST`.
기존 기록을 수정·삭제·덮어쓰거나 재정렬하지 않는다. 정정은 대상 기록의 시각과 이유를 포함한 새 기록으로 남긴다.

## 2026-10-04 00:49:58 KST

### 수행한 작업

- M1: 기존 AGENTS·PLAN, Git 상태와 누적 로그 유무를 확인했다.
- 현재 요청의 목표·요구사항·가정·milestone·validation으로 PLAN을 갱신하고 PROGRESS_LOG를 초기화했다.

### 현재 상태

- 조사와 계획 수립이 완료되었다. 기존 코드·설정·결과·reference 77개 파일의 SHA-256 기준값을 확보했다.
- 이번 변경 범위는 PROGRESS_LOG 생성과 AGENTS·PLAN의 문서 갱신이다. Logging 규칙 연결과 최종 validation은 남아 있다.

### 발견 / 이슈

- 기존 누적 로그는 없었다. 이전 작업의 정확한 시각을 알 수 없어 로그는 이번 요청부터 기록한다.
- 기록 시각은 조회한 UTC 현재 시각을 명시적으로 UTC+9로 변환한다.

### 다음 작업

- AGENTS에 기록 trigger·필수 항목·KST·append-only·최종 기록과 PLAN 동기화 규칙을 추가한다.
- 구현 완료 기록을 append한 뒤 형식·이전 내용 보존·변경 범위를 검증한다.

## 2026-10-04 00:51:07 KST

### 수행한 작업

- M2: PROGRESS_LOG를 생성하고 AGENTS의 기본 workflow·PLAN 운영·최종 review에 progress logging을 연결했다.
- Append-only 보존, KST 기록, 네 가지 필수 section, 중요한 검증·계획 변경 이유, 정정과 최종 기록 규칙을 추가했다.

### 현재 상태

- M1 조사·계획과 M2 logging 문서 연결이 완료되었다.
- PLAN의 현재 요청·요구사항·가정·milestone을 갱신했다. 실제 project feature·환경·참조 코드는 변경하지 않았다.

### 발견 / 이슈

- 과거 기록의 당시 상태는 보존하고 최신 기록과 PLAN의 현재 상태를 비교해야 한다.
- 문서만 변경하므로 TCAD·GUI·CLI·구조 checker는 이번에 재실행하지 않는다. 형식·append 보존·변경 범위 검증은 다음 milestone에서 수행한다.

### 다음 작업

- 모든 기록의 필수 항목과 KST 시간순서를 검증한다.
- 기존 기록의 byte prefix, 보호 파일 77개의 해시, 문서 diff와 PLAN 동기화를 검토한 뒤 최종 종료 기록을 append한다.

## 2026-10-04 00:53:34 KST

### 수행한 작업

- M3 완료: 기록 형식·KST 시간순서·append-only 보존·문서 상태·변경 범위를 검증하고 전체 문서 diff를 review했다.
- PLAN의 milestone·발견·Final Review를 실제 완료 상태로 갱신하고 이 종료 기록을 추가했다.

### 현재 상태

- 이번 요청 완료: PROGRESS_LOG 생성, AGENTS의 progress logging 규칙, PLAN의 역할·동기화 규칙을 모두 반영했다.
- PLAN의 M1/M2/M3는 완료 상태다. 기존 프로젝트 파일 77개의 SHA-256은 동일하며 변경 범위는 세 루트 Markdown 문서다.

### 발견 / 이슈

- 문서 validation 통과: PLAN 8개 필수 section, workflow 15단계, UTF-8·code fence, 기록별 네 필수 항목, UTC+9 변환·시간순서, 기존 기록 byte prefix 보존, diff·Git whitespace 검사.
- 이번 요청의 계획 방향 변경이나 새로운 blocking 이슈는 없다. 과거 기록의 당시 진행 상태는 그대로 보존한다.
- 기능 변경이 없어 TCAD·GUI·CLI·구조 checker는 이번 요청에서 재실행하지 않았다. 기존 launcher 경로·물리 모델·미구현 spec 한계는 이번 범위 밖으로 남아 있다.

### 다음 작업

- 현재 요청을 완료했으며 다음 요청을 대기한다.
- 다음 non-trivial task에서 PLAN을 새 목표에 맞게 갱신하고, 의미 있는 사건마다 기존 로그를 보존하여 아래에 추가한다.

## 2026-10-04 00:55:04 KST

### 수행한 작업

- 종료 기록 이후 최종 validation의 Git 종료 코드 판정 원인을 조사하고 검증 방법을 보완했다.
- 정상 LF 입력과 trailing-space 입력의 Git 결과를 비교한 뒤 세 문서의 whitespace 검사를 다시 수행했다.

### 현재 상태

- 이번 요청은 완료 상태다. 세 문서의 whitespace 검사와 PLAN·로그 형식·시각·기존 파일 보존 검증이 통과했다.
- PLAN에 원인과 검사 기준을 반영했고, 기존 로그는 수정 없이 보존했다.

### 발견 / 이슈

- 2026-10-04 00:53:34 KST 기록의 validation 결과에 검사 방법을 보완한다. Git `--no-index` 종료 코드 1은 차이를 뜻하며 whitespace 오류가 없을 때도 나온다. 이를 오류로 처리한 검증 스크립트가 원인이었다.
- 재현 결과 정상 입력은 코드 1·진단 없음, trailing-space 입력은 코드 3·오류 진단이었다. 세 문서는 코드 1·진단 없음으로 통과했다.
- 변경 이유는 검증의 잘못된 실패 판정을 바로잡기 위해서다. 구현이나 계획 방향의 변경, 새로운 프로젝트 버그는 없다.

### 다음 작업

- 현재 요청의 최종 validation과 종료 기록을 완료했으며 다음 요청을 대기한다.

## 2026-10-04 01:02:12 KST

### 수행한 작업

- Project 1 Part 1 분석 M1/M2: 과제 PDF와 config·simulator·workflows·구조 checker, 설치된 DEVSIM physics helper를 읽어 대조했다.
- PDF 실제 41/42·50/51쪽의 영문/국문 요구사항과 45~48·54~57쪽의 제출 규칙을 확인했다. 핵심 표·구조도·checker 예시를 렌더 이미지로 검토했다.
- PLAN을 이번 분석 요청에 맞게 갱신하고 기존 source/config/PDF·결과물의 해시 기준과 이전 로그 byte를 확보했다.

### 현재 상태

- M1 원문 요구사항과 M2 구현 격차 조사가 완료되었다. 현재는 작업 순서와 검증 기준을 정리하고 있으며 기능 구현·설계 탐색은 수행하지 않았다.
- Part 1 목표는 같은 소자로 8개 spec을 만족시키고 물리 보완·검증, 탐색 과정, 단일 변수 영향과 최종 구조를 보고하는 것이다.

### 발견 / 이슈

- gate 재료·일함수, 물리 등록 전 구조-only 저장, 8개 spec evaluator가 없다. 온도 입력만으로 n_i/n1/p1의 온도 의존성이 구현되는 것은 아니다.
- PDF는 표면 p+ body tap을 설명하지만 현재는 bulk 아랫면의 이상적 ohmic body 접점이다. Checker 통과가 접점 가정·physics·spec 검증을 대신하지 않는다.
- Mesh 변경이 도핑 감쇠 길이도 바꾸며 조교 physics의 상세 모델·허용 오차는 저장소에 없다.
- 기존 scratch PDF reader의 sandbox 접근 제한은 허용된 로컬 읽기로 해결했다. 프로젝트 환경이나 의존성을 변경하지 않았다.

### 다음 작업

- 의존관계에 따라 제출 구조·physics 검증·measurement·baseline·설계 탐색·최종 검증·보고서 순서를 정리한다.
- 수치·단위·과제 규약을 재검토하고 기존 파일·append-only·문서 상태를 검증한 뒤 분석 완료 기록을 남긴다.

## 2026-10-04 01:05:09 KST

### 수행한 작업

- Project 1 Part 1 분석 M3 완료: 8개 spec·설계 범위·gate 재료·제출 규약을 대조하고 현재 코드의 격차와 향후 9단계 작업 순서·완료 기준을 정리했다.
- PLAN의 요구사항·가정·발견·최종 review를 갱신했다. PDF의 핵심 표·그림 확인 후 이번에 만든 임시 PNG 57개를 제거했다.

### 현재 상태

- 사용자 요청인 Part 1 분석과 순서 정리는 완료했다. 구현·설계 탐색·최종 소자 선정·spec 판정은 수행하지 않았다.
- 변경은 PLAN 갱신과 PROGRESS_LOG append뿐이다. Tracked 파일 66개와 AGENTS의 SHA-256은 동일하며 기존 code/config/PDF/HW1·결과·환경은 그대로다.

### 발견 / 이슈

- 과제는 같은 구조·도핑·gate 재료의 8항목 검증, physics 보완·검증, 시도→지표→판단의 탐색 기록, 단일 변수 영향과 최종 구조를 요구한다.
- 구조 checker 통과와 전기적 합격은 별도다. 저장은 doping 이후·physics 이전이고 gate 재료 이름을 구조에 포함해야 한다.
- Validation 결과: PDF 추출·시각 대조, 원문과 코드/helper/checker 대조, PLAN 8개 section·8개 spec·9단계·UTF-8·diff·Git whitespace·변경 범위·해시·이전 log byte 보존 검증 통과.
- TA physics·추출 세부 방식·허용 오차와 실제 학번은 미확인이다. body tap/ohmic 가정과 mesh-doping 결합도 후속 구현에서 검토해야 한다. 분석 범위에 따라 simulation·checker·parameter 탐색은 실행하지 않았다.

### 다음 작업

- 현재 분석 요청을 완료했으며 다음 요청을 대기한다.
- 후속 구현 요청 시 요구사항/기준 보존→제출 구조→physics 검증→measurement→baseline→설계 탐색→최종 검증→저장 구조 재검증→보고서 순서로 계획을 구체화한다.
