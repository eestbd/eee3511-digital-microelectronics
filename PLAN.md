# PLAN.md

현재 작업을 외부에 유지하는 living execution document다. 새 non-trivial 요청에서는 현재 목표·계획·상태를 갱신하고, 시간순 이력은 append-only `PROGRESS_LOG.md`에 보존한다.

현재 작업: Project 1 Part 1 요구사항과 구현 순서 분석
상태: 완료 (Part 1 분석만 완료, 구현·설계 탐색은 미실행)
최종 갱신: 2026-10-04 (Asia/Seoul)

## Goal

`project1/Project1_Assignment_0927.pdf`의 Part 1과 공통 제출 규칙을 읽고 현재 코드·checker와 대조하여 해야 할 일을 순서대로 정리한다. 이번 요청은 분석만 수행하며 source·config·reference·기존 결과를 수정하거나 설계 최적화를 실행하지 않는다.

## Current State

- `project1/mosfet_tool/config.py`의 Device와 `config.yaml`이 치수·도핑·온도·상수 이동도를 설정한다. `simulator.py`는 planar nMOS의 mesh·doping·Poisson·drift-diffusion과 I–V/C–V를 지원한다.
- `build()`는 mesh→doping→physics를 연속 실행한다. 구조-only 저장 경로와 `gate_metal` 영역·gate 재료 선택이 없다.
- `workflows.py`는 Id–Vg/Id–Vd/C–V를 제공하나 8개 Part 1 spec의 통합 추출·판정은 없다. Body bias는 simulator에서 설정 가능하지만 workflow 인자로 노출되지 않는다.
- `check_structure_file.py`는 구조·이름·재료·접점·계면을 검사하며 전기적 spec evaluator는 아니다.
- 기존 참고 사항: 온도는 kT/V_t에 전달되나 설치된 DEVSIM helper의 n_i·SRH 계수·mobility는 상수다. Doping erfc 감쇠 길이가 mesh 상수에 연결되어 있다.
- 기존 로그와 규칙을 읽었고 Git에는 루트 세 작업 문서만 untracked다. 분석 시작 시 tracked 파일 66개의 SHA-256과 기존 로그 byte를 확보했다.
- 현재 PDF·코드 대조와 향후 9단계 작업 순서 정리를 완료했다. 아래 제안 단계는 아직 구현한 상태가 아니다.

## Requirements

- 실제 PDF를 읽고 Part 1의 목표·설계 자유도·제약·전기적 기준·평가 조건·제출물·평가 방식을 정확히 정리한다.
- PDF 표·그림·공통 규칙을 시각적으로 대조하고 페이지 근거를 남긴다.
- 기존 코드에서 지원되는 부분과 필요한 추가 작업을 구분한다.
- 의존관계를 반영한 실행 순서와 각 단계의 완료 기준·검증 방법을 제안한다.
- PDF나 저장소로 확정할 수 없는 TA 평가 physics·학번 등은 미확인으로 명시한다.
- 이번에는 분석·PLAN 갱신·로그 append만 한다. 기능 구현·parameter 탐색·환경 변경·HW1 수정은 하지 않는다.

### Part 1 합격 기준 — PDF 실제 41/50쪽

VDD=2 V, 폭 1 µm당 수치이며 명시되지 않은 온도는 300 K다. 아래 항목 모두 같은 구조·도핑 프로파일·gate 재료로 평가한다.

| 항목 | 측정 조건·정의 | 기준 |
|---|---|---|
| Vth | VD=0.05 V, ID=1e-7 A/µm의 VG | 0.40~0.50 V |
| Ion | VG=VD=2 V, 300 K | ≥450 µA/µm |
| Ioff | VG=0, VD=2 V, 300 K | ≤1 pA/µm |
| SS | VD=0.05 V, ID=1e-10~1e-8 A/µm 구간 평균 | ≤75 mV/dec |
| 고온 Ioff | VG=0, VD=2 V, 398 K | ≤100 pA/µm |
| DIBL | VD=0.05/2 V의 정전류 Vth 차이를 1.95 V로 나눔 | ≤30 mV/V |
| Body effect | VD=0.05 V, Vth(VB=-0.5 V)−Vth(VB=0) | ≤0.08 V |
| Eox | VDD/tox, 길이는 cm로 환산 | ≤5 MV/cm |

