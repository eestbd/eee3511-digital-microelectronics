# Project 1 Part 1·2 완료 상태 검토

검토일: 2026-10-04, Asia/Seoul. 학번: 2022142233.

**핵심 구현·최종 설계의 로컬 요구 조건은 두 Part 모두 PASS다. 과제 전체 제출 준비는 아직 완료되지 않았다.** 이번 요청에서는 재최적화·feature 구현·소자 변경·제출 보고서 제작을 하지 않았다.

근거는 [과제 PDF](Project1_Assignment_0927.pdf), [공식 Q&A](OFFICIAL_QA.md), 현재 코드, 최종 config, 원시 CSV, 측정 당시 source hash, 저장 구조와 실제 보고서다. PDF 파일 순서 기준 50~51쪽은 Part 1, 52~54쪽은 Part 2와 naming, 55~57쪽은 저장·checker·제출 요구사항이다. 관련 표·식·그림과 checker 예시를 시각 확인했다.

## 판정 구분

| 범위 | 현재 판정 | 근거 / 남은 내용 |
|---|---|---|
| Part 1 모델·측정·설계 | 로컬 PASS | 동일 #10 소자의 8개 spec, 공식 정밀도·ramp, raw 재추출 및 기존 numerical validation |
| Part 2 셀·CSTORE·READ·retention | 로컬 PASS | #11 두 상태 READ와 64 ms 보존, 기본/미세 간격, 전류·전하·원시 적분 검사 |
| 저장 구조 | 두 구조 checker OK | 새 프로세스에서 singleton·재료·접점·도핑·physics equation 없는 저장 확인 |
| 학번 파일 | 일부 완료 | Part 2 파일 존재. Part 1은 검증된 diagnostic 구조만 있으며 학번 파일 준비는 유보 상태 |
| 최종 제출 보고서·OK 화면 | 미완료 | 현재 PDF는 7쪽 Part 1 초안. Part 2 section·최종 그림·지정 곡선·실제 OK 화면을 포함한 최종 PDF 필요 |
| 조교 재평가·mesh 민감도 | 미검증 | 로컬 검사 통과를 실제 조교 evaluator 통과로 보장하지 않음 |

PDF의 실제 설계 과제는 Part 1과 Part 2다. 슬라이드의 ‘3’, ‘4’, ‘5’, ‘6’은 Part 2 목표·설계·파일 저장·제출물의 장 번호이며 별도 Part 3·4 과제를 뜻하지 않는다.

## Part 1: 8개 조건

최종 #10: W gate, Lg=0.6 µm, tox=4.75 nm, xj=0.1 µm, tSi=0.5 µm, S/D 각각 0.5 µm, NA=2e16, ND=1e19 cm⁻³. PDF 설계 범위에 들어간다.

| 항목 | 최종 fine 값 | PDF 기준 | 판정 |
|---|---:|---:|---|
| Vth | 0.484848 V | 0.40~0.50 V | PASS |
| Ion | 516.138 µA/µm | ≥450 | PASS |
| Ioff | 0.0126374 pA/µm | ≤1 | PASS |
| SS | 66.2219 mV/dec | ≤75 | PASS |
| Ioff, 398 K | 10.3755 pA/µm | ≤100 | PASS |
| DIBL | 13.0424 mV/V | ≤30 | PASS |
| Body effect | 0.0266225 V | ≤0.08 | PASS |
| Eox | 4.21053 MV/cm | ≤5 | PASS |

- [fine metrics 및 raw](results/official_20261004_155839/part1/candidate_10/fine/metrics.json)의 세 Id–Vg CSV 각 201점·0.01 V 간격과 고온 off CSV에서 8개 값을 독립적으로 다시 계산했다. 기준 전류의 log interpolation, SS 구간, 단위, 전류 보존을 확인했고 보고값과 일치했다.
- 기존 [numerical validation](results/official_20261004_155839/part1/candidate_10/numerical_validation.json)의 `grading_condition_checks_pass`, `extended_baseline_checks_pass`, `grading_conditions_match`는 모두 true다. 0.02/0.01 V 비교, 전류 보존, fresh live/reload 중요 bias 재현을 포함한다.
- 위 JSON의 `all_checks_pass=false`는 더 넓은 선택적 double 검사까지 포함하는 필드다. 이번 최종 측정에서 double은 미실행이며, 공식 Q&A의 확장 정밀도 조건 판정과 구분한다. 과거 double 실패 기록은 보존했다.
- 선택 [diagnostic 구조](results/official_20261004_155839/part1/selected/part1_selected_diagnostic.devsim)와 fine 측정 구조의 SHA256은 `41c6f8f6ff5782c8ec3ecbc98d39bd264149ec076630f8bad0c9c98d6f06d07c`로 같다. 새 checker OK, singleton·equation 부재·Lg/tox·접점 위치·NetDoping 2,340개 노드 확인 PASS다.
- Part 1이 사용하는 측정·physics·simulator·config·extractor source는 측정 시 hash와 일치한다. 당시 넓게 수집한 목록의 `mosfet_tool/cell.py`만 이후 Part 2 개발로 달라졌으며 Part 1 실행 경로는 이를 사용하지 않는다.
- `part1_2022142233.devsim`은 아직 준비되지 않았다. 이는 성능 실패가 아니라 이전에 마지막으로 유보한 제출 준비 항목이다.

