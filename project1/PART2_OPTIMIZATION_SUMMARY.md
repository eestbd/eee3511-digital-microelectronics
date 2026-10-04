# Part 2 탐색 결과

**최종 판정: Local 전체 spec 측정 PASS / 최종 validation PASS**

- 탐색 시간: 2026-10-04 20:22:48 KST부터 약 60분. 무작위 전수 탐색 대신 gate/NA/xj 단일 변수 → capacitor/채널 조합 → p+ tap/비대칭 ND를 실제 측정했다.
- 새 물리 후보 11개를 측정했다. 별도 #06은 입력 생성 오류로 측정 전에 중단됐으며 원 입력/실패 로그를 보존했다.
- Baseline 병목은 data1 누설이었다. 초기 storage 누설 2.988 pA와 실제 data1 유지시간 2.627~2.643 ms를 기준으로 비교했다.
- 선택: #11 `W + ZrO2 h=0.96 µm + p+ body tap(추가 acceptor 1e19 cm⁻³, 바닥 0.05 µm)`.
- 선택 이유: gate 단독/용량 증가/채널 조합/비대칭 ND보다 64 ms READ 결과가 좋았다. 초기 data1 누설은 0.069343 pA로 약43배 감소했다. 미측정 유지시간을 PASS로 간주하지 않았다.
- W/h0.96 기준에서 tap 추가 후 초기 body 방향 성분은 0.046614→0.001049 pA, drain 방향 성분은 0.060072→0.068294 pA였다. 총 storage 누설 감소와 READ 변화는 실제 측정값으로 판단했다(폭0.1 µm 적용 후 전류).

## 후보 비교

단위: READ는 mV, CSTORE는 fF. 초기 READ와 retention 뒤 열화된 READ를 구분한다. 끝점 screening은 최초 실패 시각/전체 retention 검증을 대신하지 않는다.

| Candidate | 주요 parameter | READ0 mV | READ1 mV | Retention0 | Retention1 | CSTORE fF | 판정 |
|---|---|---|---|---|---|---|---|
| B0 baseline | TaN, NA7e16, h0.9 | 128.264 | 84.102 | ≥64 ms PASS | 2.627~2.643 ms FAIL | 18.585 | FAIL |
| 01_gate_W | W | 123.109 | 67.391 | 미측정 | 40.11~40.51 ms FAIL | 18.585 | DATA1 FAIL |
| 02_gate_TiN | TiN | 121.175 | 61.373 | 미측정 | 20.71~20.84 ms FAIL | 18.585 | DATA1 FAIL |
| 03_body_1e17 | NA1e17 | 125.798 | 76.409 | 미측정 | 미측정 | 18.585 | SCREEN PASS/retention 미검증 |
| 04_junction_003 | xj0.03 µm | 126.808 | 80.011 | 미측정 | 미측정 | 18.585 | SCREEN PASS/retention 미검증 |
| 05_W_cap096 | W, h0.96 | 127.371 | 67.750 | 미측정 | 64ms 끝점 FAIL / 최초 실패 미측정 | 19.824 | 64ms ENDPOINT FAIL |
| 06_W_channel_split | 입력 오류 | — | — | 미측정 | 미측정 | — | ERROR |
| 07_W_channel_split | W, 채널 NA1e15/7e16 | 126.250 | 77.307 | 미측정 | 미측정 | 18.585 | SCREEN PASS/retention 미검증 |
| 08_TiN_channel_split | TiN, 채널 NA1e15/7e16 | 124.450 | 71.640 | 미측정 | 미측정 | 18.585 | SCREEN PASS/retention 미검증 |
| 09_W_channel_5e16_1e17 | W, h0.96, 채널 NA5e16/1e17 | 126.676 | 66.169 | 미측정 | 64ms 끝점 FAIL / 최초 실패 미측정 | 19.824 | 64ms ENDPOINT FAIL |
| 10_W_channel_3e16_1e17 | W, h0.96, 채널 NA3e16/1e17 | 127.603 | 68.917 | 미측정 | 64ms 끝점 FAIL / 최초 실패 미측정 | 19.824 | 64ms ENDPOINT FAIL |
| 11_W_cap096_bodytap | W, h0.96, p+ tap1e19/0.05 µm | 127.320 | 67.301 | ≥64 ms PASS | ≥64 ms PASS | 19.824 | PASS |
| 12_TiN_sourceND1e21 | TiN, h0.96, source/drain ND1e21/1e19 | 132.315 | 67.914 | 미측정 | 64ms 끝점 FAIL / 최초 실패 미측정 | 19.824 | 64ms ENDPOINT FAIL |

