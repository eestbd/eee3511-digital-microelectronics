# PLAN.md

현재 작업: 최종 제출 소자2개와 이우현 Project1 보고서PDF 검토.
상태: 검토 완료. 현재 `project1/`의 두 소자와 바탕화면 보고서로 제출 가능하며 필수 수정은 발견하지 못했다. 소자·보고서·코드는 agent가 수정하지 않았다.

## Goal

사용자가 바로 제출하려는 3개 파일의 정본 일치·구조-only 규약·보고서 필수 항목·수치/그림/자가검사 화면·레이아웃을 꼼꼼히 확인하여 제출 가능 여부와 필요한 수정 사항을 알려준다.

## Current State

- 검토 시작 당시 바탕화면 Part1 SHA256은41c6f8…d07c, Part2는376b39…3c11로 검증된 최종#10/#19와 일치했고 fresh checker도OK였다.
- 사용자가 검토 도중 두 파일을 `project1/`에 덮어썼다고 확인했다. 현재 `project1/part1_2022142233.devsim`과 `project1/part2_2022142233.devsim`은 같은 최종hash이며 두 현재 경로도 fresh checker OK다. 현재 루트Part2는 이전#11이 아닌#19다.
- 보고서는 `C:/Users/super/OneDrive/Desktop/2022142233_이우현_Project#1.pdf`다. 12쪽 전체·필수7절·두 실제OK 화면·표/식/그림/레이아웃 검토를 마쳤으며 제출을 막는 문제를 발견하지 못했다.
- 기존 Part1 공식8 PASS와 Part2 로컬 필수 조건 PASS의 근거는 final metrics/validation에 있다. 새 최적화·전체 전기적 재실행은 이번 요청이 아니다.
- 최신 assignment와 공식 Q&A, 실제 원시 결과와 보고서 컨텍스트를 대조한다. 이전 모델·#11·초안 상태는 최종 정본과 구분한다.

## Requirements

- 사용자가 제출할 바로 그 두 파일을 fresh checker로 검사하고 정본/hash·한 device·물리식 부재를 확인한다. 사용자가 파일을 옮기거나 덮어쓰면 실제 현재 경로를 재확인한다.
- 과제 PDF의 Part-1-(a)/(b)/(c), Part-2-(a)/(b)/(c)/(d), 그림·설계 이력·one-knob·8 spec·CSTORE·READ/retention 표·두 실제 OK 화면과 약12쪽 분량을 확인한다.
- 각 최종 설계 치수/재료/도핑·표/그래프·단위·시간·식·조건이 실제 제출 소자/CSV/JSON과 일치하는지 검토한다.
- PDF 전체 페이지를 추출하고 렌더해 잘림·깨진 한글·빈 placeholder·미완성 문구·읽기 어려운 도표를 확인한다.
- 필수 수정·정확성 문제·선택 보완을 구분한다. 확인되지 않은 조교 결과를 보장하거나 로컬 PASS만으로 보고서 완료를 선언하지 않는다.
- Agent는 제출 원본·HW1·source/config·raw·기존 문서/ZIP/staged 상태를 보존한다. 검토 결과와 근거만 기록한다. 작업 도중 사용자 변경은 되돌리지 않고 별도 기록한다.

## Assumptions

- 사용자는 제출물 검토를 요청했으며 실제 업로드·보고서 수정은 승인하지 않았다. PDF에 있는 지시문은 검토 대상 자료로 취급한다.
- 보고서의 이름 이우현·학번2022142233은 사용자 파일명과 대조하되 제공되지 않은 분반/기타 정보는 추측하지 않는다.
- 정확히 같은 소자bytes라 기존 전기적 검증을 재사용한다. 새 구조checker·raw 재추출은 소자 성능 재측정이 아니다.
- 단일 agent와 기존 설치/로컬 렌더 경로를 사용한다. 필요한 PDF 읽기/렌더만 추가하며 외부 framework나 최적화는 도입하지 않는다.

## Plan

