# Project 1

HW1의 DEVSIM 시뮬레이터를 확장한 MOSFET 설계 프로젝트다. 현재 Part 1의 nMOS 측정·설계 탐색·검증 도구가 구현되어 있다. 과제 요구사항은 `Project1_Assignment_0927.pdf`를 기준으로 한다.

교수·조교가 확인한 모델·채점·개정 Part 2 조건과 수정 전 구현 대조는 [OFFICIAL_QA.md](OFFICIAL_QA.md)에 정리했다. 최신 PDF를 최우선으로 하며 기존 baseline 모델 설명보다 이 공식 조건을 우선한다. 공식 모델에서 Part 1 두 후보의 재검증을 완료하고 #10을 유지했다. 사용자의 “Part 1까지만” 지시에 따라 Part 2 중간 구현·결과는 보존하고 실행을 중단했다. 현재 완료 상태는 루트 PLAN/log를 참조한다.

## 파일 안내

| 파일/폴더 | 역할 |
|---|---|
| `mosfet_tool/` | 실제 시뮬레이터: 설정, mesh/doping, 물리 모델, 측정, 공통 workflow |
| `part1.py` | 하나의 소자에서 Part 1의 8개 spec 측정·구조/CSV/JSON 저장 |
| `part1_baseline.yaml` | Part 1의 원래 baseline 입력. 최적화 후보와 구분한다. |
| `PART1_BASELINE.md` | baseline 모델·측정 정의·검증 방법·물리 가정 설명 |
| `part1_experiment.py` | 순차 설계 실험의 입력·횟수·실패·source hash 보존 |
| `validate_part1.py` | 동일 소자의 간격 비교·전류 보존·정밀도·fresh reload 검증 |
| `part2.py`, `part2_initial.yaml`, `mosfet_tool/cell.py` | 1T1C 구조·plate dQ/dV·signed READ·adaptive retention 및 초기 입력 |
| `check_structure_file.py` | 저장된 `.devsim`의 제출 구조 규약 검사. 전기적 spec 검사와 별개다. |
| `mosfet.py`, `config.yaml` | 일반 Id–Vg/Id–Vd/C–V CLI와 기존 기본 설정 |
| `tests/` | 측정·물리 조건·실험 보호 조건의 unittest |
| `results/` | 기준 측정, 설계 탐색, raw CSV, 진단 구조, 검증과 실패 로그 |
| `tmp/` | Git에서 제외되는 실행 scratch·임시 진단 자료 |

작업 규칙·현재 계획·시간순 이력은 저장소 루트의 [AGENTS.md](../AGENTS.md), [PLAN.md](../PLAN.md), [PROGRESS_LOG.md](../PROGRESS_LOG.md)에서 관리한다. HW1 학습 예제와 원본 비교 스크립트는 `../hw1/`에 있다.

## 실행

저장소 루트의 PowerShell에서 기존 Conda 환경을 사용한다.

```powershell
$repoRoot = (Get-Location).Path
$pythonExe = Join-Path $repoRoot '.conda\python.exe'
$env:PATH = "$repoRoot\.conda\Library\bin;$repoRoot\.conda;$repoRoot\.conda\Scripts;$env:PATH"
$env:PYTHONIOENCODING = 'utf-8'
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)

& $pythonExe -B .\project1\part1.py --help
& $pythonExe -B .\project1\mosfet.py --help
& $pythonExe -B -m unittest discover -s .\project1\tests -v
```

환경이 없을 때의 설치 방법은 루트 `AGENTS.md`와 `environment.yml`을 참고한다. 이미 있는 환경을 재생성하지 않는다.

Part 1의 baseline을 새 경로에 측정하는 예:

```powershell
& $pythonExe -B .\project1\part1.py `
    --config .\project1\part1_baseline.yaml `
    --output-dir .\project1\results\manual_part1
```

