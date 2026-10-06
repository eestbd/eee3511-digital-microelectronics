# Project 1 최종 제출물 검토

검토일: 2026-10-06 KST. 대상은 사용자가 지정한 보고서와 소자 파일이며, 과제의 최신 `Project1_Assignment_0927.pdf` 및 `OFFICIAL_QA.md`와 대조했다.

**결론: 검토한 보고서와 현재 `project1/`의 Part1·Part2 두 소자로 제출할 수 있다. 제출을 막는 필수 항목 누락, 잘못된 최종 후보, 수치 불일치를 발견하지 못했다.** 보고서나 소자 원본은 수정하지 않았다. 실제 LearnUs 업로드는 수행하지 않았다.

## 1. 제출할 세 파일과 정본 확인

| 파일 | 현재 위치 | 검토 결과 |
|---|---|---|
| `part1_2022142233.devsim` | `C:/Users/super/DEVSIM_PROJECT/project1/part1_2022142233.devsim` | 최종 Part1 #10과 byte 단위 일치, 새 프로세스 self-check OK |
| `part2_2022142233.devsim` | `C:/Users/super/DEVSIM_PROJECT/project1/part2_2022142233.devsim` | robust search의 최종 #19와 byte 단위 일치, 새 프로세스 self-check OK |
| `2022142233_이우현_Project#1.pdf` | `C:/Users/super/OneDrive/Desktop/2022142233_이우현_Project#1.pdf` | 12쪽 전체 본문·그림·화면 검토, 필수 7절과 두 실제 OK 화면 포함 |

검토 시작 당시 Desktop의 두 소자도 같은 정본과 일치했고 각각 self-check OK였다. 검토 도중 사용자가 두 파일을 `project1/`의 파일에 덮어썼다고 확인했으며, 변경 후 위 현재 경로를 다시 검사했다. 특히 현재 루트 Part2 파일을 예전 #11로 취급하면 안 된다. 현재 파일은 최종 #19다.

| 파일 | Byte 수 | SHA256 |
|---|---:|---|
| Part1 | 292682 | `41c6f8f6ff5782c8ec3ecbc98d39bd264149ec076630f8bad0c9c98d6f06d07c` |
| Part2 | 486342 | `376b392d2a81e9016f89c811f382a8f2d81e065dbeff9eef6072eab052753c11` |
| 보고서 | 915964 | `3ac7691314df1357bb06b94af22543964c00d0c0c9054b029e6a01121008e129` |

소자 파일마다 device가 하나이며 물리 방정식·계산 결과 없이 mesh/region/material/contact/interface/doping이 저장되어 있다. `bulk.NetDoping`, `bulk_oxide`, `gate/source/drain/body`, gate 재료 `W`, SiO₂ gate oxide가 확인된다. Part2는 `hk_l/hk_r` 재료 `ZrO2`, 각각의 `storage_l/r`, `plate_l/r`가 올바른 hk region에 있다. 직접 닿지 않는 bulk와 hk 사이에 interface가 없는 것은 공식 Q&A와 일치한다.

## 2. 보고서 필수 항목 대응

과제 제출 안내의 필수 7절을 실제 보고서에서 확인했다. 절 이름도 `Part-1-(a)` 등의 요구 형식이다.

