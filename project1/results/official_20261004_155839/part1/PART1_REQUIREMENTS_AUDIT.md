# Part 1 과제 조건 최종 대조

2026-10-04 검토. 근거는 최신 `Project1_Assignment_0927.pdf`의 Part 1 목표·설계 범위·저장·제출 페이지와 교수/조교 공식 Q&A다. 소자 및 시뮬레이션 코드는 이번 점검에서 변경하지 않았다. Part 2는 계속 중단한다.

**판정: 최종 #10의 전기적·설계 조건은 모두 충족한다. 제출 준비 전체는 학번 및 해당 OK 화면 확정 전까지 미완료다.**

## 전기적 조건 — 같은 소자 8/8 PASS

| 항목 | 과제의 측정 조건 | 요구 기준 | 실제 fine 결과 |
|---|---|---|---:|
| Vth | VD=0.05 V, ID=1e-7 A/µm | 0.40…0.50 V | 0.484848 V |
| Ion | VG=VD=2 V, 300 K | ≥450 µA/µm | 516.138 µA/µm |
| Ioff | VG=0, VD=2 V, 300 K | ≤1 pA/µm | 0.012637 pA/µm |
| SS | VD=0.05 V, ID=1e-10…1e-8 A/µm 평균 | ≤75 mV/dec | 66.222 mV/dec |
| 고온 Ioff | VG=0, VD=2 V, 398 K | ≤100 pA/µm | 10.376 pA/µm |
| DIBL | VD=0.05/2 V의 정전류 Vth 차이/1.95 | ≤30 mV/V | 13.042 mV/V |
| Body effect | VD=0.05 V, VB=-0.5/0 V의 Vth 차이 | ≤0.08 V | 0.026622 V |
| Eox | VDD/tox, cm 단위 환산 | ≤5 MV/cm | 4.211 MV/cm |

표에서 별도 지정하지 않은 온도는 300 K, VS=0 V, body-effect 외 VB=0 V다. 폭당 전류는 A/µm이며 표시 단위에 맞게 µA·pA로 변환한다.

근거: [최종 raw·입력·실행 조건](candidate_10/fine/metrics.json), 같은 폴더의 CSV, [공식 수치 검증](candidate_10/numerical_validation.json). Coarse/fine 간격·전류 보존·raw 재추출·fresh live/reload critical bias 모두 PASS. Extended 3종과 ramp 0.1 V를 사용했다. Double는 선택 진단이며 미실행을 PASS로 표시하지 않는다.

## 설계 범위·저장 규약

| 요구사항 | 실제 값 또는 근거 | 판정 |
|---|---|---|
| Lg≥0.3 µm | 0.6 µm | 충족 |
| SiO2 gate oxide, tox≥4 nm | Oxide helper κ=3.9, 저장 tox=4.75 nm | 충족 |
| xj=0.02…0.25 µm | 설계 xj=0.1 µm | 충족 |
| tSi=0.3…2 µm | 0.5 µm | 충족 |
| Source/drain 각각 0.2…1 µm | 각각 0.5 µm | 충족 |
| NA=1e14…1e17 / ND=1e18…1e21 cm⁻³ | 2e16 / 1e19, 저장된 실제 NetDoping profile | 충족 |
| Gate 재료 이름·허용 일함수 | gate_metal material=W, Φm=4.60 eV | 충족 |
| 모든 spec 동일 구조·도핑·재료 | 같은 저장 구조 SHA256로 bias/T만 변경 | 충족 |
| 단일 device·structure-only 저장 | Doping 후 physics 이전 저장, checker OK | 충족 |
| 고정 region/contact/interface/model 이름 | bulk/oxide/gate_metal, gate/source/drain/body, bulk_oxide, bulk.NetDoping | 충족 |

근거: [실제 저장 geometry](candidate_10/saved_geometry_validation.json), [최종 입력](selected/config.yaml), [실제 구조 검사](selected/checker.log). Body는 기존 bottom ohmic 접점이며 별도 p+ tap은 없다. PDF 그림은 예제이고 Q&A는 별도 고농도 tap을 허용한다. 접점 형상 변경을 필수로 명시한 근거는 확인되지 않았으므로 구조를 임의 변경하지 않았다.

## 보고서·제출 요구

| 요구사항 | 이번 점검 결과 | 현재 상태 |
|---|---|---|
| Part-1-(a): 빠진 물리·이유·구현·검증 | HW1 고정 ni/SRH·이동도·gate offset 부재와 추가 이유를 직접 코드 대조해 보강 | 설명 준비 완료 |
| Part-1-(b): 처음 설계→시도→지표→판단 | 초기 6/8 PASS와 Vth/Ion 문제, 기존 10회 이력, 공식 두 후보 재측정·최종 선택 이유 | 설명 준비 완료 |
| 최종 소자 그림·8항목 표 | Lg/tox/xj·접점·도핑·gate 재료 표시, 측정 조건/기준/결과 포함 | 준비 완료 |
| Part-1-(c): 한 변수씩 metric 영향 | 동일 0.02 V 간격에서 tox/Lg/NA 한 변수만 변경, 실제 8 metric 및 물리 trade-off 설명 | 준비 완료 |
| `part1_[실제학번].devsim` | 검증된 진단 구조는 있음. 학번을 질문한 상태 | **미완료 — 학번 필요** |
| 해당 파일의 실제 self-check OK 화면 | 현재 보고서는 실제 checker 텍스트만 포함. 앱 접근 승인 시간 초과로 자동 화면 캡처 미완료 | **미완료 — 실제 화면 필요** |

보강된 보고서는 `output/pdf/part1_report_draft.pdf`의 7쪽 Part 1 초안이다. 전체 과제 보고서에는 나중에 Part 2를 추가해야 하지만 현재 요청에서는 Part 2를 진행하지 않는다.

## 완료 기준과 한계

- 계산·알려진 공식 물리 조건·수치 검증·설계 범위·구조 규약은 충족했다. 관련 테스트 21개와 legacy 3 CLI 회귀도 이전 최종 검증에서 PASS다.
- 현재 남은 필수 제출 준비는 **실제 학번 파일 이름 및 그 파일의 OK 화면 포함**이다. 이름만 바꿀 때 구조 내용/해시는 동일하게 보존하고 checker를 다시 실행한다.
- 실제 조교 채점기 전체 실행은 확인하지 못했다. 공개된 공식 조건에서 만족했다는 결론이며 재채점 통과를 보장한다는 뜻은 아니다.
- 완전한 mesh convergence는 추가 수치 연구 범위이며 PDF에 별도 필수 제출 항목으로 명시되지 않았다. NA 경계 ablation은 coarse 결과이고 최종 소자 자체의 fine 검증과 구분한다.
- Part 1의 제출 준비까지 확정되기 전 Part 2로 넘어가지 않는다. 확정 후에도 자동 재개하지 않고 사용자 지시를 따른다.
