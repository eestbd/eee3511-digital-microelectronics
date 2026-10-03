# AGENTS.md

## 목적과 작업 범위

이 저장소는 Python으로 MOSFET의 I–V·C–V를 계산하는 교육용 프로젝트다. HW1의 square-law/DEVSIM/Streamlit 구현을 기반으로 Project 1의 nMOS와 향후 1T1C DRAM 설계를 진행한다.

- 기능 개발의 기본 대상은 `project1/`이다. `hw1/`은 완료된 reference이므로 수정·이동·삭제하지 않는다. 비교와 필요한 읽기 전용 실행은 가능하다.
- 루트 `AGENTS.md`는 작업 규칙, `PLAN.md`는 현재 계획·상태, `PROGRESS_LOG.md`는 시간순 누적 이력을 관리한다. 다른 파일의 변경은 해당 요청 범위에 맞게 결정한다.
- 사용자 지시와 현재 요청 범위를 우선한다. 조사·문서 작성 요청을 feature 구현이나 parameter optimization 승인으로 확대하지 않는다.
- Level 1: 단일 agent가 작업한다. Multi-agent orchestration, 외부 agent framework, 복잡한 자동화 시스템은 도입하지 않는다.

## 기본 workflow

여러 파일·행동 변경·physics·수치 계산·실행 경로에 영향을 주거나 조사가 필요한 작업은 비자명한 작업으로 취급한다. 다음 순서로 진행한다. 단순 오탈자 수정 등에는 불필요한 계획 절차를 늘리지 않되, 관련 검증과 최종 확인은 수행한다.

1. 코드를 수정하기 전에 문제, 최종 목표, 요청 범위와 완료 조건을 이해한다.
2. 관련 기존 코드·설정·문서를 조사한다. 검색은 `rg`/`rg --files`를 우선하고, 실제 파일·함수·호출 흐름을 확인한다.
3. 구현 전에 최근 관련 `PROGRESS_LOG.md` 기록을 확인하고, 루트 `PLAN.md`의 Goal, Current State, Requirements, Plan, Validation을 현재 작업에 맞게 작성하거나 갱신한다.
4. 불명확한 내용은 코드와 문서부터 확인한다. 합리적으로 판단한 가정은 근거와 함께 Assumptions에 남기고, 확인되지 않은 사실은 `확인 필요`로 표시한다.
5. 계획을 작고 구체적인 milestone checklist로 나눈다. 각 milestone의 결과와 검증 방법을 정한다.
6. 기존 구조를 활용하며 한 번에 하나의 논리적인 milestone을 구현한다. 목적과 무관한 refactoring·architecture 변경·의존성 추가를 피한다.
7. 의미 있는 변경마다 범위에 맞는 test 또는 validation을 수행한다. 명령, 입력 조건, 결과와 미실행 이유를 기록한다. 의미 있는 milestone 완료와 중요한 검증 결과는 `PROGRESS_LOG.md`에도 append한다.
8. 실패나 예상 밖 결과가 나오면 재현 조건과 root cause를 조사한다. 출력 값·허용 오차·solver 설정을 바꿔 실패를 숨기지 않는다.
9. 발견한 사실, 실패 원인, 변경된 범위와 계획 수정 이유를 PLAN의 Progress / Discoveries에 남긴다. 중요한 발견·문제·계획 변경은 `PROGRESS_LOG.md`에 새 기록으로 추가한다. 가정이 틀렸으면 Requirements·Assumptions·Plan·Validation도 수정한다.
10. 승인된 범위에서 다음 milestone으로 계속 진행한다. 계획만 쓰고 관례적으로 "진행할까요?"를 묻고 멈추지 않는다.
11. 구현 후 전체 diff를 다시 읽고 아래 Final review 기준으로 최초 요구사항과 결과를 비교한다.
12. 검토에서 발견한 문제를 직접 수정하고, 필요한 경우 계획도 갱신한다.
13. 수정된 경로의 test/validation과 필요한 회귀 검증을 다시 실행한다. 통과 후 추가 변경·실패·불확실성이 없다면 불필요하게 반복하지 않는다.
14. 종료 전에 `PLAN.md`의 checklist, 상태, 실제 validation, limitation, Final Review를 최종 결과와 일치시키고 `PROGRESS_LOG.md`에 최종 기록을 반드시 append한다. 두 문서의 완료 범위·남은 작업·검증 결과가 일치하는지 확인한다. 실행 성공만으로 완료 처리하지 않는다.
15. 사용자에게 실제 변경, 요구사항 충족 여부, 검증 결과와 남은 한계를 간단히 보고한다.