| 요구 항목 | 보고서 위치 | 확인한 내용 |
|---|---|---|
| Part-1-(a) 빠진 물리 | 1–2쪽 | HW1 재사용 모델과 추가한 온도 의존 ni/이동도·gate work-function 구분, 이유·식·구현·검증 |
| Part-1-(b) 설계 탐색 | 2–4쪽 | 초기 실패, 10회 탐색, 공식 모델 재측정, 최종 선택 판단, 소자 그림, 8 spec 표 |
| Part-1-(c) 왜 되는가 | 4–5쪽 | 최종 설계에서 tox/Lg/NA를 각각 바꾼 one-knob 비교, 지표 변화와 물리 해석, 상한 초과 FAIL도 기록 |
| Part-2-(a) 셀 구조 | 5–6쪽·11쪽 | 1T1C 그림, 비대칭 도핑·tap·source 위 capacitor, 전체 plate dQ/dV 추출과 CSTORE |
| Part-2-(b) 읽기 | 6–8쪽 | Data0/1의 ΔVBL(t)와 I(t), 부호·폭·시간 갱신, 0.5 ns 값과 60 mV 비교 |
| Part-2-(c) 설계 탐색 | 8–9쪽 | 초기 retention 실패 → #11 통과 → 여유 개선 #19, 변수·측정·선택 이유와 tradeoff |
| Part-2-(d) 결과 | 9–12쪽 | 최종 셀/NetDoping 그림, 초기/64 ms READ 및 retention 표, 실패 구간·하한·설계 근거 |
| 두 실제 self-check OK 화면 | 3쪽 그림1(b)·12쪽 그림5(c) | 최종 Part1 파일과 robust selected Part2 #19의 실제 결과. 현재 제출 파일과 hash가 같음 |
| 형식/분량 | 전체 | 학번·이름과 파일명 일치, 12쪽, 페이지·그림·표 표시, 이미지 PDF 내부 포함 |

필요한 OK 화면이 PDF 안에 들어 있으므로 제출물은 보고서 PDF와 두 `.devsim`, 총 세 파일로 구성할 수 있다. 설정 YAML, Python 코드, #19 실험 폴더를 함께 제출해야 한다는 요구는 없다.

## 3. Part1 최종 설계·성능

W gate, Lg=0.6 µm, tox=4.75 nm, xj=0.1 µm, tSi=0.5 µm, source/drain 각 0.5 µm, NA=2×10¹⁶ cm⁻³, ND=10¹⁹ cm⁻³는 허용 범위 안에 있다. 저장된 geometry도 보고서의 치수와 일치한다.

최종 fine raw CSV에서 8개 지표를 다시 추출해 기존 metrics JSON과 보고서의 반올림 값을 대조했다.

| 항목 | 과제 기준 | 최종 값 | 판정 |
|---|---|---:|---|
| Vth | 0.40–0.50 V | 0.484848 V | PASS |
| Ion | ≥450 µA/µm | 516.137657 µA/µm | PASS |
| Ioff | ≤1 pA/µm | 0.012637 pA/µm | PASS |
| SS | ≤75 mV/dec | 66.221883 mV/dec | PASS |
| Ioff, 398 K | ≤100 pA/µm | 10.375526 pA/µm | PASS |
| DIBL | ≤30 mV/V | 13.042381 mV/V | PASS |
| Body effect | ≤0.08 V | 0.026622 V | PASS |
| Eox | ≤5 MV/cm | 4.210526 MV/cm | PASS |

Vth의 양의 전류 log 보간, SS의 2-decade 평균, DIBL의 1.95 V 및 mV 환산, body bias 조건, Eox=2 V/tox를 원시 데이터·구현과 대조했다. 보고서의 one-knob 측정 간격과 최종 fine 값의 작은 차이는 명시되어 있으며, NA 변경의 0.500344 V를 반올림하여 PASS로 취급하지 않는다.

## 4. Part2 최종 #19

고정 Lg=0.3 µm·폭0.1 µm를 유지하며, tox=5.3 nm, xj=0.05 µm, tSi=0.3 µm, source/drain 각0.2 µm다. ZrO₂ 높이1.245 µm·두께4 nm, source contact 위 pillar와 clearance50 nm는 보고서와 일치한다. 비균일 배경·비대칭 S/D·하단 p+ tap은 최종 NetDoping에 저장되며 공식 Q&A의 허용 범위에 부합한다.

| 항목 | 기준 | 최종 값 | 판정 |
|---|---|---:|---|
| CSTORE | ≤20 fF | 19.2819375 fF | PASS |
| Gate field | ≤5 MV/cm | 4.716981 MV/cm | PASS |
| Capacitor field | ≤4 MV/cm | 2.5 MV/cm | PASS |
| 초기Data0 READ | 0.5 ns에서≥60 mV | 127.806239 mV | PASS |
| 초기Data1 READ | 0.5 ns에서≥60 mV | 69.463266 mV | PASS |
| 64 ms 후Data0 READ | 0.5 ns에서≥60 mV | 113.056656 mV | PASS |
| 64 ms 후Data1 READ | 0.5 ns에서≥60 mV | 63.559235 mV | PASS |
| Data0 retention | ≥64 ms | ≥128 ms, 최대 시간 미측정 | PASS |
| Data1/cell retention | ≥64 ms | 약95.198837 ms, 아래의 구간 추정 | PASS |

