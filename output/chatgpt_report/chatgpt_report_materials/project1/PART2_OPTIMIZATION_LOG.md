# Part 2 parameter optimization

약 60분 예산으로 실제 측정한 후보를 비교한다. Part 1과 기존 결과는 보존한다.

업데이트: 2026-10-04 21:18:41 KST

| Candidate | 변경 | Read0 mV | Read1 mV | Retention0 | Retention1 | CSTORE fF | Reliability | 판정 |
|---|---|---:|---:|---|---|---:|---|---|
| B0 baseline | 기존 검증 결과 재사용 | 128.264 | 84.102 | ≥64 ms PASS | 2.627~2.643 ms FAIL | 18.585 | PASS | FAIL |
| 01_gate_W | {"gate_material": "W"} | 123.109 | 67.391 | 미측정 | 40.11~40.51 ms FAIL | 18.585 | PASS | DATA1 FAIL |
| 02_gate_TiN | {"gate_material": "TiN"} | 121.175 | 61.373 | 미측정 | 20.71~20.84 ms FAIL | 18.585 | PASS | DATA1 FAIL |
| 03_body_1e17 | {"body_doping_cm3": 1e+17} | 125.798 | 76.409 | 미측정 | 미측정 | 18.585 | PASS | SCREEN PASS/retention 미검증 |
| 04_junction_003 | {"junction_depth_um": 0.03} | 126.808 | 80.011 | 미측정 | 미측정 | 18.585 | PASS | SCREEN PASS/retention 미검증 |
| 05_W_cap096 | {"gate_material": "W", "capacitor.height_um": 0.96} | 127.371 | 67.750 | 미측정 | 64ms 끝점 FAIL / 최초 실패 미측정 | 19.824 | PASS | 64ms ENDPOINT FAIL |
| 06_W_channel_split | {"gate_material": "07_TiN_channel_split", "doping_profile": {"source_side_na_cm3": 1000000000000000.0, "drain_side_na_cm3": 7e+16, "split_fraction": 0.5}} | 미측정 | 미측정 | 미측정 | 미측정 | 미측정 | 미측정 | ERROR |
| 07_W_channel_split | {"gate_material": "W", "doping_profile": {"source_side_na_cm3": 1000000000000000.0, "drain_side_na_cm3": 7e+16, "split_fraction": 0.5}} | 126.250 | 77.307 | 미측정 | 미측정 | 18.585 | PASS | SCREEN PASS/retention 미검증 |
| 08_TiN_channel_split | {"gate_material": "TiN", "doping_profile": {"source_side_na_cm3": 1000000000000000.0, "drain_side_na_cm3": 7e+16, "split_fraction": 0.5}} | 124.450 | 71.640 | 미측정 | 미측정 | 18.585 | PASS | SCREEN PASS/retention 미검증 |
| 09_W_channel_5e16_1e17 | {"gate_material": "W", "capacitor.height_um": 0.96, "doping_profile": {"source_side_na_cm3": 5e+16, "drain_side_na_cm3": 1e+17, "split_fraction": 0.5}} | 126.676 | 66.169 | 미측정 | 64ms 끝점 FAIL / 최초 실패 미측정 | 19.824 | PASS | 64ms ENDPOINT FAIL |
| 10_W_channel_3e16_1e17 | {"gate_material": "W", "capacitor.height_um": 0.96, "doping_profile": {"source_side_na_cm3": 3e+16, "drain_side_na_cm3": 1e+17, "split_fraction": 0.5}} | 127.603 | 68.917 | 미측정 | 64ms 끝점 FAIL / 최초 실패 미측정 | 19.824 | PASS | 64ms ENDPOINT FAIL |
| 11_W_cap096_bodytap | {"gate_material": "W", "capacitor.height_um": 0.96, "body_tap": {"additional_acceptor_cm3": 1e+19, "thickness_um": 0.05}} | 127.320 | 67.301 | ≥64 ms PASS | ≥64 ms PASS | 19.824 | PASS | PASS |
| 12_TiN_sourceND1e21 | {"gate_material": "TiN", "capacitor.height_um": 0.96, "doping_profile": {"source_side_na_cm3": 7e+16, "drain_side_na_cm3": 7e+16, "split_fraction": 0.5, "source_nd_cm3": 1e+21, "drain_nd_cm3": 1e+19}} | 132.315 | 67.914 | 미측정 | 64ms 끝점 FAIL / 최초 실패 미측정 | 19.824 | PASS | 64ms ENDPOINT FAIL |

## 기록 원칙

- B0는 이전 검증 결과다. 새 후보는 해당 input.yaml·변경 값·metrics/raw CSV·구조/checker·실패 로그를 새 폴더에 보존한다.
- 초기 READ/hard constraint FAIL은 retention을 실행하지 않고 제외한다. 미측정은 PASS로 대신하지 않는다.
- Data1 screening PASS는 전체 PASS가 아니다. 최종 후보는 기존 part2.py 및 동일 cell.retention의 독립 상태 측정을 검증한다. 종합 결과에는 원 checkpoint/source/config provenance를 남긴다.
- Retention ≥64 ms는 관측 하한이며 실제 최대 유지시간이 아니다. 조교 시뮬레이터 전체 실행도 별도 확인 대상이다.

## 결과 위치

- 세션·비교 CSV·후보 raw: project1/results/part2_optimization_20261004_202430/

## 후보 해석

- B0 baseline: 초기 READ는 충분하나 data1 누설/retention이 병목.
- 01_gate_W: 누설은 감소했지만 실제 retention 약40.3 ms로 부족.
- 02_gate_TiN: 누설 최저여도 초기 READ 여유가 작아 약20.8 ms에 실패.
- 03_body_1e17: 누설 감소는 gate 후보보다 작아 후속 retention을 생략.
- 04_junction_003: 누설 개선이 작아 후속 retention을 생략.
- 05_W_cap096: 용량 증가만으로 64 ms READ 기준을 만족하지 못함.
- 06_W_channel_split: 입력 생성 오류로 native 측정 전 중단. 물리 후보 수에서 제외.
- 07_W_channel_split: 낮은 source-side NA가 body 누설을 증가시켜 제외.
- 08_TiN_channel_split: READ는 개선되지만 body 누설 증가로 제외.
- 09_W_channel_5e16_1e17: 국소 NA 조합도 64 ms 끝점 FAIL.
- 10_W_channel_3e16_1e17: 국소 NA 조합도 64 ms 끝점 FAIL.
- 11_W_cap096_bodytap: 공식 허용 p+ tap으로 body 누설 감소. 끝점 여유는 작음.
- 12_TiN_sourceND1e21: 공식 허용 S/D 비대칭이나 64 ms 마진59.145 mV로 FAIL.