전체 입력·초기 누설·끝점 마진·후보 해석은 [탐색 로그](PART2_OPTIMIZATION_LOG.md)와 [비교 CSV](results/part2_optimization_20261004_202430/comparison.csv)에 있다.

## 최종 parameter

| Parameter | Baseline | Final |
|---|---|---|
| Gate | TaN | W |
| Lg (µm) | 0.3 | 0.3 |
| tox (nm) | 5.0 | 5.0 |
| Background NA (cm⁻³) | 7e+16 | 7e+16 |
| S/D ND (cm⁻³) | 1e+19 | 1e+19 |
| xj (µm) | 0.05 | 0.05 |
| Source length (µm) | 0.2 | 0.2 |
| Drain length (µm) | 0.2 | 0.2 |
| tSi (µm) | 0.3 | 0.3 |
| Cap dielectric | ZrO2 | ZrO2 |
| Cap height (µm) | 0.9 | 0.96 |
| tdiel (nm) | 3.0 | 3.0 |
| p+ tap (추가 cm⁻³ / 두께 µm) | 없음 | 1e19 / 0.05 |
| 공통 고정 조건 | W=0.1 µm, T=398 K, VB=-0.5 V | 동일 |

p+ tap은 background NA와 별도다. 저장 파일의 `bulk.NetDoping`에 tap이 포함된 실제 공간 분포를 기록했다. 신규 LDD/Halo 모델에 의존하지 않는다. 구조는 source contact 위 storage pillar와 양쪽 high-k slab을 유지하며 storage는 source, plate는 1 V로 연결한다.

## 요구사항과 검증

| Metric | Requirement | Baseline | Final | PASS/FAIL |
|---|---|---|---|---|
| CSTORE | ≤20 fF | 18.585 | 19.824 | PASS |
| Gate field | ≤5 MV/cm | 5.0 | 5.0 | PASS |
| Cap field | ≤4 MV/cm | 3.333 | 3.333 | PASS |
| Initial READ0 | ≥60 mV | 128.264 | 127.320 | PASS |
| Initial READ1 | ≥60 mV | 84.102 | 67.301 | PASS |
| Retention0 | ≥64 ms | ≥64 ms | ≥64.000 ms | PASS |
| Retention1 | ≥64 ms | ~2.64 ms | ≥64.000 ms | PASS |

실제 두 상태 전체 측정을 완료했다. 동일 저장 구조·입력·공용 source로 기존 공식 함수를 상태별 독립 실행했고, 완료된 원 checkpoint와 data1 결과를 provenance 대조 후 종합했다. 원 순차 실행의 미완료 상태와 원 로그는 보존했다. Raw 검증 PASS. Retention 적분 최대 변화량3/1.5 mV 비교(허용: 끝점 전압차≤3 mV, 마진차≤2 mV):

| 상태 | 64 ms Vcell 차이(mV) | 64 ms READ 마진 차이(mV) | 판정 |
|---|---|---|---|
| Data 0 | 0.635588 | 0.089621 | PASS |
| Data 1 | 0.072691 | 0.003000 | PASS |

