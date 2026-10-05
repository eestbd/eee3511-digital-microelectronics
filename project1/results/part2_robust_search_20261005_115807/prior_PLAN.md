# PLAN.md

현재 작업: 최종 Part 2 셀의 64 ms 이후 retention 실패 시각 측정.
상태: 측정·원시 데이터·민감도·보호 검증 완료. Cell retention estimate 약67.2 ms, 제한 상태data1. 기존 최소64 ms 조건은 유지된다.

## Goal

최종 셀에서 열화 후 0.5 ns READ 마진이60 mV 아래로 내려가는 최초 시각을 실제 계산으로 추정한다. 셀 retention은 두 저장 상태 중 짧은 시간이다. 결과는 유한 구간과 수치 민감도로 보고하며 수학적으로 정확한 값이라 주장하지 않는다.

## Current State

- Part 2 #11, part2_2022142233.devsim SHA256=f2442ee257af6dfcb610db5928d0ff5d3b8e5bce1d2423d72e00c7fb099fe62e, config=part2_final.yaml.
- 기본/미세 retention 모두64 ms에서 PASS. Data1 마진60.417968/60.420969 mV, data0 마진117.214/117.304 mV다. 최초 실패 시간은 아직 측정되지 않았다.
- 기존 retention 함수는64 ms 기본 상한과 초기 Vcell0/2만 지원한다. 기존 raw/코드를 덮어쓰지 않고 새 측정 script에서 동일 signed Euler·READ 판정으로64 ms 끝점부터 이어간다.
- Structure 저장/자가검사는 완료됐으며 실제 OK 화면과 통합 보고서 제작은 별도 남은 작업이다.

## Requirements

- 최종 설계·구조·physics·source·과거 결과·Part 1/HW1·PDF를 보존하고 새 결과 폴더만 사용한다.
- T398 K, VB−0.5 V, extended3종=true, ramp0.1 V, W0.1 µm, CBL100 fF, READ10 ps/0.5 ns, |VBL−1|≥60 mV 판정 유지.
- Data1 holding WL0/BL0, data0 WL0/BL2; 저장 누설에 폭을 한 번 적용한다. 기존 기본/미세3/1.5 mV 적분 제한과8 ms 최대 시간 간격을 유지한다.
- 각 기존 checkpoint의 fresh READ 재현을 먼저 확인하고 physics/source/config/구조/CSTORE가 원 측정과 일치하는지 검증한다. 재개 이유·전압·기존 결과 provenance를 기록한다.
- 먼저 data1 failure bracket을 찾고 재적분+READ bisection으로 상대 구간폭≤0.1%까지 좁힌다. Data0은 적어도 그 bracket 상단까지 READ 통과를 확인해 셀의 제한 상태를 구분한다.
- 소자 재설계·새 parameter 탐색·기존 PASS/FAIL 기록 수정·commit/push·제출은 수행하지 않는다.

## Assumptions

- 요청은 최대 cell retention이 궁금하다는 추가 측정 승인이다. 기존10회 parameter 탐색과 무관한 고정 소자 재측정이며 parameter 후보를 추가하지 않는다.
- DC 모델의 현재 상태는 terminal 전압과 고정 구조로 정해지므로 checkpoint 전압을 fresh reload로 재현한 뒤 continuation한다. 실제 READ 차이가0.05 mV를 넘으면 중단하고 원인을 조사한다.
- 한계에 가까운 data1을 먼저 측정하고 data0이 그 상단까지 통과하면 cell retention은 data1의 추정 bracket이다. Data0 자체의 전체 최대 시간까지 불필요하게 계산하지 않는다.
- 새 측정의 물리 시간 guard는1 s/10,000 Euler steps다. 그 안에 실패하지 않으면 그 하한만 보고하며 임의 extrapolation하지 않는다. Wall-clock 상한은 정하지 않았고 meaningful 진행 상태를 지속 보고한다.
- 기존 구현과 동일하게 checkpoint 사이 단일 failure crossing/연속적 margin 변화를 가정하며 관측 margin 단조성을 확인한다. Mesh 민감도/조교 evaluator는 별도 미검증이다.

## Plan

- [x] 최신 PLAN/log·최종 구조/config·공식 조건·기존 retention raw/알고리즘 조사.
- [x] 보호 snapshot과 새 continuation script·기본 논리 검증 준비.
- [x] 기본/미세 data1의64 ms 재현·실패 bracket/bisection 실제 측정.
- [x] Data0가 data1 failure 상단까지 통과하는지 실제 continuation 확인.
- [x] Raw·적분/전류/전하·민감도·source/hash/provenance 검증, 결과 문서/PLAN/log final review.

## Validation

