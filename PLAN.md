# PLAN.md

현재 작업: Project 1 폴더의 불필요한 HW1 복사본 정리
상태: 완료 — 17개 삭제, 최상위 파일 26→10개, 기능·원본 보호 검증 통과
최종 갱신: 2026-10-04 (Asia/Seoul)

## Goal

`project1/`에서 현재 구현에 사용하지 않는 HW1 예제·launcher·옛 생성 결과를 삭제해 주요 파일을 쉽게 찾도록 한다. 실제 simulator·측정·검증 경로와 기존 실험 증거는 유지한다.

## Current State

- project1 바로 아래 파일은 작업 전 26개에서 새 README를 포함해 10개가 됐다. 현재 Part 1 진입점은 `part1.py`, `part1_experiment.py`, `validate_part1.py`, `check_structure_file.py`다. 일반 I–V/C–V CLI `mosfet.py`도 보존했다.
- `mosfet_tool/`의 config/simulator/physics/materials/metrics/workflows가 실제 구현이며 필요한 코드다. HW1에서 이어진 파일이라는 이유로 삭제하지 않는다.
- 현재 진입점·tests가 읽거나 import하지 않는 비교 스크립트 2개·직접 실행 예제 1개·STEP2 launcher 3개·옛 CSV 5개·HTML 6개, 총 17개를 삭제했다.
- 해당 17개는 모두 tracked이고 staged/unstaged 수정이 없어 Git으로 복구 가능하다. 약 27.85 MiB이며 일부는 HW1과 byte 동일하다.
- `results/part1_baseline/`와 `results/part1_search_20261004/`는 측정·실패·검증 근거이므로 보존한다. 두 선정 후보의 extended 검증은 통과했지만 double 전체 검증 실패는 여전히 미해결이다.
- 이전 작업의 미커밋 변경이 존재한다. 시작의 visible 파일 289개 hash·로그 prefix·원래 YAML과 top-level 파일 개수는 `project1/tmp/cleanup_20261004/start_snapshot.json`에 확보했다.

## Requirements

- 삭제 대상은 project1의 확인된 미사용 파일 17개에 한정한다. HW1·과제 PDF·실험 raw/JSON/devsim/log·tests·현재 구현은 유지한다.
- 장치 기본값·실제 sweep 조건·CLI mode·API·전류/정전용량 단위를 변경하지 않는다. 삭제된 비교 예제 전용 YAML `compare`와 stale 문서 참조만 정리한다.
- 사용자 승인 없이 기존 미커밋 변경을 취소하거나 commit/push하지 않는다.
- 추가 모델 변경·새 실험·double 문제 수정·Part 2 feature·새 의존성/인프라는 수행하지 않는다.
- 짧은 project1 README에 남은 구조, 기본 실행 명령, 결과 위치와 현재 검증 한계를 안내한다.
- PLAN을 갱신하고 PROGRESS_LOG에 실제 KST의 milestone·검증·최종 종료 기록을 append한다.

## Assumptions

- 사용자 요청의 “필요없는 파일”은 실제 개발·검증 경로에서 쓰지 않는 HW1용 예제와 재생성 가능한 옛 출력으로 해석한다.
- `run_example.py`의 기능은 HW1 reference와 현재 part1/workflows에 남아 있으므로 project1 복사본을 삭제한다.
- `STEP2_RUN.bat`은 현재 CLI를 호출하지만 실행 편의 wrapper일 뿐이다. STEP2 명칭 혼란을 줄이기 위해 삭제하고 README에 실제 interpreter 명령을 제공한다.
- 보존하는 결과 파일이 많아도 재현·double 원인 조사에 필요한 증거다. 사용자 요청을 실험 이력 삭제로 확대하지 않는다.
- config.py/mosfet.py의 변경은 삭제된 파일 이름을 언급한 주석/docstring뿐이며 계산 동작은 보존한다.

## Plan

- [x] M1 — AGENTS/최근 PLAN·log·dirty 상태·파일 목록·import·문서·Git 복구 가능성 조사, 보호 snapshot.
- [x] M2 — project1의 미사용 파일 17개 삭제, 오래된 compare 설정·참조 정리.
- [x] M3 — project1 README와 AGENTS의 구조·실행 안내 갱신.
- [x] M4 — device/sweeps 의미 동일성, imports/help, 20개 tests, 기존 CLI 3종 회귀.
- [x] M5 — 전체 diff·삭제 목록·원본/실험 보호 hash·append-only 확인, 최종 상태·종료 기록.

## Validation

