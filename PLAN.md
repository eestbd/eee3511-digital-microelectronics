# PLAN.md

현재 작업: Part 1 과제 요구사항의 최종 대조와 제출 준비. Part 2는 계속 중단한다.
상태: 전기적 8개 spec·필수 수치 검증 PASS. 제출 준비는 학번 및 해당 파일의 OK 화면 확정 전까지 미완료다.

## Goal

최신 과제 PDF의 Part 1 목표·설계 범위·동일 소자 측정·저장 규약·보고서 (a)/(b)/(c)·OK 화면 요구를 실제 산출물과 대조하고, 가능한 미완료 사항을 마무리한다. 계산 완료와 제출 준비 완료를 구분한다.

## Current State

- 공식 모델 최종 후보 #10: W, Lg=0.6 µm, tox=4.75 nm, xj=0.1 µm, tSi=0.5 µm, source/drain=0.5 µm, NA=2e16 / ND=1e19 cm⁻³. 동일 구조에서 8/8 PASS.
- #10/#8 모두 coarse/fine·전류 보존·raw 재추출·fresh live/reload·공식 extended 3종/ramp0.1 검증 PASS. 관련 21 tests와 legacy 3 CLI 회귀 PASS. 과거 10회 탐색·FAIL·HW1은 보존됐다.
- Selected 진단 구조·재현 입력·checker OK와 7쪽 Part 1 보고서 초안이 있다. 보고서에는 checker 텍스트가 있으나 UI OK 화면은 없고 학번도 미확인이다.
- Part 2 중간 코드·raw·checkpoint는 보존했다. 사용자 지시 전까지 실행·추가 구현·탐색하지 않는다.

## Requirements

- PDF의 8개 정확한 bias·온도·단위·정의와 설계 범위를 모두 대조한다.
- 구조는 하나이며 bulk/oxide/gate_metal·gate/source/drain/body·bulk_oxide·bulk.NetDoping·이름 재료를 지킨다. Doping 이후 physics 이전에 저장된 실제 파일을 검사한다.
- 보고서 Part-1-(a): HW1의 부족한 물리, 필요한 이유, 구현, 검증. (b): 초기 설계→시도→지표→판단, 최종 그림·8 spec 표. (c): 한 변수씩 바꾼 metric 영향.
- 실제 학번의 `part1_[학번].devsim`과 해당 self-check OK 화면을 확정한다. 미확정이면 완료로 표시하지 않는다.
- 기존 소자/코드/결과를 불필요하게 변경하지 않는다. 추가 최적화·Part 2는 제외한다.

## Assumptions

- 앞선 “완료”는 계산·검증·초안 정리 완료였다. 이번 작업은 제출 요구까지 모두 충족했는지 따로 점검하는 요청이다.
- PDF의 p+ tap 그림은 예제이며 검사기·Q&A는 별도 tap을 허용하지만 필수 형상을 명시하지 않는다. 기존 bottom body contact를 유지하고 차이를 보고한다.
- 실제 조교 채점기 전체 소스/실행은 제공되지 않았다. 공개된 공식 조건 일치와 실제 채점 통과 보장을 구분한다.
- 학번은 반드시 사용자가 제공해야 한다. 비동기 질문을 보냈으며 답변을 기다리는 동안 독립 문서·검증을 진행한다.

## Plan

- [x] PDF Part 1 목표·설계 범위·제출 슬라이드와 공식 Q&A, 원 코드·결과 직접 대조.
- [x] 요구사항별 근거·완료/미완료 표 작성, 저장 구조·입력·물리 조건 일치 최종 확인.
- [x] 보고서 (a) HW1 대비/필요 이유, (b) 초기 소자·설계 판단, (c) 실제 metric 영향 설명 보강·렌더 검토.
- [ ] 실제 self-check 출력 UI 화면 캡처. 학번 확인 후 제출 이름/최종 checker/해당 화면 확정.
- [x] 전체 diff·보호 hash·로그 prefix·PLAN 일치 검증 및 이번 점검 종료 기록. 제출 이름/OK 화면은 미완료로 남긴다.