질문은 올바른 구현에 필수인 사용자 결정, 결과를 크게 바꾸지만 저장소에서 판단 근거를 찾을 수 없는 선택, destructive/irreversible 작업에 한정한다. 필수 답변을 기다릴 때도 독립적으로 가능한 조사·검증은 계속한다. 명시적으로 분석이나 승인 전 계획만 요청된 단계에서는 그 범위를 지킨다.

## PLAN.md 운영

- 필수 section: `Goal`, `Current State`, `Requirements`, `Assumptions`, `Plan`, `Validation`, `Progress / Discoveries`, `Final Review`.
- 새 비자명한 작업 시작, milestone 종료, 실패·새 발견·방향 전환, 최종 review 뒤에 갱신한다. 중요한 결정과 실행 상태를 대화에만 남기지 않는다.
- checkbox는 실제 완료된 milestone만 체크한다. 실패·미검증·blocking 사유를 완료로 표시하지 않는다.
- 새 작업에서는 이전 Goal과 완료 checklist를 현재 작업에 맞게 교체한다. 유효한 발견만 간결하게 보존하며 날짜, 근거 경로, 다음 동작을 기록한다.
- 미래 아이디어나 기존 미완성 기능을 현재 승인된 작업으로 자동 편입하지 않는다. 문서를 불필요한 전체 backlog나 반복 로그로 키우지 않는다.
- 현재 상태와 간결한 발견은 PLAN에, 시간순 작업 이력은 PROGRESS_LOG에 남긴다. PLAN을 새 작업으로 갱신해도 기존 로그는 그대로 보존한다.

## PROGRESS_LOG.md 운영

- Non-trivial task의 의미 있는 milestone 완료, 중요한 발견·문제, 계획 변경, 작업 종료 때 루트 `PROGRESS_LOG.md`의 맨 아래에 새 기록을 추가한다. 사소한 한 줄 수정마다 기록하지 않으며, 같은 시점의 관련 사건은 한 기록으로 묶을 수 있다.
- Append-only: 기존 기록과 표제를 수정·삭제·덮어쓰거나 순서를 바꾸지 않는다. 로그 전체를 재작성하거나 formatter로 과거 내용을 변경하지 않는다. 오류 정정은 원래 기록 시각·정정 내용·이유를 포함한 새 기록으로 남긴다.
- 기록 시각은 실제 현재 시각을 확인해 `Asia/Seoul (KST, UTC+9)`로 변환한다. 실행 호스트의 로컬 시간대에 의존하거나 과거 시각을 추측하지 않는다. 표제에는 날짜·시·분·초와 KST를 명시한다.
- 각 기록은 수행한 작업, 현재까지 완료된 내용과 남은 범위, 중요한 발견/문제, 다음 작업을 포함한다. 이슈가 없으면 없다고 명시한다. 작업을 구분할 수 있는 목표나 milestone 이름을 넣는다.
- 계획 변경 기록에는 변경 이유와 영향, 중요한 test/validation에는 명령·조건·결과 또는 미실행 이유를 남긴다. 완료되지 않은 검증을 통과한 것으로 기록하지 않는다.
- 작업 종료의 최종 기록에는 완료 범위, 실제 검증 결과, 남은 한계·미완료 사항, 다음 작업을 명시한다. 다음 작업이 없다면 현재 요청이 완료되었고 다음 요청을 기다리는 상태라고 기록한다.
- 기록 전 최신 PLAN과 로그의 끝을 확인하고, 기록 후 이전 byte prefix가 보존되었는지와 날짜 순서·현재 상태의 일치를 검토한다. 현재 상태가 바뀌면 PLAN도 갱신한다. 과거 당시의 상태와 새로운 상태가 다른 것은 모순이 아니다.
- 로그는 이번 도입부터 누적한다. 이전 이력을 회고할 경우 회고임을 밝히고 확인된 사실만 쓰며, 정확한 수행 시각을 알 수 없는 과거 작업의 timestamp를 만들어내지 않는다.