`manual_part1`은 실행 예시 이름이다. 매번 사용하지 않은 output 경로를 지정한다. 후보를 재측정할 때는 해당 후보의 입력 YAML을 `--config`에 넣는다. 전체 측정은 시간이 걸린다.

일반 CLI는 CSV를 현재 작업 폴더에 저장한다. 별도 폴더에서 실행하면 소스 폴더에 결과가 쌓이지 않는다.

```powershell
$outputDir = Join-Path $repoRoot 'project1\tmp\manual_iv'
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
Push-Location -LiteralPath $outputDir
try {
    & $pythonExe -B (Join-Path $repoRoot 'project1\mosfet.py') idvg `
        --config (Join-Path $repoRoot 'project1\config.yaml')
} finally {
    Pop-Location
}
```

`idvg` 대신 `idvd`나 `cv`를 지정할 수 있다. 일반 CLI 실행만으로 Part 1의 8개 spec을 모두 검사한 것은 아니다.

## 현재 결과 읽기

- [기준 측정](results/part1_baseline/primary/metrics.json): 초기 소자 6 PASS/2 FAIL(Vth·Ion).
- [10회 설계 탐색 요약](results/part1_search_20261004/summary.csv): 단일 변수 4회·조합 4회·주변 2회.
- [최종 후보·검증 요약](results/part1_search_20261004/final_summary.json): 후보 #10과 #8의 fine 결과 및 정밀도별 판정.
- `results/part1_search_20261004/selected/`: 선정 후보의 입력과 진단 `.devsim`. 실제 학번이 없으므로 제출 이름이 아니다.
- `results/part1_search_20261004/validation/`: 후보별 수치 판정 JSON과 native 실패 로그.

두 선정 후보의 당시 8개 spec·extended PASS, double FAIL과 기존 JSON은 보존한다. **공식 채점은 128비트이므로 double 실패만으로 채점 탈락을 뜻하지 않는다.** 현재 varshni 경로의 고온 mobility·gate 전위식을 공지에 맞추고 새 run에서 재측정을 완료했다. 후보 #10/#8 모두 공식 coarse/fine 8개 spec과 필수 extended numerical validation을 통과했다. 최종 후보는 #10이다. Mesh convergence·실제 조교 시뮬레이터 실행 확인은 별도다.

공식 재검증 결과는 `results/official_20261004_155839/`에 있다. 이전 탐색 결과와 구분한다. `validate_part1.py`는 `grading_condition_checks_pass`로 필수 판정을 반환하고, double은 `--double-diagnostic`을 지정한 경우에만 실행한다. 미실행 double은 None이며 PASS로 바꾸지 않는다.

- [공식 Part 1 비교 결과](results/official_20261004_155839/part1/summary.json): baseline, 두 후보, Lg/NA ablation.
- [최종 후보 정리](results/official_20261004_155839/part1/selected/README.md): 8개 결과, 구조·검증 경로 및 재현 명령.
- Part 1 보고서 초안: 루트 `output/pdf/part1_report_draft.pdf`. 실제 학번과 제출용 OK 화면은 미확정이다.

Part 2는 현재 중단·미완료이며 자동으로 재개하지 않는다. 재개 요청 시 기존 환경에서 `part2.py --config project1/part2_initial.yaml --output-dir <새 경로>`를 실행할 수 있다. `--skip-retention`은 READ 진단이며 전체 PASS가 아니다. `--retention-delta-v 0.0015`는 적분 민감도 검증이다. 새 run의 input/cap/READ/retention checkpoint JSON·raw·native log·최종 metrics를 함께 확인한다. READ는 10 ps, retention은 최대 3 mV 누설 적분과 30 mV/8 ms READ checkpoint·실패 구간 재검증을 사용한다. Checkpoint 사이 단일 failure crossing 가정과 시간 bracket의 한계를 기록한다.

과거 결과의 입력·source hash·판정은 실제 당시 실행 기록이므로 보존한다. 다시 측정할 때는 새 경로에 저장한다.