## Validation

- 기존 `results/official_20261004_155839/part1/candidate_10/fine/metrics.json`와 `numerical_validation.json`, `saved_geometry_validation.json`, selected config/structure/checker를 대조한다. 시뮬레이션 코드나 소자를 바꾸지 않으므로 전체 TCAD를 재실행하지 않는다.
- Fresh checker는 `.conda/python.exe -B project1/check_structure_file.py <실제 파일>`로 실행하며 출력·returncode·구조 hash를 보존한다.
- 보고서 표를 raw metric과 대조하고 실제 PDF 전 페이지 렌더를 검토한다. UI 화면은 실제 로그 표시 화면만 사용한다.
- `git diff --check`, 기존 HW1/results hash 및 기존 PROGRESS_LOG byte prefix를 확인한다.

## Progress / Discoveries

- 2026-10-04: PDF 실제 목표·허용 범위·제출 규약 페이지 재검토. 전기적 8 spec과 설계 변수 범위는 충족했다. 보고서의 HW1 대비 설명·설계 판단을 더 분명히 하고 실제 학번·OK 화면을 확정해야 제출 준비 완료다.
- 기존 7쪽 초안은 (a)에서 수정 직전 Project 1 구현과 HW1을 충분히 구분하지 않았다. HW1 helper의 고정 ni/n1/p1, 고정 이동도, gate offset 부재를 직접 확인했으며 설명을 보강한다.
- 2026-10-04: `part1/PART1_REQUIREMENTS_AUDIT.md`에 PDF 요구별 근거와 완료 상태를 정리했다. `submission_audit.json`에서 8개 실제 기준, 공식 수치 검증, 최종 구조 hash 및 ablation별 한 변수/같은 sweep을 확인했다. HW1/기존 결과 hash와 이전 로그 prefix도 보존됐다.
- 2026-10-04: 보고서 7쪽을 보강·전 페이지 렌더 검토했다. HW1 대비 물리 필요성·Varshni/ni 식, 초기 Vth/Ion 실패와 시도→판단, 실제 8개 ablation metric·Lg/tox/xj 그림 표시를 추가했다. 소자·실행 코드·raw는 바꾸지 않아 전체 TCAD/test를 반복하지 않았다.
- 2026-10-04: Computer-use로 실제 checker 출력 화면을 준비하려 했으나 `sky.launch_app`에서 `Computer Use app approval timed out`을 반환했다. 승인 없는 UI 작업이나 화면을 가장한 이미지 생성으로 대체하지 않았다. 현재 실제 학번 답변도 미확인이다.

## Final Review

- 완료한 점검: 최신 PDF 목표·허용 범위·저장·제출 조건을 대조했다. 8 spec·설계 범위·동일 구조·물리 조건·구조 규약은 충족한다. 보고서 (a)/(b)/(c)의 설명을 보강했고 전 페이지 렌더를 확인했다.
- 검증: `submission_audit.json`의 8개 기준·공식 수치 판정·구조 hash·3개 one-knob/same-sweep·문서 링크·HW1/results hash·로그 prefix PASS. `git diff --check` PASS. 기존 21 tests·legacy 3 CLI PASS 증거를 사용했다. 이번에 소자/시뮬레이션 코드가 바뀌지 않아 전체 실행을 반복하지 않았다.
- 미완료: 실제 학번의 제출 파일 이름과 그 파일의 OK 화면 보고서 포함. 학번 질문이 pending이며 앱 접근 승인 시간 초과로 UI 캡처도 미완료다. 따라서 `part1_submission_ready=false`를 유지한다.
- 실제 조교 채점기 전체 실행은 미검증이며 공개된 공식 조건의 만족과 채점 보장을 구분한다. 완전한 mesh convergence·coarse NA 경계 ablation 한계도 남긴다.
- 다음: 사용자 학번/실제 화면 확보 후 제출 파일·fresh checker·보고서 화면 포함을 확정한다. 그 전 Part 2로 넘어가지 않으며 완료 후에도 별도 사용자 지시 없이 재개하지 않는다.