기본 기록 형식은 다음과 같다. 실제 로그에는 확인한 시각과 작업 내용으로 채운다.

```markdown
## YYYY-MM-DD HH:mm:ss KST

### 수행한 작업

- 수행한 작업과 milestone.

### 현재 상태

- 완료된 내용과 아직 남은 범위.

### 발견 / 이슈

- 발견·문제·계획 변경 이유·중요한 validation 결과. 없으면 없음.

### 다음 작업

- 다음에 진행할 승인된 작업 또는 현재 요청 완료·다음 요청 대기.
```

## 저장소 탐색과 convention

| 경로 | 역할 |
|---|---|
| `project1/mosfet.py` | CLI: `idvg`, `idvd`, `cv`, `--config` |
| `project1/mosfet_tool/config.py`, `config.yaml` | `Device` dataclass, YAML 설정 |
| `project1/mosfet_tool/simulator.py` | mesh·doping·physics·bias·전류·전하·sweep |
| `project1/mosfet_tool/workflows.py` | CLI와 소비자가 공유하는 `run_idvg/run_idvd/run_cv/save_csv` |
| `project1/run_example.py` | simulator 직접 사용 예제 |
| `project1/compare_tcad.py`, `compare_models.py` | 소자 비교와 간이 모델 비교 |
| `project1/check_structure_file.py` | 제출 구조 self-check. 전기적 spec 검사기는 아님 |
| `hw1/step1`, `step2`, `step3`, `demo` | 간이 모델, TCAD reference, GUI, 컴파일된 demo |
| `README.md`, `hw1/MANUAL*.html`, `hw1/HW1.pdf` | 프로젝트 안내와 HW1 설명·요구사항 |
| `project1/Project1_Assignment_0927.pdf` | Project 설계·제출 요구사항 |

Python은 4-space indentation, `snake_case` 함수·변수, `PascalCase` 클래스, 단위가 드러나는 식별자, dataclass·type hint·`pathlib.Path`를 사용하는 기존 패턴을 따른다. UTF-8과 기존 한국어 docstring·주석 스타일을 유지한다. 주석은 동작 이유·물리 가정·단위 변환을 설명한다.

기존 CLI mode, config 기본값, workflow API와 DataFrame 열 이름(`Vg_V`, `Vd_V`, `Id_A_per_um`, `Cgg_F_per_um`)을 보존한다. 호환성을 바꾸는 작업이면 영향과 이유를 계획·검증에 명시한다. 저장소에는 formatter/linter/test framework 설정이 없으므로 작업과 무관한 도구 도입을 기본 변경에 섞지 않는다.

매뉴얼은 starter 코드와 옛 폴더 배치를 설명할 수 있다. 현재 구현 여부·경로는 실제 코드로 확인하고, 과제 요구사항은 해당 PDF와 checker로 대조한다. 근거 없이 helper 동작이나 물리 모델을 추측하지 않는다.

## 실행과 validation

별도 source build 단계는 없다. `environment.yml`의 로컬 Conda 환경을 사용한다. `.conda`가 없다면 설치가 필요한 작업에서 저장소 루트의 Anaconda Prompt로 `conda env create --prefix .\.conda --file environment.yml`을 사용한다. 기존 환경이 있으면 재생성하지 않는다. Windows에는 매뉴얼의 Visual C++ x64 런타임과 DEVSIM DLL 경로가 필요하다.

저장소 루트의 PowerShell에서 다음으로 경로를 준비한다. 시스템 Python 대신 저장소 interpreter를 사용한다.

```powershell
$repoRoot = (Get-Location).Path
$pythonExe = Join-Path $repoRoot '.conda\python.exe'
$mosfetCli = Join-Path $repoRoot 'project1\mosfet.py'
$configFile = Join-Path $repoRoot 'project1\config.yaml'
$env:PATH = "$repoRoot\.conda\Library\bin;$repoRoot\.conda;$repoRoot\.conda\Scripts;$env:PATH"
$env:PYTHONIOENCODING = 'utf-8'
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
& $pythonExe -B $mosfetCli --help
```

