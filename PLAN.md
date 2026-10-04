# PLAN.md

현재 작업: Project 1 PDF 기준 Part 1·2 구현 및 완료 상태 검토.
상태: 검토 완료. 두 Part의 핵심 구현·로컬 설계 조건 PASS, 과제 전체 제출 준비 미완료. 설계/parameter/physics는 변경하지 않았다.

## Goal

Part 1과 Part 2가 과제에서 요구하는 구현·설계 조건·검증·보고서·제출물까지 완료됐는지 확인하고, 충족/미완료/미검증을 근거와 함께 구분한다.

## Current State

- Part 1 공식 모델 최종 #10은 8/8 specs PASS 및 numerical validation PASS로 기록돼 있다. 선택 구조는 `results/official_20261004_155839/part1/selected/part1_selected_diagnostic.devsim`이다.
- Part 2 최종 #11은 READ0/1=127.320/67.301 mV, 양 상태 retention≥64 ms, CSTORE19.824 fF, 전계5/3.333 MV/cm. 기본/미세 raw 검증과 학번 구조 checker PASS다.
- 학번은2022142233. Part 2 제출명 구조는 있고, Part 1 제출 준비는 이전 사용자 지시로 마지막에 하도록 유보했다.
- Part 1 학번 파일은 없고 Part 2 학번 파일은 있다. 현재 PDF는 학번 미확인의7쪽 Part 1 초안이며 Part 2 최종 section·구조/전류/READ 그림·두 학번 파일의 실제 OK 화면을 포함한 최종 PDF가 필요하다.
- 상세 판정과 다음 제출 준비 순서는 `project1/PART1_PART2_COMPLETION_AUDIT.md`에 기록했다. 이번 검토는 완료됐지만 제출 준비를 수행한 것은 아니다.

## Requirements

- 최신 `Project1_Assignment_0927.pdf`의 Part 1·2와 저장·naming·보고서·제출 요구사항을 직접 읽는다.
- 추가 공식 Q&A의 구조/모델/정밀도/설계 자유도를 함께 적용하고 PDF 그림을 필수 형상으로 오인하지 않는다.
- 실제 source/최종 config·raw CSV·metrics·validation·저장 구조 hash로 이전 PASS 주장을 대조한다.
- 최종 구조를 fresh checker로 다시 읽고 필수 명명·재료·도핑·구조만 저장됐는지 점검한다.
- 리뷰 요청을 신규 최적화/feature/제출 준비/Part 1 변경으로 확대하지 않는다. 문서와 scratch 검토 자료만 작성한다.

## Assumptions

- 측정과 physics source hash가 그대로라면 비싼 전체 TCAD를 반복하지 않고 기존 raw를 독립 재검토한다. 문제가 발견되면 재현 범위를 정하고 PLAN에 기록한다.
- 전기적 조건 통과와 보고서/제출 준비 완료는 별도로 판정한다. TA evaluator 전체 재실행을 로컬 checker와 동일시하지 않는다.
- 정확한 최대 retention이 아닌≥64 ms 관측 하한은 최소 조건 충족 근거다. 추가 점수/여유 여부는 따로 설명한다.

## Plan

- [x] 현재 규칙·PLAN·최근 log와 최종 선택 기록 확인, 보호 snapshot 준비.
- [x] PDF 관련 페이지의 표·식·그림·제출 checklist 및 공식 Q&A 대조.
- [x] Part 1/2 source·measurement·raw/간격·저장 구조/geometry 검토.
- [x] 보고서 각 section·도표·학번 파일·실제 checker 화면 준비 여부 확인.
- [x] 상세 audit 문서, 최종 PLAN/log, 보호·한글·diff 검증 및 완료 상태 정리.

## Validation