### 설계 자유도·제출 규약 — PDF 실제 42/51, 45~48/54~57쪽

- Lg≥0.3 µm(Part 1에서는 0.3 µm 고정이 아님), tox≥4 nm·SiO2 고정, xj=0.02~0.25 µm, tSi=0.3~2 µm, source/drain 길이 각각 0.2~1 µm, NA=1e14~1e17 및 ND=1e18~1e21 cm⁻³. 구조·mesh·공간 도핑 프로파일도 설계할 수 있다.
- Gate의 유효 일함수 표(eV): n+poly 4.05, Al 4.10, Ta 4.25, Ti 4.33, TaN 4.45, W 4.60, TiN 4.65, Mo 4.70, Ni 5.10, p+poly 5.15, Pt 5.30. PDF의 poly-Si 표기는 checker의 정규화 별칭과 일치한다. 숫자가 아니라 재료 이름을 저장한다.
- Mobility·ramp 등 코드 상수와 numerical setting을 spec 통과 목적으로 임의 변경하지 않는다. 근거 있는 물리 모델로 상수를 대체하는 것은 허용한다. PDF는 수렴 문제에 128-bit 확장 정밀도를 별도로 안내한다.
- 고정 항목: bulk/Silicon, oxide/Oxide 또는 SiO2, gate_metal/표의 gate 재료, gate/source/drain/body, bulk_oxide, bulk.NetDoping. gate contact는 oxide 윗면에 붙이며 gate_metal은 방정식 없는 재료 라벨이다. 소스 왼쪽·드레인 오른쪽·평탄 gate, 실리콘 표면 y=0 규약을 유지한다. Part 1에는 hk/storage/plate가 필요 없다.
- mesh·영역·접점·계면·doping만 저장한다. _build_doping() 뒤 _build_physics() 전에 part1_[학번].devsim을 만들고 파일당 소자 하나만 포함한다. 재실행에 config나 학생 코드는 필요 없어야 한다.
- Part 1 보고서 절은 Part-1-(a) 빠진 물리와 필요성·구현·검증, Part-1-(b) 시도→지표→판단의 탐색·최종 구조 그림·8항목 표, Part-1-(c) 단일 변수 변화에 따른 지표 설명이다. Checker OK 화면도 보고서에 넣는다.
- PDF의 전체 Project 제출 마감은 2026-10-07 23:59 LearnUs이며 전체 보고서는 약 12쪽이다. 전체 제출은 Part 1과 Part 2 파일 모두를 요구하지만 이번 분석·향후 순서 제안은 Part 1에 한정한다. 조교 재실행과 허용 오차 밖으로 다른 보고 수치는 인정되지 않으며 타당한 과정에는 부분 점수가 있다.

## Assumptions