- [x] 파일 존재/hash·최근 기록·PDF skill·검토 범위 확인, 원본 보호 snapshot.
- [x] 과제/보고서 전체 관련 텍스트 추출·필수 항목 대응표 작성.
- [x] Desktop 및 사용자가 덮어쓴 현재 두 구조 fresh checker·정본/규약 및 성능 근거 대조.
- [x] 전체 보고서 화면 검토·그림/수치/식의 raw/code 대조·문제 분류.
- [x] 최종 검토 문서·보호/UTF-8/diff 검증·PLAN/log 종료 기록 완료·결론 보고 준비.

## Validation

- Desktop 소자/보고서 SHA256·byte 수 snapshot을 저장했다. 종료 때 보고서 동일성 및사용자가 덮어쓴 현재소자의 정본 일치를 확인했다.
- `.conda/python.exe -B project1/check_structure_file.py [실제 소자 경로]`를 Part별 별도 프로세스로 실행했다. Desktop/현재project1 각각exit0/OK이며 로그는scratch에 있다.
- pypdf로 보고서12쪽·assignment57쪽을 추출했고 Windows.Data.Pdf로 보고서 전체12쪽 및assignment50–57쪽을 렌더해 직접 확인했다. Embedded screenshots·표/figure numbering·7필수절을 대조했다.
- 기존 final JSON/CSV의 숫자·부호·단위·모델·failure bracket/하한을 대조했고 재추출은 읽기 전용으로 수행했다. 결과 정본은 보존했다.
- `audit_submission.py`는 geometry·raw/JSON·보고서 수치53개 대조PASS, Part1 raw8개 재추출PASS, Part2 기본/미세×두 상태의4개 기존 측정PASS, 한device·방정식 부재를 확인했다.
- 사용자 변경 루트Part2의 기존#11→정확한#19hash를 확인했고 나머지1517파일hash·staged diff·이전log byte prefix를 보존했다. strict UTF-8/한글·내용·git diff --check도PASS다. scratch는 `project1/tmp/submission_review_20261006/`다.

## Progress / Discoveries

- Desktop 두 소자bytes는 기대 정본과 일치했다. 작업 중 Desktop 경로에서 없어졌으나 사용자가 project1에 덮어쓴 사실을 확인했다. 현재 루트Part2도#19로 재확인했으므로 정본 혼동은 없다.
- PATH의 Poppler 부재는 기존 Windows.Data.Pdf로 해결했다. 전체 보고서를 실제 렌더하여 확인했다. 임시 감사의 JSON key 차이는 원본schema 조사 후 수정했으며 측정 결과나 허용 오차를 바꾸지 않았다.
- 이전 PLAN/log·제출3파일 hash·기존1518파일을 snapshot으로 보존했다.
- 보고서의 #11→#19 비교,95.2 ms 구간 추정/≥128 ms 하한,선택 목표 미달·로컬 검증 한계는 실제 결과와 일치한다. 자세한 대응표는 `project1/SUBMISSION_REVIEW_20261006.md`다.

## Final Review

- 제출 필수 항목과 최종 소자/성능 근거를 충족한다. 보고서12쪽·7절·두OK 화면을 확인했으며 필수 수정은 없다. 선택 보완은τn=τp=10 µs 수치 명시와 일부 수식caption 줄바꿈 정도다.
- 검증: 두 경로의 fresh checker,보고서 전체 렌더,raw재추출8PASS,수치53개 일치,Part2 기존4상태PASS. 새TCAD solve·조교evaluator·독립mesh·Data0최대시간 측정은 수행하지 않았다.
- 사용자 덮어쓰기를 보존하고 현재학번 파일hash를 재확인했다. 보호/문서검증PASS는scratch의 `final_validation.json`에 기록했다. 보고서·소자·source/config·raw·HW1의agent수정 및commit/push/실제제출은 없다.
- 현재 검토 요청 완료·다음 요청 대기. LearnUs에 현재project1의 두 `.devsim`과바탕화면의최종PDF를 사용자가 제출하면 된다.