## Part 2: 1T1C 조건

최종 #11: [part2_final.yaml](part2_final.yaml), W gate, Lg=0.3 µm, tox=5 nm, xj=0.05 µm, tSi=0.3 µm, S/D 각각 0.2 µm, NA=7e16·ND=1e19 cm⁻³. ZrO2 κ=35, 높이0.96 µm·막3 nm의 양쪽 slab. Bottom p+ tap은 추가 acceptor1e19 cm⁻³·두께0.05 µm이며 실제 NetDoping에 포함된다.

| 항목 | 기본 측정 | 미세 간격 측정 | PDF 기준 / 판정 |
|---|---:|---:|---|
| 초기 data 0, 0.5 ns READ 마진 | 127.320 mV | 126.881 mV | ≥60, PASS |
| 초기 data 1, 0.5 ns READ 마진 | 67.301 mV | 67.209 mV | ≥60, PASS |
| data 0 retention | ≥64 ms | ≥64 ms | ≥64, PASS |
| data 1 retention | ≥64 ms | ≥64 ms | ≥64, PASS |
| data 0, 64 ms 후 READ 마진 | 117.214 mV | 117.304 mV | ≥60, PASS |
| data 1, 64 ms 후 READ 마진 | 60.417968 mV | 60.420969 mV | ≥60, PASS |
| CSTORE | 19.824 fF | plate 미분 간격 반감 일치 | ≤20, PASS |
| Gate 전계 | 5.000 MV/cm | 동일 | ≤5, PASS |
| Capacitor 전계 | 3.333 MV/cm | 동일 | ≤4, PASS |

- 구현: `mosfet_tool/cell.py`의 셀 mesh, storage/plate 연결, 전체 plate dQ/dV, DC→signed current→전압 갱신 READ 및 adaptive retention. 398 K·VB=−0.5 V·WL=2.5 V READ, BL 초기1 V·CBL100 fF·폭0.1 µm, holding WL0·data0 BL2/data1 BL0 조건을 사용한다. 폭 변환은 한 번 적용된다.
- READ 기본10 ps/미세5 ps는 0.5 ns까지 측정했다. 원시 CSV의 시간, 전류 보존, 양 capacitor Euler 갱신과 body 전류를 포함한 총 전하 보존을 재확인했다. Retention 기본/미세 ΔV 제한은3/1.5 mV다. Signed storage current 적분과 열화 후 0.5 ns READ 판정, 64 ms 끝점 및 모든 저장된 READ checkpoint 통과를 확인했다.
- [combined_final](results/part2_optimization_20261004_202430/experiments/11_W_cap096_bodytap/combined_final/metrics.json)과 [combined_fine](results/part2_optimization_20261004_202430/experiments/11_W_cap096_bodytap/combined_fine/metrics.json)은 같은 구조·config·공식 함수·수치 조건의 상태별 완료 측정을 종합한다. 원 순차 실행은 data0 checkpoint 뒤 중복 data1 계산을 종료했다. 원 순차 실행 전체가 완료됐다고 해석하지 않는다. 원 기록·로그·provenance를 보존했고 공통 source 및 wrapper의 추가 hash, 입력 조건과 실제 raw를 대조했다.
- 현재 [학번 구조](part2_2022142233.devsim)의 SHA256 `f2442ee257af6dfcb610db5928d0ff5d3b8e5bce1d2423d72e00c7fb099fe62e`는 기본·미세 측정 구조와 같다. 새 checker OK, singleton·equation 부재, 실제 geometry/재료/storage·plate 접점과 NetDoping 2,142개 노드 PASS다. Tap을 포함한 기대 분포와 차이는0이다.
- Source contact 위 capacitor 배치와 bulk-hk 직접 접촉 부재는 추가 공식 Q&A에서 허용한 구조다. Part 1과 다른 TR parameter와 bottom p+ tap 사용도 허용된다. 미인식 LDDDoping/HaloDoping에 의존하지 않는다.
- 재현 시 주의: profile/tap을 새로 구축하려면 `part2_experiment.py`의 `ProfileCellSimulator` 경로를 사용한다. 일반 `part2.py`는 `--reload-structure part2_2022142233.devsim`으로 최종 저장 NetDoping을 읽어야 한다. `part2.py --config part2_final.yaml`만으로 다시 build하면 최종 tap을 재생성하지 않는다. 제출 채점은 저장 구조를 읽으므로 현재 학번 파일의 tap은 포함돼 있다.

## 물리 모델과 검증 범위