- Part 1의 공통 좌표·명명·저장·채점 규칙도 범위에 포함하고 Part 2 capacitor 구현은 범위 밖으로 둔다.
- 코드에 대한 사실은 실제 소스, 과제 요구사항은 PDF와 배포 checker를 근거로 판단한다. AGENTS의 이전 요약도 PDF로 재확인한다.
- 설계 변수의 영향과 탐색 순서는 분석에 따른 제안이며 spec 달성이나 특정 최종 설계를 보장하지 않는다.
- 기존 simulation 결과는 평가 조건·모델·온도가 일치하는지 확인되기 전까지 Part 1 합격 근거로 쓰지 않는다.
- PDF 독서용 임시 이미지·도구는 scratch로만 사용하고 프로젝트 의존성을 추가하지 않는다.
- VS=0, 기본 VB=0으로 기존 코드와 평가 조건을 구성하고 body-effect 항목에서만 VB=-0.5 V로 바꾼다. 모든 구조·도핑·gate 재료는 고정한다.
- Vth는 목표 전류를 실제로 bracket하는 데이터에서 추출하고 coarse 0.1 V sweep만으로 판단하지 않는다. SS의 구현안은 로그 전류 구간 두 끝점의 VG 차이를 2 decade로 나눈 평균이다. PDF에는 평균의 세부 weighting·interpolation·조교 허용 오차가 없어 이후 구현에서 정의·근거를 기록하고 조교 조건과 대조해야 한다.
- Gate work-function 기준 전위·온도 의존 식·계수·body tap과 접점 처리 등 조교 physics의 세부 구현은 배포되어 있지 않다. PDF와 구조 checker만으로 그 구현을 역추측하지 않으며 현재 수치를 합격이라고 주장하지 않는다.

## Plan

- [x] M1 — 과제 PDF의 전체 relevant 페이지와 Part 1·공통 규칙을 읽어 목표·표·제출 조건을 추출한다.
- [x] M2 — config·mesh/doping·physics·bias/sweep·checker를 대조하여 구현 격차와 미확인 사항을 정리한다.
- [x] M3 — 실행 순서·완료 기준을 정리하고 원문과 수치·단위·제출 규약을 재검토한다. 문서 상태·기존 파일·로그 보존 검증 후 분석 완료 기록을 남긴다.

### 향후 구현·설계 순서 제안 — 이번 요청에서 실행하지 않음

| 순서 | 해야 할 일 | 완료 기준·검증 |
|---|---|---|
| 1 | 요구사항·단위·8항목 측정 정의를 고정하고 기존 baseline 설정/코드/결과를 보존한다. | 표와 변수 범위·전류 폭 환산·기본 bias가 명시되고 기존 결과를 덮어쓰지 않는 작업 경로를 정한다. |
| 2 | 제출용 구조를 먼저 준비한다. gate 재료 선택과 gate_metal 라벨, 올바른 접점·계면·NetDoping, physics 이전 저장 경로를 추가한다. PDF의 표면 p+ body tap과 현재 하부 ohmic 접점 차이도 조사해 처리한다. | 새 프로세스에서 저장 파일을 로드해 구조 checker 통과, 단일 device·이름·재료·치수·도핑·physics/bias/result 배제 여부를 별도 확인한다. Checker 통과만으로 tap/physics/spec 충족을 단정하지 않는다. |
| 3 | Gate work function을 전위 기준과 일관되게 반영하고 고온 carrier/SRH 모델의 온도 의존성을 보완한다. 추가 모델은 필요한 근거부터 결정한다. | 재료 변경에 따른 Vth 이동의 방향·크기, 300/398 K에서 물성값·평형 농도·접합 누설의 일관성을 독립 근거와 비교한다. 이동도·수치 상수를 임의 조정하거나 설치된 helper 자체를 patch하지 않는다. |
| 4 | 8항목 measurement·판정을 구현한다. body bias, low/high VD, 398 K 조건을 재현하고 Vth/SS를 충분한 전압 해상도로 추출한다. | 최소 300 K의 (VD=0.05, VB=0), (VD=2, VB=0), (VD=0.05, VB=-0.5) Id–Vg와 398 K off-point를 확보한다. VG=VD=2의 Ion, Eox, DIBL 환산을 확인한다. 목표 전류 미도달·SS 구간 부족·비유한 값·solver 실패는 명시적 실패로 처리한다. 추출기는 독립 기대 곡선·단위·실패 사례로 검증한다. |
| 5 | 검증된 모델과 추출기로 초기 소자의 8항목 baseline 표를 만든다. | 하나의 구조에 대해 모든 조건과 수치·PASS/FAIL·근거 파일을 함께 기록한다. 기존 CSV나 checker OK만을 합격 근거로 쓰지 않는다. |
| 6 | 변수를 하나씩 바꾸어 영향과 병목을 파악하고, 이후 조합을 조정해 모든 spec을 동시에 만족시킨다. | Gate 재료/NA/tox로 Vth·누설·body effect·SS, Lg/xj/채널 도핑으로 DIBL, tox/Lg/ND/S-D 길이로 Ion을 함께 살핀다. 각 시도마다 전체 설정·8지표·실패·선택 이유를 기록한다. 표의 일반 설계 힌트는 시작점이며 최종 값은 실행 결과로 결정한다. |
| 7 | 최종 후보를 모든 조건에서 다시 측정하고 numerical 안정성과 여유를 확인한다. | 도핑 profile을 고정한 mesh 검증, 전압 간격 검증, 작은 전류의 재현성·전류 보존을 확인한다. 기존 mesh-doping 결합을 먼저 해소한다. 4 nm에서 Eox=5 MV/cm로 경계값인 점과 다른 항목의 여유도 검토한다. |
| 8 | 최종 part1_[학번].devsim을 재생성하고 저장 파일에서 구조와 결과를 재현한다. | 새 프로세스에서 checker OK, 모든 device/모델·정확한 파일명·범위 확인, 저장 구조에 검증된 로컬 physics를 다시 붙여 8항목 재평가. TA physics/허용 오차와의 차이는 별도로 남긴다. 학번은 실제 사용자 정보를 사용한다. |
| 9 | Part-1-(a)/(b)/(c) 보고서와 증거를 정리한다. | 물리 검증, 실패 포함 탐색 과정, 단일 변수 실험, 최종 단면·8항목 표·정확한 조건/단위·checker OK 캡처·한계를 포함한다. 과정을 탐색 시작 때부터 축적한다. |

