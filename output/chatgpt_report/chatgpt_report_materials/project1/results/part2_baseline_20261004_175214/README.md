# Part 2 초기 소자: 전체 baseline 및 수치 검증

이번 결과는 기존 소자의 측정·검증이며 재설계/최적화 결과가 아니다.

- 측정 완료: True; spec PASS: False; 수치 검증 PASS: True.
- 고정 조건: T=398 K, VB=-0.5 V, Lg=0.3 µm, W=0.1 µm, WL high=2.5 V, dt=10 ps, BL precharge=1 V, CBL=100 fF.
- 소자: TaN, tox=5 nm, xj=0.05 µm, tSi=0.3 µm, S/D 각각 0.2 µm, NA=7e16/ND=1e19 cm⁻³.
- Capacitor: ZrO2, h=0.9 µm, tdiel=3 nm, source 위 두 dielectric slab.

| 항목 | 결과 | 요구 기준 | 판정 |
|---|---:|---:|---|
| Data 0 retention | ≥64 ms | ≥64 ms | PASS |
| Data 1 retention | 2.62732…2.64281 ms | ≥64 ms | FAIL |
| CSTORE | 18.585 fF | ≤20 fF | PASS |
| Gate 전계 | 5 MV/cm | ≤5 MV/cm | PASS |
| Capacitor 전계 | 3.33333 MV/cm | ≤4 MV/cm | PASS |
| Data 0 초기 READ | 128.264 mV | ≥60 mV @0.5 ns | PASS |
| Data 0 마지막 sampled 재READ (64 ms) | 102.578 mV | ≥60 mV | PASS |
| Data 1 초기 READ | 84.1016 mV | ≥60 mV @0.5 ns | PASS |
| Data 1 마지막 sampled 재READ (2.72 ms) | 59.095 mV | ≥60 mV | FAIL |

## 이번 실패의 원인

- Data1의 signed storage current는 처음 2.9877 pA, 첫 failed sample 직전 2.45545 pA다. 누설로 Vcell이 2→1.604 V로 떨어졌고 재READ 마진이 60 mV 아래로 내려갔다.
- 간격을 줄여도 같은 FAIL이며 저장 구조의 fresh off-current와 실패 bracket 양쪽 READ도 재현됐다. 이번 결과는 수렴 실패가 아닌 기존 초기 소자의 data1 유지시간 부족이다.
- 다음 보완 판단의 우선 대상은 data1 누설/retention이다. 치수·도핑·재료·solver·모델을 바꾼 추가 설계 탐색은 이번에 수행하지 않았다.

## 어떻게 이해하면 되나

- 초기 READ는 막 저장한 0/2 V를 0.5 ns 안에 구분할 수 있는지 확인한다.
- Retention은 누설로 변한 Vcell에서 같은 READ를 다시 수행한다. 64 ms에서 두 마진이 60 mV 이상인지가 핵심이다.
- 64 ms까지 실패가 없으면 retention ≥64 ms라는 하한이다. 실제 실패 시각이나 최대 retention time을 계산한 것은 아니다.

## 수치 검증

- 기존 29 tests PASS; structure-only fresh checker 및 실제 geometry/naming 검사.
- CSTORE: plate charge dQ/dV, 10/5 mV perturbation 및 기하 추정 비교.
- READ: 공식 10 ps/비교 5 ps, raw signed 전류·폭·Euler update·전하 보존 재계산.
- Retention: 최대 Vcell step 3/1.5 mV 및 8 ms 시간 상한 비교. 각 checkpoint와 64 ms에서 열화 상태의 READ를 수행.
- 저장된 같은 구조를 새 Python 프로세스에서 로드하여 초기 READ 0/1, data0 64 ms 및 data1 실패 bracket 양쪽 READ와 4개 off-current 중요점 재현.

- Data 0 같은 64 ms 끝점 비교: Vcell 차이=0.716441 mV, 재READ 마진 차이=0.0975613 mV; 기준 3/2 mV 및 판정 일치 — PASS.
- Data 1 refined failure time 간격 비교: midpoint 상대 차이=0.215453% (기준≤1%) 및 FAIL 판정 일치 — PASS. 처음 실패를 발견한 raw checkpoint는 시각이 달라 끝점 전압 차이를 같은 시간의 오차로 사용하지 않는다.

## 근거·그래프·재현

- [기본 raw/실행 조건](primary/metrics.json), [미세 raw/실행 조건](retention_fine/metrics.json), [독립 raw 비교·보호 검증](validation.json), [fresh replay](fresh_replay/validation.json), [구조 검사](primary/checker.log).
- [READ/retention 곡선](curves.html). 진한/점선은 기본/미세 간격이며 READ ±60 mV·retention 60 mV 기준선을 표시했다.
- AGENTS의 Conda/DLL PATH를 준비한 뒤 새 output 경로를 사용한다:

```powershell
& .\.conda\python.exe -B .\project1\part2.py --config .\project1\part2_initial.yaml --output-dir .\project1\results\manual_part2_baseline
& .\.conda\python.exe -B .\project1\part2.py --config .\project1\part2_initial.yaml --output-dir .\project1\results\manual_part2_fine --retention-delta-v 0.0015
```

## 남은 한계·다음 판단

- Gate 전계는 정확히 상한 5 MV/cm이며 추가 설계 여유는 없다. 초기/열화 READ의 가장 작은 마진과 retention 하한을 함께 보고 보완 필요성을 판단한다.
- Checkpoint 사이 단일 failure crossing을 가정한다. 관측값의 단조성은 검사했지만 연속 시간의 모든 지점을 측정한 것은 아니다.
- Full mesh convergence와 실제 조교 시뮬레이터 전체 실행은 미검증이다. 공식 조건에서의 로컬 결과와 채점 보장을 구분한다.
- 현재 파일은 진단 이름이다. 실제 학번 제출 파일/OK 화면과 Part 1+2 최종 보고서는 마지막 단계에 남긴다.
- 이번에는 설계 변수 탐색을 하지 않았다. 이후 개선 여부·대상·실험 예산은 사용자 검토 후 정한다.