- PDF 전체57쪽에서 관련40~57쪽을 추출하고 관련 한국어 페이지를 시각 검토한다. 기존 readable pypdf와 Windows PDF renderer를 사용하며 환경을 재설치하지 않는다.
- Part 1의 `candidate_10/fine/metrics.json`·numerical validation·raw CSV·선택 구조 hash와 source를 대조한다.
- Part 2의 `combined_final/combined_fine`와 원 checkpoint/provenance·raw CSV·최종 구조·validation을 대조한다.
- root `.conda/python.exe -B project1/check_structure_file.py <선택/학번 구조>`를 각각 새 프로세스에서 실행해 stdout/stderr/exit code를 새 scratch 폴더에 보존한다.
- 보고서 PDF/소자 파일 inventory, Part-1-(a)~(c)·Part-2-(a)~(d), 구조/READ·current 그래프·spec 표·OK 화면 요구사항을 실제 확인한다.
- 작업 시작 snapshot 대비 기존 source/소자/config/결과/PDF hash·staged 상태·log prefix, UTF-8 실제 한글과 `git diff --check`를 확인한다.
- 실제 새 실행: `.conda/python.exe -B project1/tmp/completion_review_20261004/verify_review.py` PASS. 두 fresh checker OK, Part 1 독립 raw8항목·Part 2 기본/미세 raw 적분·전류/전하·plate dQ/dV·provenance·source/구조 hash PASS. Part 2 NetDoping2,142노드와 singleton/equation 부재 PASS.
- 같은 scratch의 `part1_geometry.py` fresh reload PASS: singleton/equation 부재·Lg/tox·접점 위치·NetDoping2,340노드. 이전 numerical validation의 공식 채점 조건 PASS를 확인했다. 전체 TCAD/unit/GUI는 변경된 실행 코드가 없어 반복하지 않았다.
- PDF는57쪽 전체 추출, 관련50~57쪽 시각 검토와 현재 Part 1 초안1/4/7쪽 fresh render를 대조했다. source/report PDF를 수정·재출력하지 않았다.

## Progress / Discoveries

- 기존 Part 1 audit는 spec/설계/수치 검증 완료와 학번 이름·실제 OK 화면 미완료를 구분했다. 현재 학번은 확인됐으므로 실제 제출명 파일 존재 여부를 재점검한다.
- 기존 Part 2 최종 data1의64 ms 마진은60.417968/60.420969 mV로 여유가 작다. 원 순차 실행과 독립 상태 종합 결과를 구분해 검토한다.
- 확인: 학번 파일 준비·최종 보고서·실제 OK 화면이 남은 필수 항목이다. Part 2 전류 raw는 있지만 최종 I(t) 그림은 아직 없다. 최종 구조 그림은 실제 bottom p+ tap을 표시해야 한다.
- Part 2의 원 순차 실행 종료 후 동일 조건 상태별 완료 결과를 종합한 provenance와 원 데이터를 확인했다. 독립 wrapper는 공통 source 외 추가 hash 및 일부 조건만 기록하므로 metadata 전체 dict 동일성을 가정하지 않고 공통 필수 조건·추가 hash·실제 함수를 대조했다. 감사 helper의 과도한 동일성 가정을 수정했고 소자/측정 실패는 발견되지 않았다.
- Part 1 실행 source는 그대로다. 넓게 수집한 hash 목록의 미사용 cell.py만 이후 Part 2 개발로 달라진다. 선택적 double 미실행에 따른 all_checks_pass=false를 공식 extended 채점 조건 실패로 오인하지 않는다.
- PDF의 실제 과제는 Part 1/2이며 뒤의3~6은 설명 슬라이드 장 번호다. 64 ms 이상은 최소 조건 충족 하한이고 최초 실패 시각/추가 점수·조교 evaluator·mesh 민감도는 미검증이다.

## Final Review

- 요청된 원문 대조·구현/결과 검토 완료. 추가 구현이나 parameter 수정이 필요한 필수 누락은 이번 검토에서 발견되지 않았다. 제출 준비 누락을 성능 PASS와 별도로 명시했다.
- 기존 Part 1/HW1·source·config·소자·raw·PDF를 보존하고 검토 문서/PLAN/append log 및 새 ignored scratch만 작성했다. Commit/push·실제 제출·재최적화는 하지 않았다.
- 남은 한계: data1 최소 마진 여유 약0.418 mV, retention≥64 ms 하한, 독립 mesh/조교 전체 재평가 미검증. Part 1 제출명·통합 보고서·실제 두 OK 화면은 후속 제출 준비 범위다.
- 최종 보호587개 파일 hash·staged 상태·기존 log byte prefix·새 기록 날짜 순서·실제 UTF-8 한글·audit 링크·diff check PASS. 2026-10-04 21:39:10 KST 최종 log를 append했다. 검토 요청 완료·다음 요청 대기다.