## Validation

- PDF 텍스트를 추출하고 해당 페이지를 render해 표의 값·단위·행 대응과 그림 규약을 직접 확인한다.
- 실제 함수와 조건을 검색·읽기 전용으로 대조한다. 실행하지 않은 spec을 PASS로 표시하지 않는다.
- Part 1의 모든 spec·설계 범위·제출 규칙에 분석의 대응 항목이 있는지 확인한다.
- 기존 tracked 파일과 AGENTS의 SHA-256, Git 변경 범위, PLAN의 8개 section·checklist, 로그의 필수 항목·KST 시간순서·이전 byte prefix 보존을 검증한다.
- 분석 요청이므로 TCAD·GUI·CLI·checker를 실행하여 결과물을 만들거나 코드를 수정하지 않는다.

## Progress / Discoveries

- 기존 workflow·로그와 project1의 config·simulator·workflows·checker를 확인했다. gate 재료·구조-only 저장·spec evaluator의 누락을 재확인했다.
- scratch의 PDF 라이브러리 디렉터리는 sandbox에서 하위 파일 접근이 거부되어 namespace import만 되고 reader가 동작하지 않았다. 기존 reader의 제한된 접근으로 PDF 독서를 진행하며 프로젝트 환경은 수정하지 않는다.
- 기존 reader를 허용된 읽기 경로로 실행해 57쪽 PDF를 추출했다. PDF 실제 페이지 41/42(영문)와 50/51(국문)의 Part 1, 45~48 및 54~57의 공통 규칙을 대조했다. 표·그림·checker 예시는 render 이미지로 확인했다. PDF 내부의 슬라이드 번호와 실제 파일 페이지가 다르므로 근거는 실제 페이지 번호를 쓴다.
- 8개 spec은 하나의 구조·도핑·gate 재료에 적용한다. gate work function 선택은 표의 재료 이름으로 저장하고, 조교가 별도 physics를 붙여 재실행한다. 단순 YAML 조정만으로 제출 준비가 완료되지 않는다.
- 설치된 helper의 CreateOxideContact는 Potential − gate_bias 식만 사용하고 일함수 항이 없다. SetSiliconParameters는 T/kT/V_t를 갱신하지만 n_i/n1/p1은 상수다. 물리 누락과 measurement API 누락을 구분해 먼저 검증해야 한다.
- PDF의 body 접점 그림은 표면 p+ tap 위에 있으나 현재는 bulk 아랫면의 이상적 ohmic 접점이다. Checker는 tap이나 body의 표면 위치를 강제하지 않으므로 통과만으로 이 가정의 타당성을 확정할 수 없다. 별도 Schottky solver가 과제의 명시적 필수사항이라고 단정하지 않는다.
- Mesh 상수 DX_CHANNEL/DY_JUNCTION이 도핑 erfc 감쇠 길이에도 사용된다. 최종 mesh 검증은 물리 도핑을 고정한 채 수행해야 한다.
- 현재 Id–Vg 기본 간격은 0.1 V이며 workflow에는 body bias 인자가 없다. Vth/SS 구간의 세밀한 추출과 body 조건 재현은 별도 measurement 작업이다. Gate 재료 표 11개와 8개 spec, 설계 범위를 영문/국문 원문 및 checker와 대조했다.
- 제안 순서는 제출 구조 준비→physics 검증→measurement 검증→baseline→단일 변수/조합 탐색→최종 재현성→저장 파일 재검증→보고서다. 보고서의 과정 증거는 baseline과 탐색부터 함께 남긴다. 향후 구현 승인은 이번 분석 완료와 별개다.
- 분석 validation에서 8개 spec·9개 향후 단계·필수 PLAN section·Git whitespace·변경 범위를 확인했다. Tracked 파일 66개와 AGENTS의 SHA-256은 그대로이며 이전 로그 byte가 보존되었다. 시각 검토를 마친 임시 PNG 57개는 확인한 scratch 경로에서 제거했다.

