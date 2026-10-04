# PLAN.md

현재 작업: 추가 공식 Q&A 반영 문서의 한글 손상 복구.
상태: 문서 내용을 복원해 UTF-8로 저장하고 확인했다. 실험과 코드·설계 입력 변경은 수행하지 않았다.

## Goal

추가 공식 Q&A를 반영한 PLAN과 최신 PROGRESS_LOG 기록에서 물음표로 손실된 한글을 확인 가능한 원문으로 복구하고, 앞으로 Part 1과 Part 2의 독립 설계 및 허용된 구조·doping 자유도를 정확히 참조할 수 있게 한다.

## Current State

- Part 1 공식 8/8 PASS 결과·입력·구조·source를 보존한다. 제출 준비는 마지막에 한다.
- Part 2 baseline: CSTORE 18.585 fF, 초기 READ 0/1 128.264/84.102 mV, data0 ≥64 ms PASS; data1 약 2.64 ms FAIL. 이번 문서 복구는 전기적 판정을 바꾸지 않는다.
- 현재 capacitor는 source contact 위 metal stem/두 slab 구조다. 추가 공식 답변은 이 배치의 허용성을 확인했다.
- 이전 수정 제안은 gate TaN→W/TiN 비교 후 유망 후보에 capacitor h=0.96 µm 결합이다. 아직 실험하지 않았다.
- 손상본은 ignored project1/tmp/encoding_repair_* 폴더에 원본 bytes로 백업했다. PLAN 전체와 2026-10-04 20:06:40 KST 로그 한 건만 한글 손상이 확인됐다.

## Requirements

- PLAN과 손상된 최신 로그의 한글을 복원한다. 손상되지 않은 과거 로그는 byte 단위로 보존한다.
- 실제 한글 문자와 UTF-8 decoding을 검사한다. 이미 물음표로 손실된 내용은 단순 인코딩 변환으로 복구되지 않으므로 확인 가능한 이전 작성 내용을 사용한다.
- 추가 공식 Q&A 3항을 유지한다: source contact 바로 위 capacitor 배치, 비균일/비대칭 doping, Part 1/2 독립 설계.
- 최종 doping 분포는 bulk.NetDoping에 표현한다. 제출 구조가 미인식 LDDDoping/HaloDoping 등에 의존하지 않게 한다.
- 이번에는 문서만 수정한다. 실험·코드·config·구조·기존 결과·Git staged 상태는 보존한다.
- 복구 사실·범위·원인·검증을 PROGRESS_LOG에 실제 KST 시각으로 기록한다.

## Assumptions

- 사용자의 한글 복구 요청은 손상된 로그 한 건의 본문을 원래 내용으로 바로잡는 것을 포함한다. 시각을 유지하고 손상본 백업과 별도 정정 기록을 남긴다.
- 사용자가 전달한 장이준 조교의 답변을 추가 공식 확인으로 기록한다. 수신 날짜는 2026-10-04이며 원 답변 시각은 알 수 없어 만들어내지 않는다.
- Node 0개 bulk-hk interface 허용은 해당 배치의 구조 확인이다. 실제 접촉하지 않는 영역에 interface를 새로 만들라는 요구는 아니다.
- 비균일/asymmetric profile 허용은 설계 자유도다. 현재 코드가 모든 profile을 지원한다거나 후보가 spec을 통과한다는 의미는 아니다.
- 실험 중 참고하라는 지시는 앞으로의 설계 기준 반영이며 지금 탐색/구현을 시작하라는 승인이 아니다.

## Plan

- [x] 문서 실제 bytes·UTF-8·한글/물음표 분포 조사, 손상 범위 확인.
- [x] 손상본 백업과 문서 외 파일·Git staged 상태 보호 snapshot 확보.
- [x] 확인 가능한 작성 원문으로 PLAN과 최신 로그 본문 복원, UTF-8로 저장.
- [x] Windows 한글 전달 경로의 재발 방지 규칙을 AGENTS에 추가.
- [x] Markdown 문서 인코딩·한글·링크·diff, 과거 로그 prefix와 문서 외 파일 보호 검증 및 최종 기록.

## Validation

- 문서 조사에서 PLAN은 UTF-8로 decoding되지만 한글 0개/물음표 1,052개였다. 최신 로그 한 건도 한글이 물음표로 바뀌었다. AGENTS/OFFICIAL_QA 및 다른 저장소 Markdown에는 연속 물음표/대체문자 손상이 없었다.
- 복구 후 UTF-8 strict decoding·한글 포함·연속 물음표/대체문자 부재를 확인한다. 이전 정상 로그 byte prefix와 최신 원래 timestamp를 보존한다.
- 문서 외 파일의 변경 전 hash와 Git staged name/status를 대조하고 git diff --check 및 로컬 문서 링크를 검사한다.
- 새 실험/test는 실행하지 않는다. 문서 변경이므로 구조 checker나 전체 TCAD를 반복하지 않는다.

## Progress / Discoveries

- 한글 손상은 표시 설정이나 현재 UTF-8 decoding 오류가 아니라 이전 PowerShell→Python stdin 전달 중 문자 치환이었다. 이미 저장된 ?를 다른 encoding으로 읽는 것만으로 원문을 복원할 수 없다.
- 한국어 본문은 UTF-8 파일로 직접 작성하고 Python은 파일 bytes/text를 읽어 사용한다. PowerShell pipeline에 한글 본문을 싣는 경로를 피한다.
- 추가 공식 확인: source contact 전체 윗면 위 capacitor 배치 허용. Checker/naming/storage·plate 연결/plate dQ/dV가 핵심이며 bare n+ 배치나 contact 축소를 강제하지 않는다.
- 추가 공식 확인: 허용 범위 내 위치별 doping·source/drain 비대칭이 가능하고 evaluator는 제출 NetDoping 분포를 그대로 읽는다.
- 추가 공식 확인: Part 1 parameter를 Part 2에 강제하지 않는다. Part 1은 8개 nMOS spec, Part 2는 READ/retention 중심 pass transistor+capacitor co-design이다.
- 후속 실험 선택지가 확대됐지만 이번에는 실험하지 않았다. 기존 gate/cap 제안은 유지하되 필요하면 비균일/비대칭 doping을 검토하고 fresh NetDoping·구조·READ/retention을 검증한다.

## Final Review

- 완료 범위: PLAN과 2026-10-04 20:06:40 KST 로그의 한글을 복원하고 UTF-8로 저장했다. 정상 과거 로그·원래 최신 기록 시각은 보존하고 복구 이력을 append했다.
- 손상본 백업·실제 한글/UTF-8·Markdown 링크·diff·문서 외 파일과 Git staged 상태 보존을 검증했다.
- 추가 공식 Q&A의 구조·NetDoping·독립 설계 기준을 유지했다. 코드/설계 입력 변경이나 실험은 수행하지 않았다.
- 남은 목표: 이후 요청에서 Part 2 후보 설계·실행·전체 조건 검증. 문서 복구나 구조 허용 확인만으로 data1 retention FAIL을 PASS로 바꾸지 않는다.
- 다음 작업: 실험 시작 요청을 기다린다. Part 1을 보존하면서 Part 2 고유 조건과 추가 설계 자유도를 적용한다.