CLI·config·simulation 변경의 기본 회귀 검증은 기존 설정으로 세 가지 해석을 실행하는 것이다. `mosfet.py`의 CSV는 현재 작업 디렉터리에 생성되므로 기존 결과를 덮어쓰지 않도록 별도 scratch 디렉터리를 사용한다.

```powershell
$validationDir = Join-Path $repoRoot 'project1\tmp\validation'
New-Item -ItemType Directory -Path $validationDir -Force | Out-Null
Push-Location -LiteralPath $validationDir
try {
    foreach ($mode in @('idvg', 'idvd', 'cv')) {
        & $pythonExe -B $mosfetCli $mode --config $configFile *> "$mode.log"
        if ($LASTEXITCODE -ne 0) { throw "$mode failed; inspect $mode.log" }
    }
} finally {
    Pop-Location
}
```

- 현재 기본 config/default에서 Id–Vg·Id–Vd는 각각 21점, C–V는 31점이다. 필요한 열·bias·단위·유한값, 끝점과 합리적인 물리 경향을 확인한다. 요구된 변화와 허용 오차를 사전에 정해 baseline과 비교한다.
- 현재 전류는 A/µm, 정전용량은 F/µm이다. C–V는 전류 수송을 켜지 않고 평형 gate charge를 미분한다. 2점 이상과 유효한 전압 간격이 필요하다.
- 순수 measurement logic·새 동작·bug 수정에는 독립적인 기대값과 의미 있는 edge case를 검증한다. 필요하면 `project1/` 내부에 가벼운 test를 추가한다. 구현을 그대로 반복하는 test나 저위험 문서 변경용 형식적 test는 만들지 않는다.
- 제출 구조 변경은 새 Python 프로세스에서 `check_structure_file.py`로 실제 저장 파일을 다시 로드한다. 준비한 `$pythonExe`로 `& $pythonExe -B .\project1\check_structure_file.py .\project1\part1_[studentID].devsim`을 실행하며 실제 학번·파일 경로를 넣는다. 진단용 파일의 이름을 제출 파일로 오인하지 않는다.
- GUI가 관련된 작업에는 첫 화면, 해석 선택, 입력 변경과 이전 결과 표시, 버튼 실행, 오류 처리·session state를 확인한다. 기존 GUI reference의 직접 실행은 `& $pythonExe -B -m streamlit run .\hw1\step3\my_app.py --server.headless true`다. 검증 때문에 `hw1/`이나 GUI 대상 범위를 바꾸지 않는다.
- 구문/import 검사, simulation 정상 종료, 구조 checker 통과, 물리 정확성·spec 충족은 서로 다른 증거다. 필요한 검증이 불가능하면 정확한 원인과 미검증 범위를 PLAN에 남긴다.
- 문서만 바꾼 경우 링크·명령·내용·diff를 검증한다. 관련 코드가 바뀌지 않았다면 전체 TCAD/GUI 실행을 반복하지 않는다.

`project1/STEP2_*.bat`는 루트 `.conda`를 가리킨다. HW1 launcher는 현재 없는 `hw1/.conda`를 기대하므로 보호된 배치 파일을 수정하지 않고 실제 interpreter 경로를 사용한다. `compare_models.py`는 import 경로 문제와 스크립트 폴더 고정 출력 경로가 있다. 실행 전 이를 확인하고 기존 결과물 보호 방법을 정한다.

## 물리·제출 제약