## Final Review

| 검토 항목 | 결과 |
|---|---|
| 최초 요구사항 | PDF의 Part 1·관련 배경·공통 규칙과 현재 코드를 읽고 해야 할 일을 의존관계에 따라 9단계로 정리했다. 분석만 완료했다. |
| 원문 정확성 | 실제 41/42·50/51쪽의 영문/국문 spec·설계 범위·gate 표와 45~48·54~57쪽의 제출 규칙을 대조하고 핵심 표·그림·예시를 시각적으로 확인했다. |
| 중요한 격차 | Gate 재료·일함수, 고온 n_i/n1/p1, 구조-only 저장, spec 추출·body 조건, mesh-doping 결합과 body tap/ohmic 가정의 차이를 식별했다. |
| 실행한 validation | PDF 추출·render 확인, 함수와 helper·checker 읽기 대조, 8개 spec·9단계·PLAN 8개 section·UTF-8·diff·Git whitespace·해시·append 보존·상태 일치 검증을 완료했다. |
| 미실행 검증 | TCAD·GUI·CLI·구조 checker 및 parameter 탐색은 분석 범위이므로 실행하지 않았다. 실제 spec 충족 여부는 미판정이다. |
| 변경 범위 | PLAN 갱신과 PROGRESS_LOG append만 수행했다. Tracked 66개 파일과 AGENTS는 동일하며 code/config/PDF/HW1/기존 결과·환경을 수정하지 않았다. |
| 남은 불확실성 | 조교 physics의 상세 식·계수·추출 알고리즘·허용 오차, 실제 학번, body tap 처리의 상세 조건은 확인 필요다. 특정 설계의 합격이나 필수 추가 모델 전체를 추측하지 않는다. |
| 다음 상태 | 현재 분석 요청은 완료했다. 향후 구현 요청이 오면 이 순서를 현재 목표에 맞게 PLAN에 갱신하고 logging을 이어간다. |
