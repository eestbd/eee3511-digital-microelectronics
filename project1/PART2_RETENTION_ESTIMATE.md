# Part 2 cell retention estimate

측정일: 2026-10-05, Asia/Seoul. 최종 #11 구조와 parameter를 그대로 사용했다.

**현재 모델의 cell retention estimate는 약67.2 ms다. 제한 상태는 data 1이다.** 기존 결과의≥64 ms는 당시 계산을 멈춘 하한이었으며, 이번에는64 ms 이후 실제 누설 적분과 재읽기를 수행해 실패 구간을 측정했다.

## 실제 측정 결과

| 항목 | 기본 적분(최대3 mV/step) | 미세 적분(최대1.5 mV/step) |
|---|---:|---:|
| Data1 마지막 통과 시각 | 67.156949 ms | 67.171761 ms |
| 그 시각의 READ 마진 | 60.002516 mV | 60.003691 mV |
| Data1 첫 실패 구간 상단 | 67.224118 ms | 67.235196 ms |
| 그 시각의 READ 마진 | 59.993549 mV | 59.995273 mV |
| Data1 구간 중간값 estimate | 67.190533 ms | **67.203479 ms** |
| Data0 확인 시각 | 72.597648 ms | 72.597648 ms |
| Data0 확인 시각의 READ 마진 | 116.674533 mV | 116.763318 mV |

두 data1 estimate의 차이는0.012945 ms(약0.0193%)로 사전에 정한≤1% 기준 안이다. 각각의 실패 구간 상대폭은0.099918%/0.094348%로0.1% 이하이다. 두 적분 설정의 전체 위치 범위를 합치면 약67.156949~67.235196 ms다. 이는 적분·구간 탐색에 대한 수치 확인이며 모든 물리/mesh 오차를 포함하는 confidence interval은 아니다.

Data0는 data1 실패 구간보다 긴72.5976 ms까지 실제 통과했다. 따라서 두 저장 상태 중 먼저 실패하는 cell retention을 약67.2 ms로 보고할 수 있다. **Data0 자체의 최대 retention은 이번에도 찾지 않았다.** Data0의 값을67.2 ms 또는72.5976 ms의 정확한 최대 시간이라고 적지 않는다.

## 측정 방법과 조건

- 최종 `part2_2022142233.devsim` SHA256은 `f2442ee257af6dfcb610db5928d0ff5d3b8e5bce1d2423d72e00c7fb099fe62e`이며 이전 기본/미세 측정과 동일하다. `part2_final.yaml`, physics·설계 source, Part1/HW1·과거 CSV/JSON·PDF를 변경하지 않았다.
- T398 K, VB−0.5 V, extended_solver/model/equation=true, ramp0.1 V, W0.1 µm, CSTORE19.824 fF, CBL100 fF 조건이다.
- READ는 BL초기1 V·WL2.5 V·dt10 ps·0.5 ns이며 |VBL−1|≥60 mV를 통과 기준으로 사용했다. Holding은 WL0, data1 BL0/data0 BL2다.
- 과거 `combined_final/combined_fine`의64 ms 마지막 Vcell을 각각 fresh load로 재현했다. CSTORE를 재추출하고64 ms READ 마진이 이전 값과 일치함을 확인한 뒤 이어 계산했다. Seed 재현 허용차는0.05 mV이며 실제 차이는 부동소수점 반올림 수준이다.
- Holding은 기존과 같은 signed source current×W를 한 번 적용하고 Euler 적분했다. 최대ΔV3/1.5 mV·최대dt8 ms, 정기 재읽기를 유지했다. 최초 sampled failure 구간을 같은 누설 재적분과 실제 READ bisection으로 상대폭≤0.1%까지 좁혔다. 마진/누설을 직선 외삽한 결과가 아니다.
- Checkpoint 사이 연속적·단일 failure crossing을 가정하며 저장된 마진의 단조성을 확인했다. 정확한 수학적 시간이나 실제 조교 evaluator의 결과를 주장하지 않는다.

## Validation

모든 새 검증 PASS:

- 양 부호 상수 누설의 독립 analytic failure time 및 실패 없는 continuation3건.
- Fresh64 ms READ 재현, source/config/구조 hash·CSTORE 대조.
- 네 측정의 실제 continuation CSV 유한값·시간/ΔV 제한·signed Euler, 모든 재읽기의50step·전류/전하 보존·전압 갱신·최종 margin.
- 실제 실패 bracket 양끝의 통과/실패, refinement 재적분, 구간폭≤0.1%, 기본/미세 estimate 차이≤1%.
- 기존592개 보호 파일 hash·staged 상태·기존 progress log byte prefix 보존.

## 근거 및 재현

새 결과는 [retention_estimate_20261005_111911](results/retention_estimate_20261005_111911/validation.json)에 보존했다. 각 `primary_bit1/fine_bit1/primary_bit0/fine_bit0` 폴더에 metrics·continuation.csv·read_*.csv·refinement·native log가 있다. Native log는 gitignore되지만 로컬에는 유지한다.

기존 Conda interpreter와 DLL PATH를 준비한 뒤, 새 빈 output 경로를 사용한다. 실제 실행 script는 `results/retention_estimate_20261005_111911/measure.py`다.

```powershell
& .\.conda\python.exe -B .\project1\results\retention_estimate_20261005_111911\measure.py --selftest
# 각 명령의 output은 기존 결과와 다른 새 경로여야 한다.
& .\.conda\python.exe -B .\project1\results\retention_estimate_20261005_111911\measure.py --phase primary --bit 1 --output .\project1\tmp\retention_repeat\primary_bit1
& .\.conda\python.exe -B .\project1\results\retention_estimate_20261005_111911\measure.py --phase fine --bit 1 --output .\project1\tmp\retention_repeat\fine_bit1
& .\.conda\python.exe -B .\project1\results\retention_estimate_20261005_111911\measure.py --phase primary --bit 0 --stop-time 0.07259764773458156 --output .\project1\tmp\retention_repeat\primary_bit0
& .\.conda\python.exe -B .\project1\results\retention_estimate_20261005_111911\measure.py --phase fine --bit 0 --stop-time 0.07259764773458156 --output .\project1\tmp\retention_repeat\fine_bit0
& .\.conda\python.exe -B .\project1\results\retention_estimate_20261005_111911\audit.py
```

Audit는 이번에 저장한 측정 폴더를 검사한다. 위 재측정용 scratch 폴더는 별도 증거이므로 재측정 결과를 검토할 때는 대상을 명시해서 확인해야 한다.

최소64 ms 조건은 계속 PASS다. 독립 mesh 민감도·조교 전체 evaluator·data0 단독 최대 시간·최종 보고서 반영은 이번 추가 측정과 별도 범위다.
