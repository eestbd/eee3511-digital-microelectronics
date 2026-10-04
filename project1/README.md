# Project 1

HW1의 DEVSIM 시뮬레이터를 확장한 MOSFET 설계 프로젝트다. 현재 Part 1의 nMOS 측정·설계 탐색·검증 도구가 구현되어 있다. 과제 요구사항은 `Project1_Assignment_0927.pdf`를 기준으로 한다.

## 파일 안내

| 파일/폴더 | 역할 |
|---|---|
| `mosfet_tool/` | 실제 시뮬레이터: 설정, mesh/doping, 물리 모델, 측정, 공통 workflow |
| `part1.py` | 하나의 소자에서 Part 1의 8개 spec 측정·구조/CSV/JSON 저장 |
| `part1_baseline.yaml` | Part 1의 원래 baseline 입력. 최적화 후보와 구분한다. |
| `PART1_BASELINE.md` | baseline 모델·측정 정의·검증 방법·물리 가정 설명 |
| `part1_experiment.py` | 순차 설계 실험의 입력·횟수·실패·source hash 보존 |
| `validate_part1.py` | 동일 소자의 간격 비교·전류 보존·정밀도·fresh reload 검증 |
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

두 선정 후보는 현 모델의 8개 spec과 extended 수치 검증을 통과했다. **Double 전체 검증은 실패가 남아 있으며 최종 설계 확정은 아직 아니다.** Mesh convergence와 조교 모델 일치도 미확인이다. 폴더 정리는 이 수치 문제를 해결하는 작업과 별개다.

과거 결과의 입력·source hash·판정은 실제 당시 실행 기록이므로 보존한다. 다시 측정할 때는 새 경로에 저장한다.