- .conda/python.exe -B 사용, DLL PATH와 UTF-8을 준비한다. 새 script를 fake constant-current/READ로 검증하고 실제 TCAD에서 checkpoint margin 재현을 확인한다.
- 고정 source/config/제출 구조 hash와 CSTORE19.824 fF를 대조한다. 각 DC terminal conservation은 기존 current/read validation을 그대로 사용한다.
- 새 실행 script: project1/results/retention_estimate_20261005_111911/measure.py. --selftest는 양 부호 상수 누설의 알려진 failure time과 실패 없는 상한 처리3건 PASS다. 기존 cell.py/part2.py를 수정하지 않았다.
- 실제 continuation CSV의 dt>0, dt≤8 ms, |ΔVcell|≤3/1.5 mV, signed Euler ΔV=−Is·W·dt/CSTORE, READ50steps/전하 보존을 확인한다. Bracket 양끝의 READ 통과/실패와 상대폭≤0.1%를 검증한다.
- 기본/미세 failure 중간값 차이≤1%를 사전 수치 민감도 기준으로 사용한다. 벗어나면 결과를 안정된 estimate로 선언하지 않고 root cause를 조사한다.
- 기존 파일/hash·staged 상태·log byte prefix·UTF-8 실제 한글·diff check를 검증하고 실제 UTC→KST 시각으로 최종 log를 append한다.
- 실제 실행 완료: measure.py --phase primary/fine --bit1(각1 s guard), 이어 --bit0 --stop-time 0.07259764773458156. 네 fresh process 모두 measurement_complete=true/error 없음. Data1 basic/fine 약711/718초, data0 약140초씩 실행했다.
- audit.py 독립 검증 PASS: 네 continuation의 유한값·dt/ΔV·Euler, 모든 READ50steps·전류/전하·전압 update, 실제 failure bracket/refinement·단조성·기본/미세 민감도·source/config/구조 hash 대조. 기존592개 보호 파일·staged 상태·log prefix 보존 PASS. Native 전체 log는 새 결과 폴더에 보존했다.

## Progress / Discoveries

- Data1을 기준으로 cell retention을 먼저 찾는 이유는64 ms에서60 mV 기준까지 여유가0.418 mV인 반면 data0은117 mV이기 때문이다. Data0 자체의 실패시각 대신 cell 제한 상태를 실제 확인한다.
- 단순 누설 전류나 기존 margin 직선 외삽으로 시간을 산출하지 않고 DC 누설 적분과 열화된 READ를 반복한다.
- 기본/미세 seed READ는64 ms의60.417968/60.420969 mV를 각각 재현했다. 실제 continuation CSV/native log/read checkpoint를 새 결과 폴더에 누적하고 있다.
- Data1 최초 sampled failure는 기본72.597648 ms/59.269445 mV, 미세72.119709 ms/59.338223 mV였다. 이 통과/실패 구간을 실제 bisection으로 좁혀 아래의 최종 bracket을 얻었다. 기존64 ms PASS는 유지된다.
- Data1 bisection 완료: 기본67.156949~67.224118 ms, 미세67.171761~67.235196 ms. 각 구간폭은0.1% 이하이고 실제 endpoint READ는 통과/실패를 구분한다. 중간값은67.190533/67.203479 ms, 차이0.012945 ms(약0.0193%)다. Cell 제한 상태 확정을 위해 data0은 기본 최초 sampled failure 상단72.597648 ms까지 추가 확인했다. 이는 최종 실패 bracket 상단보다 긴 보존 확인이다.
- Data0 기본/미세72.597648 ms 실제 측정 완료: margin116.674533/116.763318 mV PASS. 자체 failure time은 미측정이나 data1 구간 상단보다 길게 통과해 cell 제한 상태가 data1임을 확인했다.

## Final Review

- 고정 최종 셀의 최초 READ failure time 측정 완료. 미세 data1 midpoint67.203479 ms(약67.2 ms), bracket67.171761~67.235196 ms다. Data0는72.5976 ms까지 유지돼 cell 제한 상태는data1이다. Data0 자체 최대 retention을 측정했다고 주장하지 않는다.
- 신규 report=project1/PART2_RETENTION_ESTIMATE.md, 실제 결과/검증=project1/results/retention_estimate_20261005_111911. 기존 code/API/설계/소자/raw/physics/Part1/HW1/PDF를 변경하지 않았고 과거 실패 기록을 보존했다. 새 측정 script와 raw·보고 문서만 추가했다.
- 요구 판정·전류/전하/적분·기본/미세 민감도·provenance·기존 파일 보호 PASS. Native 로그·중간 checkpoint·재읽기CSV·refinement도 보존했다. 독립 mesh/조교 evaluator/물리 모델 전체 오차는 미검증이며 bracket은 이에 대한 confidence interval이 아니다.
- 2026-10-05 11:39:08 KST 최종 기록을 append했고 기존 prefix를 보존했다. 최종 UTF-8 실제 한글·doc 링크·diff check·기존 파일/hash·staged/log prefix 보존 PASS. 현재 측정 요청 완료이며 재설계·commit/push·업로드·최종 보고서 제작은 수행하지 않았다.
