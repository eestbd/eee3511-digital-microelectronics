# PLAN.md

현재 작업: 2026-10-06 수신 추가 공식 Q&A와 최종 Part1·Part2 구현 대조.
상태: 완료. 추가 Q&A와 부합하며 코드·소자 재설계가 필요한 불일치는 발견되지 않았다. 최종 소자·physics·과거 결과·HW1은 보존했다.

## Goal

사용자가 보낸 capacitor separation·ohmic contact·SRH 수명·Vg sweep·전체 길이 답변을 실제 코드/최종 입력/저장 구조/원시 결과와 대조하여 변경 필요 여부를 판단한다.

## Current State

- Part1 공식 최종 #10은 fine0.01 V 측정에서 8 PASS. Part2 최종 #19는 로컬 필수 조건 PASS, data1/cell estimate95.198837 ms다.
- 최종 파일은 `project1/part1_2022142233.devsim`과 robust run의 `selected/part2_2022142233.devsim`이다. 루트 Part2는 이전 #11이다.
- 기존 코드에서 DEVSIM simple_physics의 silicon 접점을 재사용한다. 실제 SRH 수명은 helper 기본값인10 µs이며 온도별 변경이 없음을 확인했다.
- Part2 입력과 실제 저장 좌표에서 bottom clearance0.05 µm/dielectric4 nm, Lg0.3/source0.2/drain0.2 µm 및 storage=source 연결을 대조했다.
- 직전 보고서 컨텍스트 작업은 완료됐다. 이번 요청은 추가 Q&A 대조이며 보고서 제작·새 최적화로 확대하지 않는다.

## Requirements

- Source/drain/body ohmic boundary의 실제 호출과 식을 확인한다.
- τn=τp=1e−5 s(10 µs)가300/398 K 모두 사용되는지 확인한다.
- Si–hk separation과 dielectric thickness를 구분하고 storage=source·비접촉 계면 부재를 확인한다. 조교의 ‘테스트 가능’ 답변을 모든 separation의 무조건 허용으로 확대하지 않는다.
- Vg measurement sweep와 bias ramp를 구분한다. 0.1 V보다 세밀한 간격은 허용되지만 추출값이 완전히 같다고 단정하지 않는다.
- 전체 길이 변경 자유와 개별 Lg/W/S/D 제한을 구분한다.
- 새 확인은 OFFICIAL_QA/PLAN/log에 남긴다. 코드·소자·원래 JSON/CSV·HW1·기존 자료 ZIP은 변경하지 않는다.

## Assumptions

- 수신일은2026-10-06이며 인용 대화의 실제 날짜는 제공되지 않았다. 18:38/18:52/18:53은 제공된 답변 시각으로만 기록한다.
- 사용자가 붙여넣은 교수/조교 답변을 공식 Q&A 근거로 취급한다. 실제 전체 평가기는 확보되지 않았다.
- 새 DC/READ/retention을 실행하지 않는다. 필요하면 저장 구조의 physics 등록 후 parameter/boundary만 확인하고 기존 raw의0.1 V 표본으로 추출 민감도를 비교한다.

## Plan

- [x] 최근 PLAN/log·새 Q&A·관련 코드/최종 입력 조사.
- [x] 실제 contact/SRH parameter·저장 좌표/도핑/구조-only 확인.
- [x] Part1 fine raw의0.1 V 표본 재추출과 최종 설계 범위 대조.
- [x] 공식 Q&A 문서 갱신·전체 review·원본 보호/한글/diff 검증.
- [x] 최종 PLAN/log 기록·결과 보고 준비.

## Validation

- `& .\.conda\python.exe -B .\project1\tmp\qa_audit_20261006\audit.py`: parameter/geometry 검사 PASS. Part1의300/398 K·Part2의398 K에서 τn=τp=10 µs, ni=n1=p1, source/drain/body의 potential·전자·정공 contact 등록을 확인했다. Numerical solve를 차단하고 기존 파일을 읽기만 했다.
- Fresh reload에서 두 파일의 equation 부재·NetDoping·실제 geometry·기존 hash 일치를 확인했다. Part2 separation50 nm/dielectric4 nm·storage=source·hk 접점 위치·bulk_oxide만 존재를 확인했다.
- 기존 fine raw의0.1 V 표본21점으로8/8 PASS. Vth0.486363 V, SS66.683007 mV/dec, DIBL12.537776 mV/V, body0.028194 V. 새0.1 V DC sweep·조교 evaluator 결과가 아니며 fine 정본은 그대로다.
- strict UTF-8/한글·필수 PLAN절·OFFICIAL_QA 내용·git diff --check·보호 snapshot1518파일 hash·staged/log prefix 검사 PASS. 최종 결과는 `project1/tmp/qa_audit_20261006/validation.json`, 상세 근거는 `audit_result.json`이다.

## Progress / Discoveries

- Vg sweep0.1 V는 이번에 알려진 추출 sampling 간격이다. 기존 공식 ramp0.1 V와 역할이 다르며, 답변은 더 세밀한 sweep을 허용한다.
- Capacitor separation20 nm는 질문자의 예시값이지 의무값이 아니다. 우리 구조의50 nm separation과4 nm dielectric을 별도로 평가한다.
- 이전 PLAN은 scratch에 백업했다. 사용자 추가 파일 `hw1/step2/check_structure_file.py`도 읽기 전용으로 보존한다.
- 초기 감사 스크립트가 Part2를300 K에도 등록하려다 기존 ‘Part2는398 K’ guard에 거절됐다. 원인은 감사 범위 선택이며 소자 수렴 실패가 아니다. 기존 guard/physics는 유지하고 공식 조건398 K로 검사 범위를 바로잡았다. 첫 등록 로그도 보존했다.
- Actual bulk 길이는 Part1의1.6 µm와 Part2의0.7 µm다. 새 답변과 기존 S/D 개별 범위를 모두 만족하며 Lg/W 변경은 없다.
- 추가된 `hw1/step2/check_structure_file.py`와 사용한 `project1/check_structure_file.py`의 SHA256도 동일하다. 두 파일 모두 읽기 전용으로 보존했다.
- 조교가 질문자의20 nm 분리 구조를 테스트 가능하다고 답한 것이 우리50 nm 구조의 직접 재평가 결과는 아니다. 기존 source-contact 위 구조 허용·현재 self-check/geometry/연결·CSTORE 근거와 함께 부합 여부를 판단했다.

## Final Review

- 추가 Q&A의 ohmic contact·10 µs SRH 수명·더 세밀한 Vg sweep 허용·전체 길이 자유에 부합한다. 우리 Part2의50 nm separation/4 nm dielectric·storage 연결·계면은 기존 구조 허용 및 이번 설명과 충돌하지 않는다.
- 측정 표본 변화에 따른 추출값 차이를 실제 raw로 확인했고0.1 V 표본도8 PASS였다. 이 결과를 조교 전체 evaluator의 PASS나 새 DC sweep으로 주장하지 않는다.
- 추가 공식 답변과 실제 대조를 `project1/OFFICIAL_QA.md`에 기록했다. PLAN/log 외 변경은 이 문서와 ignored scratch 근거에 한정하며 source·최종 소자·config·기존 CSV/JSON·HW1·REPORT_CONTEXT/ZIP은 보존했다.
- 새 numerical solve·READ/retention·전체 unittest·최적화·commit/push·제출은 없다. 이번 대조 요청은 완료하고 다음 요청을 기다린다. 조교 재평가 및 우리50 nm separation의 개별 공식 확인은 확보되지 않았다.