- 공식 READ는 10 ps/0.5 ns다. 5 ps는 수치 민감도 검사로만 사용했다. 초기 READ 마진 차이는 data0 0.438562 mV/data1 0.091733 mV이며 둘 다 2 mV 이내다.
- 전류·전하, 실제 Euler update와 3/1.5 mV retention 민감도는 raw CSV로 대조한다. 원 checkpoint/metrics/log를 덮어쓰지 않는다.
- 실제 기본 간격의 초기 READ와 data1 유지/열화 READ 곡선은 [독립 HTML 비교 그래프](results/part2_optimization_20261004_202430/read_retention_comparison.html)에 저장했다. 점선은 과제 판정 기준이다.
- Fresh 제출 구조 checker: **OK**. 하나의 device, 요구 region/contact/material, physics equation 부재와 bulk 2,142개 node의 실제 NetDoping을 별도 확인했다.
- 기존 전체 tests 35개 PASS(96.243 s). 이후 비대칭 ND 범위 test를 추가한 최종 profile tests 7개 PASS(0.040 s). 이 결과를 42개의 서로 다른 test로 합산하지 않는다.

## 변경 파일과 재실행

- 새 Part 2 구현: `part2_design.py`, `part2_experiment.py`, `tests/test_part2_design.py`.
- 최종 입력/선택 구조: [part2_final.yaml](part2_final.yaml), [part2_2022142233.devsim](part2_2022142233.devsim).
- 문서: `PART2_OPTIMIZATION_LOG.md`, 이 보고서, 루트 `PLAN.md`/`PROGRESS_LOG.md`.
- 결과·source hash·실패/timeout·원 raw·검증 근거: [결과 폴더](results/part2_optimization_20261004_202430/).

루트 PowerShell에서 기존 `.conda`의 DLL 경로를 준비한 뒤 선택된 저장 구조를 다음처럼 재검증한다. `part2.py`는 top-level `body_tap`을 새 구조로 만드는 경로가 없으므로 **선택 구조를 반드시 reload**한다.

```powershell
$repoDir = (Get-Location).Path
$env:PATH = "$repoDir\.conda\Library\bin;$repoDir\.conda;$repoDir\.conda\Scripts;$env:PATH"
$env:PYTHONIOENCODING = 'utf-8'
& .\.conda\python.exe -B .\project1\part2.py --config .\project1\part2_final.yaml --reload-structure .\project1\part2_2022142233.devsim --output-dir .\project1\tmp\part2_final_recheck_new
& .\.conda\python.exe -B .\project1\check_structure_file.py .\project1\part2_2022142233.devsim
```

새 구조를 입력에서 재생성하려면 `part2_experiment.py --stage screen --config project1/part2_final.yaml --output-dir project1/tmp/part2_final_rebuild_new`를 사용한다. 그 폴더의 `part2_diagnostic.devsim`이 tap을 반영한 구조이며 기존 최종 파일을 덮어쓰지 않는다. 출력 폴더는 항상 새 이름을 사용한다.

## 남은 한계

- 64 ms는 관측 하한이다. 정확한 최대 retention이나 전역 최적 설계로 해석하지 않는다.
- data1 끝점 마진은 약60.4 mV로 기준60 mV에 가깝다. tox 전계는 상한5 MV/cm이고 CSTORE도 상한20 fF에 가깝다. 공정/mesh 변경에 대한 충분한 여유는 확보하지 못했다.
- 조교의 전체 evaluator와 별도 mesh 민감도 검사는 실행하지 않았다. Local 수치 검증과 structure checker의 통과는 구분해서 해석한다.
- 첫 audit는 PowerShell 출력의 UTF-16 BOM을 UTF-8로 읽어 중단됐다. BOM에 맞춘 reader로 수정 후 raw/구조/간격/보호 검증 PASS를 확인했다. 원 오류 로그와 구조 checker 출력은 보존했으며 수치 결과/판정은 변경하지 않았다.
- Part 1/HW1/기존 결과/공용 physics·simulator는 보존했다. Git commit/push는 수행하지 않았다.

결과 정리 시각: 2026-10-04 21:19:44 KST
