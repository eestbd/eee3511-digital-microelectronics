# Part 1 최종 후보 #10 — 공식 재검증 완료

기존 10회 탐색의 #10을 유지했다. 첫 공식 재측정에서는 구조·도핑·gate 재료를 바꾸지 않고 온도 의존 이동도·gate 기준만 공식 식에 맞췄다. #8도 통과했으나 최악 정규화 spec 여유가 #10 0.11704 / #8 0.11111이므로 기존 선택을 유지했다.

## 소자와 실제 결과

- Lg=0.6 µm, tox=4.75 nm, xj=0.1 µm, tSi=0.5 µm, source/drain 각각 0.5 µm.
- NA=2e16, ND=1e19 cm⁻³, gate=W. 같은 저장 구조로 8개 항목을 평가했다.
- Fine 간격 0.01 V, extended 3종, bias ramp 0.1 V. `config.yaml`은 fine 실행에 맞춘 재현 입력이며 당시 원 입력·CLI override는 `../candidate_10/fine/`에 보존한다.

| Spec | 결과 | 기준 | 판정 |
|---|---:|---:|---|
| Vth | 0.484848 V | 0.40…0.50 V | PASS |
| Ion | 516.138 µA/µm | ≥450 | PASS |
| Ioff | 0.012637 pA/µm | ≤1 | PASS |
| SS | 66.222 mV/dec | ≤75 | PASS |
| Ioff 398 K | 10.376 pA/µm | ≤100 | PASS |
| DIBL | 13.042 mV/V | ≤30 | PASS |
| Body effect | 0.026622 V | ≤0.08 | PASS |
| Eox | 4.211 MV/cm | ≤5 | PASS |

## 근거와 재현

- [Fine 원시 결과·실행 조건](../candidate_10/fine/metrics.json), 같은 폴더의 CSV.
- [필수 수치 검증](../candidate_10/numerical_validation.json): 간격·전류 보존·raw 재추출·fresh live/reload critical bias PASS. `grading_condition_checks_pass=true`다.
- [새 프로세스 구조 검사](checker.log), [저장 geometry 검사](../candidate_10/saved_geometry_validation.json).
- [후보/ablation 비교](../summary.json). NA ablation의 coarse Vth 상한 경계 결과는 별도 fine 검증을 완료한 것으로 주장하지 않는다.

루트 PowerShell에서 AGENTS.md의 Conda/DLL PATH를 준비한 뒤:

```powershell
& .\.conda\python.exe -B .\project1\part1.py `
    --config .\project1\results\official_20261004_155839\part1\selected\config.yaml `
    --output-dir .\project1\results\manual_part1_selected_fine
& .\.conda\python.exe -B .\project1\check_structure_file.py `
    .\project1\results\official_20261004_155839\part1\selected\part1_selected_diagnostic.devsim
```

새 output 경로를 사용한다. 원 YAML의 `part1.step_v=0.02`를 그대로 사용할 때 fine 측정에는 `--step-v 0.01`이 필요하다. `metrics.json`의 실제 sweep·command_arguments가 근거다.

## 남은 확인

공식 조건에서의 spec·필수 수치 검증·구조 self-check를 통과했다. 실제 조교 시뮬레이터 전체 실행 및 완전한 mesh convergence는 미검증이다. Double는 이번 필수 검사에서 미실행하며 과거 FAIL을 보존했다.

학번이 미확인이므로 파일은 진단명이다. 제출 전 `part1_[실제학번].devsim` 이름과 해당 OK 화면을 확정해야 한다. 보고서는 `output/pdf/part1_report_draft.pdf`의 Part 1 초안이다. Part 2는 사용자 지시로 중단했으며 완료 범위에 포함하지 않는다.