Data1의 fine 실패 구간은94.937594 ms의60.030102 mV PASS와95.460080 ms의59.966779 mV FAIL이다. 95.198837 ms는 구간의 중간값이며 해당 시각을 직접 측정한 최대값이 아니다. Data0의≥128 ms도 측정한 하한이다. 보고서는 이 구분을 올바르게 설명한다.

T=398 K, VB=−0.5 V, WL high=2.5 V, READ 초기BL=1 V, CBL=100 fF, dt=10 ps, 0.5 ns 판정이다. Retention은 WL=0에서 Data0의BL=2 V/Data1의BL=0 V를 사용하고 열화된 Vcell에서 재READ했다. 두 데이터 상태×기본/미세의4개 프로세스에서 수행한 기존 측정은 모두 필수 조건PASS이며 동일한 최종 구조hash를 기록한다.

## 5. 수치·그림·구현의 상세 확인

- geometry·raw 재추출·보고서 반올림·전류·VBL/Vcell·시간·용량·이전#11 비교 등53개 수치의 일치를 확인했다. 추가 DC/READ/retention 실험은 실행하지 않았다.
- Plate 좌우 전하를 합산하며1 V 중심의±10 mV 및±5 mV 차분에서 CSTORE가 일치한다. 2D 전하의 폭cm 환산과A/µm 전류의 폭µm 환산을 혼동하거나 중복 적용하지 않는다.
- READ 전류는 구간 시작, CSV 갱신 후 전압은 구간 종료로 설명한다. Data0/1의 반대 전류 방향,50 step/100 step, ns 축과 hold의ms 축이 올바르다. Data1의0.4 ns 미달과0.5 ns 통과를 구분한다.
- Body 전류를 포함한 charge residual은 허용값 이하이며 물리적 예측 정확도의 보증으로 취급하지 않는다. 기존128bit 확장 정밀도·ramp0.1 V 검증과 double 진단의FAIL/미재실행도 구분한다.
- 이전#11→#19 retention 개선41.66%와64 ms에서60 mV 초과분의 약8.5배를 구분한다. Data0 마진 감소, 추가75 mV/96 ms 등의 목표 미달, 전역 최적·공정 변동·독립 mesh 미검증도 공개한다.
- 전체12쪽을 이미지로 확인했다. 한글·식·그래프·표·스크린샷의 중대한 깨짐, 잘림, 누락, 빈칸, 오래된 학번·미완성 문구는 발견하지 못했다.

## 6. 필수 수정·선택 보완·한계

**필수 수정 없음.** 현재 보고서와 위의 두 파일을 제출할 수 있다.

선택 보완으로 SRH의 ‘기존 수명 유지’를τn=τp=10 µs로 수치까지 쓰면 공식Q&A와의 대응이 더욱 명확하다. 일부 수식caption에서 단어가 줄을 넘는 부분도 있지만 내용을 읽을 수 있으며 제출을 막는 누락은 아니다. 이 수정들은 필수가 아니다.

실제 파일의 구조와 로컬에 저장된 재현·성능 근거를 검토했으며 조교의 비공개 채점 프로그램을 실행한 결과는 아니다. 실제 채점값·허용 오차와의 일치를 보장하는 증거는 없다. 이 한계는 보고서의 설명과 모순되지 않는다.

근거: `project1/tmp/submission_review_20261006/`의 추출 본문,전체 페이지render,Desktop/current 각checker log,`audit_results.json`. 최종Part1 raw는`results/official_20261004_155839/part1/candidate_10/fine/`,최종Part2는`results/part2_robust_search_20261005_115807/experiments/19_balanced_ND20/`다.