- 삭제 전 각 target의 절대 경로가 project1 내부의 실제 file인지 확인하고 `Remove-Item -LiteralPath`로 개별 삭제한다. 디렉터리·reparse point·wildcard·recursive 삭제는 사용하지 않는다.
- Git staged/unstaged diff가 없는 17개만 삭제한다. 현재 계산 경로에 해당 모듈 import 또는 옛 출력 read가 없음을 확인했다.
- 시작 YAML과 정리 YAML의 device/sweeps parsed 값을 비교하고 load_config의 반환 Device/sweeps도 확인한다. 실제 계산 조건을 바꾸지 않는다.
- 준비한 `.conda\python.exe`와 DLL PATH로 남은 imports/4개 CLI help, `-m unittest discover -s project1/tests -v` 실행.
- `mosfet.py idvg/idvd/cv --config <absolute config>`를 별도 scratch에서 실행한다. 기존 baseline legacy CSV와 21/21/31점·열·bias·유한값·I–V 수치를 비교한다. C–V 마지막 자리 변동은 원래 기록의 2~3 ULP 반복 사례와 구분해 보존한다.
- 계산 코드·구조가 바뀌지 않아 10회 설계 탐색·fine/probe 전체를 재실행하지 않는다. 기존 double 실패도 해결됐다고 기록하지 않는다.
- 시작 snapshot에서 의도한 삭제·문서·compare cleanup 외 파일 hash 일치, 특히 HW1/results/part1.py/experiment/tests 보존 확인. 이전 PROGRESS_LOG byte prefix·KST 순서와 정상 UTF-8 추가 기록 확인.
- `git diff --check`, docs의 현재 파일·실행 명령·삭제 참조 확인.
- 실제 결과: 20개 unittest exit 0, 5개 imports·4개 help 통과, 기본 CLI 3종 exit 0. 21/21/31점의 열·bias·유한값과 I–V 기존 오차 기준 통과, C–V bit-exact 일치.
- `project1/tmp/cleanup_20261004/check_cleanup.py` 검사 통과: 대상 17개만 삭제, protected snapshot 파일 266개 hash 일치, 현재 YAML 의미 보존, README 링크·활성 참조·Python 구문·PLAN section·로그 prefix/KST 순서 정상. 결과는 같은 scratch의 `cleanup_validation.json`에 있다.
- EOF 빈 줄 수정 후 `git diff --check` exit 0. 문서·빈 줄 변경 뒤 전체 TCAD/설계 탐색을 불필요하게 반복하지 않았다.

## Progress / Discoveries

- 삭제 후보: `compare_models.py`, `compare_tcad.py`, `run_example.py`, `STEP2_COMPARE.bat`, `STEP2_COMPARE_MODELS.bat`, `STEP2_RUN.bat`; 옛 결과 `compare_gate_length.html`, `compare_gate_length_log.html`, `compare_models.csv`, `compare_models.html`, `compare_models_log.html`, `compare_tcad.csv`, `cv.csv`, `cv.html`, `idvd.csv`, `idvd.html`, `idvg.csv`.
- compare_models는 현재 없는 루트 step1을 import하는 과거 HW1 예제다. Compare YAML은 해당 비교 스크립트만 읽고 일반 CLI/Part 1은 사용하지 않는다.
- AGENTS·mosfet.py docstring·config.py 주석·config.yaml에 삭제 예정 파일 참조가 있어 정리 시 함께 갱신한다.
- 이번 작업 전에 기록됐던 로그 인코딩 손상은 기존 정정 기록과 함께 그대로 보존하며, 이번 한국어 문서 작성은 UTF-8 apply_patch 경로를 사용한다.
- 17개 삭제 뒤 최상위 파일은 새 README를 포함해 10개다. 제거한 compare 외 parsed YAML과 load_config의 Device/sweeps가 같고, config.py/mosfet.py의 구현 AST도 동일하다(docstring 제외).
- 5개 entrypoint import·4개 help·20개 tests 통과. 기본 CLI idvg/idvd/cv exit 0, 21/21/31점·열·bias·유한값 일치. I–V 차이는 기존 허용 오차 이내(max 1.8635e-20/2.7105e-20 A/µm), 이번 C–V는 bit-exact 일치다.
- diff 검사에서 compare block 삭제로 남은 YAML 끝 빈 줄을 발견해 제거했다. 설정 값은 그대로다. 계산 코드가 바뀌지 않아 전체 10회 설계/precision 재실행은 하지 않았다.

## Final Review

- 사용자 요청의 미사용 파일 정리 완료: 17개 삭제, 최상위 파일 26→10개, README·AGENTS에서 현재 역할과 실행 경로 안내.
- 소자·sweep 값과 계산 구현 유지. 삭제 예제의 `compare` 블록 및 stale 주석/docstring만 정리했다. 테스트·3종 CLI·imports/help·문서/diff 검증 통과.
- HW1·과제 PDF·baseline·10회 탐색·원시 측정/실패 로그·기존 미커밋 구현은 protected 266개 hash로 보존 확인했다. 삭제 대상도 Git으로 복구 가능하다.
- 과거 source hash는 원래 실행 증거로 보존했다. 이번 설명/설정 정리 뒤의 파일 hash가 다르더라도 당시 결과를 현재 source hash로 덮어쓰지 않는다.
- Double 수렴·전류 보존 문제는 미해결 상태 그대로다. 이 정리의 실행 검증 통과를 설계 전체 검증 PASS로 확대하지 않는다.
- 새 feature·의존성·framework·multi-agent·보고서·commit/push 없음. PLAN과 최종 KST 로그가 일치하며 기존 로그 prefix를 보존했다. 현재 요청 완료, 다음 요청 대기.