`mosfet_tool/physics.py`와 simulator는 공식 Q&A의 Varshni Eg(T), ni(300 K)=1e10 정규화 ni(T), 동일 ni의 SRH n1/p1, μn=400(T/300)^−2.4·μp=200(T/300)^−2.2, gate offset Φm−[4.05+Eg(T)/2]를 사용한다. 398 K μn/μp=202.970/107.388 cm²/(V·s)로 측정 기록과 일치한다. 확장 정밀도3종과 ramp0.1 V를 사용했으며 임의 mobility·solver 조정으로 spec 실패를 숨기지 않았다.

이번 검토의 새 검증은 `.conda/python.exe -B project1/tmp/completion_review_20261004/verify_review.py` 및 같은 폴더의 `part1_geometry.py`다. 각각 fresh checker·Part 2 geometry·원시 데이터·hash·provenance와 Part 1 geometry를 확인했다. 보호된 기존 raw·source가 그대로이므로 전체 TCAD/GUI/기존 unit test를 다시 실행하지 않았다. 새 증거는 ignored scratch에 보존한다. 구조 checker OK는 전기적 spec 검사나 조교 전체 evaluator 실행의 대체물이 아니다.

## 보고서·제출물 checklist

현재 보고서는 [Part 1 PDF 초안](../output/pdf/part1_report_draft.pdf) 7쪽이다. 실제 표·그림과 한글을 확인했다. Part 1 설명을 재사용할 수 있지만 표지의 ‘학번 미확인’, ‘Part 2 미완료 중단’은 작성 당시 상태이므로 최종 보고서에서 현재 상태로 갱신해야 한다.

| 요구 항목 | 실제 준비 상태 | 남은 작업 |
|---|---|---|
| Part-1-(a) 빠진 물리 | 초안에 설명·검증 존재 | 최종 PDF로 편집 |
| Part-1-(b) 탐색·최종 그림·8항목 표 | 초안에 존재 | 최종 학번/현재 상태 반영 |
| Part-1-(c) 한 knob씩 ablation | 초안에 tox/Lg/NA 비교 존재 | coarse 경계 ablation과 최종 fine PASS 구분 유지 |
| Part-2-(a) 셀 구조·plate dQ/dV | 코드·원시 측정 준비 | 실제 bottom tap을 표시한 최종 1T1C 그림, 추출 식/조건/값을 PDF에 작성 |
| Part-2-(b) 두 상태 READ | CSV·VBL(t) 비교 HTML·값 준비 | 최종 ΔVBL(t) 양 상태 및 PDF53쪽의 I(t), 0.5 ns·60 mV 기준 포함 |
| Part-2-(c) 설계 탐색 | OPTIMIZATION_LOG/SUMMARY·후보 metrics 준비 | 시도→지표→판단을 최종 PDF에 작성 |
| Part-2-(d) 최종 결과 | 양 상태 기본/미세 READ·retention 결과 준비 | 최종 셀 그림·값/하한 표·설계 근거를 PDF에 작성 |
| Part 1 학번 파일 | 없음 | 기존 검증 구조를 정확한 제출명으로 준비하고 hash 대조·fresh checker |
| Part 2 학번 파일 | 있음, fresh checker OK | 같은 최종 파일을 제출 package에 포함 |
| 두 실제 파일의 OK 화면 | 현재 보고서에 없음 | 정확한 학번 파일명으로 검사한 실제 화면을 캡처하여 PDF에 포함 |

현재 최종 비교 HTML은 READ 전압·data1 보존 전압/마진을 그린다. READ I(t)는 raw의 `Id_A/Is_A/Ib_A`로 준비할 수 있지만 최종 보고서용 전류 그림은 아직 없으며 보존 전압 그림을 I(t) 그림으로 계산하지 않는다. Checker 원문을 텍스트로 넣은 초안7쪽은 과제의 실제 화면 캡처 준비와 구분한다.

## 남은 한계와 다음 순서

1. Part 1 검증 구조를 `part1_2022142233.devsim`으로 준비하고 최종 두 파일의 실제 OK 화면을 확보한다. 기존 diagnostic 파일을 바꾸거나 재설계할 필요는 없다.
2. 준비된 결과로 Part-1-(a)~(c)·Part-2-(a)~(d)를 정확히 표기한 약12쪽 최종 PDF를 만들고 구조·전류·READ 곡선·수치 표·OK 화면을 포함한다. 학번과 현재 완료 상태를 갱신한다.
3. 보고서 값과 최종 두 구조의 hash·실제 검증 조건을 대조하고 LearnUs 제출물을 최종 확인한다. 마감은2026-10-07 23:59 KST다. 이번에는 제출·commit·push를 하지 않았다.

Data1의64 ms 마진 여유는 약0.418 mV로 작다. Gate 전계는 상한과 같고 CSTORE도 상한에 가깝다. 64 ms 이후 최초 실패 시각은 아직 측정하지 않았으므로 retention은 **≥64 ms 관측 하한**으로 표기해야 한다. 더 긴 retention의 점수나 독립 mesh/조교 재실행에 대한 여유를 확인하려면 별도 추가 검증·탐색이 필요하다. 이것을 현재 최소 조건 FAIL이나 이미 확인된 최대 retention으로 표현하지 않는다.