- Mobility 상수나 ramp/solver setting을 spec 통과 목적으로 임의 조정하지 않는다. 근거 있는 physical model로 대체하는 작업은 모델·계수·검증 결과를 명시한다.
- 설계 탐색·최종 소자 설계는 해당 요청 범위에서 수행한다. 원본 baseline과 실제 실행 조건을 보존하고 변경한 변수를 기록한다.
- 내부 길이는 cm이며 `UM=1e-4`, `NM=1e-7`이다. 실리콘 표면 y=0, bulk는 y>0, oxide는 y<0, source는 왼쪽, drain은 오른쪽, gate는 planar 배치를 지킨다.
- `.devsim`은 `_build_doping()` 뒤, `_build_physics()` 전에 저장한다. mesh·regions·contacts·interfaces·doping·materials만 포함하며 physics equation·bias·결과는 포함하지 않는다.
- Part 1 고정 이름: `bulk`/`Silicon`, `oxide`/`Oxide` 또는 `SiO2`, `gate_metal`/과제 gate 재료 이름, `gate/source/drain/body`, `bulk_oxide`, `bulk.NetDoping`. `gate` contact는 oxide에 둔다. Material은 숫자가 아니라 이름이며 허용 이름은 checker `GATE_TABLE`과 PDF를 대조한다.
- Part 1 파일은 `part1_[studentID].devsim`, device는 하나다. 학번을 추측하지 않는다. Part 1에는 capacitor 항목이 필요 없다. Part 2는 요청된 경우 해당 PDF의 별도 규칙을 조사한다.
- Part 1 범위: Lg≥0.3 µm, tox≥4 nm(SiO2), xj=0.02…0.25 µm, tSi=0.3…2 µm, source/drain 각각 0.2…1 µm, NA=1e14…1e17, ND=1e18…1e21 cm⁻³.

VDD=2 V, 기본 T=300 K, VS=VB=0 V이며 같은 구조·doping·gate 재료로 아래 항목을 평가한다. 고온·body effect 항목은 표의 조건으로 변경한다.

| Spec | 정의와 기준 |
|---|---|
| Vth | VD=0.05 V, ID=1e-7 A/µm의 VG, 0.40…0.50 V |
| Ion | VG=VD=2 V, ≥450 µA/µm |
| Ioff | VG=0, VD=2 V, ≤1 pA/µm |
| SS | VD=0.05 V, ID=1e-10…1e-8 A/µm 구간 평균, ≤75 mV/dec |
| 고온 Ioff | VG=0, VD=2 V, T=398 K, ≤100 pA/µm |
| DIBL | VD=0.05/2 V에서 각각 ID=1e-7 A/µm로 추출한 `(Vth_low - Vth_high)/1.95`, ≤30 mV/V. V 단위 계산을 mV/V로 환산 |
| Body effect | VD=0.05 V, `Vth(VB=-0.5)-Vth(VB=0)`, ≤0.08 V |
| Eox | `VDD/tox`, ≤5 MV/cm. cm 단위로 환산 |

DEVSIM은 프로세스 전체 상태를 공유하며 현재 `build()`는 이전 device/mesh를 모두 삭제한다. 여러 simulator를 살아 있는 독립 상태로 가정하지 않는다. 작은 전류의 정확성은 수렴 메시지 외에 전류 보존·단위·모델·재현성도 확인한다. Mesh 변경은 현재 doping 감쇠 길이에 영향을 주므로 순수 numerical 변경으로 단정하지 않는다.

## Final review 기준

- 최초 요구사항과 완료 조건을 실제로 충족했는가? 각 중요한 요구사항에 검증 근거가 있는가?
- Bug·예외·실패 시 상태 문제가 있는가?
- CLI·config·workflow·결과 단위·기존 I–V/C–V에 regression을 만들었는가?
- 경계값·잘못된 입력·비유한 값·빈 결과·수렴 실패 등 관련 edge case를 검토했는가?
- 불필요한 복잡성·refactoring·인프라·의존성이 추가되었는가?
- 기존 구조와 convention, 변경 범위·reference 보호·제출 규약을 지켰는가?
- 필요한 validation/test를 실행했는가? 미실행 항목·불확실성·한계가 정확히 기록되었는가?
- PLAN의 최종 상태와 최신 PROGRESS_LOG 기록이 일치하고, 이전 로그 보존과 작업 종료 기록을 확인했는가?

문제를 발견하면 수정하고 관련 검증을 다시 수행한다. 완료 보고는 실제 요구사항 충족과 검증 결과를 기준으로 하며, 미검증 physics나 제출용 spec을 PASS로 주장하지 않는다.
