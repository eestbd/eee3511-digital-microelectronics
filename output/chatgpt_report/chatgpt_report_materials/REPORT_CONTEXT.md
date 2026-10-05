# Project 1 보고서 작성용 컨텍스트

기준일: 2026-10-05, Asia/Seoul(KST). 학번: **2022142233**.

이 문서는 현재 코드, 과제 PDF, 공식 Q&A, 실제 입력·CSV·JSON·진행 기록을 대조한 보고서 작성 자료다. 경로는 모두 repository root `C:/Users/super/DEVSIM_PROJECT` 기준이다. GPT에 이 문서와 과제 PDF를 전달하면 본문을 작성할 수 있고, 원시 자료 묶음을 첨부하면 그래프를 실제 데이터로 작성할 수 있다.

**현재 결론:** Part 1 최종 소자는 공식 모델에서 8/8 PASS, Part 2 새 추천 소자는 필수 소자 조건의 로컬 검증 PASS다. 최종 통합 보고서와 두 실제 checker OK 화면은 미완료다. 조교 전체 evaluator의 재실행 결과는 **확인 불가**이며 채점 통과를 보장하지 않는다.

## 1. 목표와 과제 요구사항

### 프로젝트 목적

HW1의 Python/DEVSIM MOSFET 시뮬레이터를 확장해, 서로 충돌하는 전기적 성능과 설계 범위의 균형을 찾는다. Part 1은 8개 spec을 동시에 만족하는 nMOS, Part 2는 빠른 READ와 긴 retention을 함께 만족하는 pass transistor + storage capacitor다. 두 Part는 독립 소자 최적화이며 물리·코드는 재사용하되 parameter가 같을 필요는 없다.

주요 근거는 `project1/Project1_Assignment_0927.pdf`와 `project1/OFFICIAL_QA.md`다. 실제 PDF 순서 50~51 쪽은 Part 1, 52~54 쪽은 Part 2/명명, 55~57 쪽은 저장/자가검사/제출이다. 슬라이드의 장 번호 3~6 은 별도 Part 3~6 과제를 뜻하지 않는다.

### Part 1 전기적 기준과 최종 공식 결과

VDD=2 V. 별도 지정이 없으면 T=300 K, VS=VB=0 V 다. 모든 항목을 **동일 구조·도핑·gate 재료**로 평가한다. 전류는 폭 1 µm 당이다.

| 항목 | 측정 조건/정의 | 과제 기준 | 최종 fine 값 | 판정 |
|---|---|---|---:|---|
| Vth | VD=0.05 V, ID=1e−7 A/µm 의 VG | 0.40~0.50 V | 0.484848 V | PASS |
| Ion | VG=VD=2 V, 300 K | ≥450 µA/µm | 516.138 µA/µm | PASS |
| Ioff | VG=0, VD=2 V, 300 K | ≤1 pA/µm | 0.0126374 pA/µm | PASS |
| SS | VD=0.05 V, ID=1e−10~1e−8 구간 평균 | ≤75 mV/dec | 66.2219 mV/dec | PASS |
| 고온 Ioff | VG=0, VD=2 V, 398 K | ≤100 pA/µm | 10.3755 pA/µm | PASS |
| DIBL | [Vth(VD0.05)−Vth(VD2)]/1.95 V | ≤30 mV/V | 13.0424 mV/V | PASS |
| Body effect | VD=0.05 V, Vth(VB=−0.5)−Vth(VB=0) | ≤0.08 V | 0.0266225 V | PASS |
| Eox | 2 V/tox, cm 단위 환산 | ≤5 MV/cm | 4.21053 MV/cm | PASS |

Part 1 허용 범위: Lg≥0.3 µm, gate SiO2 tox≥4 nm, xj=0.02~0.25 µm, tSi=0.3~2 µm, source/drain 각각0.2~1 µm, NA=1e14~1e17, ND=1e18~1e21 cm⁻³. Gate 재료는 PDF/checker 의 이름·일함수 표를 따른다.

### Part 2 동작·구조 기준

| 항목 | 과제 조건 |
|---|---|
| 공통 | VDD2 V, T398 K(125°C), VB−0.5 V |
| 고정 치수 | **Lg0.3 µm, 폭 W0.1 µm — 모든 Part 2 실험에서 유지** |
| READ | BL 초기1 V, WL2.5 V, CBL100 fF, dt10 ps, 0.5 ns 판정 |
| 저장 상태 | Data0 초기 Vcell0 V, Data1 초기 Vcell2 V; 쓰기 simulation 없음 |
| READ 기준 | 두 상태 모두 abs(VBL−1 V)≥60 mV |
| Retention hold | WL0, Data0 BL2 V / Data1 BL0 V |
| Retention 기준 | 열화된 Vcell 에서 BL1 V 로0.5 ns 재 READ; 마진60 mV 미만 최초 시각, 두 상태≥64 ms |
| TR 설계 범위 | Part1 범위 재사용, 단 Lg 고정·SiO2 tox≥5 nm·2.5 V/tox≤5 MV/cm |
| 저장 cap | CSTORE≤20 fF, 전체 plate dQ/dV 를 plate1 V 에서 추출 |
| Cap 치수·전계 | h0.2~1.5 µm, tdiel3~10 nm, 1 V/tdiel≤4 MV/cm |
| Cap 재료 | SiO2κ3.9 / Al2O3κ9 / HfO2κ20 / ZrO2κ35 |

최신 Q&A 는 source contact 바로 위 capacitor 와 bulk-hk 직접 접촉이 없는 배치, 허용 범위의 비균일/비대칭 doping 을 허용한다. 실제 분포는 저장된 `bulk.NetDoping`에 있어야 한다. Background NA 와 별도 고농도 p+ body tap 의 허용은 구별한다.

### 보고서 서식·분량·필수 절

**PDF, 약 12쪽, 양식 자유**다. Q&A에서 조금 초과하는 것은 허용했다. 특정 Word 서식, 글꼴·여백·줄간격, 표지의 쪽수 포함 규칙은 **확인 불가**다. 읽기 쉬운 A4·10~11pt 등은 편집 권장값이지 과제 의무가 아니다.

| 필수 절 이름 | 넣어야 할 내용 |
|---|---|
| Part-1-(a) | HW1 의 부족한 물리, 필요성, 구현·검증 방법 |
| Part-1-(b) | 초기 설계→spec→재설계의 시도·지표·판단, 최종 소자 그림, 8 항목 표 |
| Part-1-(c) | 한 knob 씩 바꾼 비교와 지표 변화/동작 이유 |
| Part-2-(a) | 1T1C 그림, plate dQ/dV CSTORE 와 추출 조건 |
| Part-2-(b) | Data0/1 ΔVBL(t),0.5 ns 값/60 mV 비교, 설계 슬라이드가 요구하는 **I(t)** |
| Part-2-(c) | 초기 셀→READ/retention 검사→재설계의 시도·지표·판단 |
| Part-2-(d) | 최종 셀 그림, READ 마진·retention 표, 설계 근거 |

두 실제 `.devsim`의 checker **OK 화면을 보고서에 삽입**한다. 제출은 PDF 와 `part1_2022142233.devsim`, `part2_2022142233.devsim`이며 2026-10-07 23:59 KST 까지 LearnUs 에 업로드한다. 업로드 완료는 확인되지 않았다.

## 2. 전체 구현 구조와 주요 파일 역할

```text
repository/
├─ hw1/                         완료된 학습/reference (이번 Project1 작업에서 보존)
│  ├─ step1/                    square-law Python 모델
│  ├─ step2/                    2D DEVSIM MOSFET·I–V/C–V reference
│  ├─ step3/                    Streamlit GUI
│  └─ demo/                     배포된 실행 demo
├─ project1/
│  ├─ mosfet.py / config.yaml   기존 일반 CLI 경로
│  ├─ mosfet_tool/              공용 설정·mesh/doping·physics·측정·cell
│  ├─ part1.py                 동일 저장 소자의8개 spec 측정
│  ├─ part1_experiment.py      제한된 설계 탐색과 실패/출처 보존
│  ├─ validate_part1.py        필수 numerical check·선택 double 진단
│  ├─ part2.py                 READ/64 ms retention 평가
│  ├─ part2_design.py          비균일채널·비대칭ND·body tap
│  ├─ part2_experiment.py      screen/endpoint1/retention1
│  ├─ tests/                  unittest
│  └─ results/                세션별 입력·CSV·JSON·구조·검증·실패
├─ output/pdf/                 기존7쪽 Part1 보고서 초안
├─ AGENTS.md / PLAN.md / PROGRESS_LOG.md
└─ environment.yml             로컬 Conda 환경 정의
```

| 주요 파일 | 역할과 구현 이유 |
|---|---|
| `project1/mosfet_tool/config.py` | Device dataclass/YAML, 읽기 쉬운µm/nm 입력을 보관. 모델·도핑 감쇠 길이·재료를 명시하여 baseline 과 후보 구분 |
| `project1/mosfet_tool/materials.py` | 허용 gate 이름/별칭·일함수 표. 숫자를 재료 이름으로 저장하는 오류 방지 |
| `project1/mosfet_tool/physics.py` | Varshni Eg/ni, 공식 μ(T), gate offset. 모델 식의 중복·온도 불일치를 피함 |
| `project1/mosfet_tool/simulator.py` | MosfetSimulator: mesh/erfc doping/physics/bias ramp/전류·전하/sweep/build·reload. 구조와 물리를 분리하여 제출 재실행 가능 |
| `project1/mosfet_tool/workflows.py` | run_idvg/run_idvd/run_cv/save_csv. CLI 와 소비자가 같은 준비 순서·단위·열 이름 사용 |
| `project1/mosfet.py` | idvg/idvd/cv 일반 CLI. 이것만 실행해서8 개 spec 완료라고 판단하지 않음 |
| `project1/mosfet_tool/metrics.py` | log-current crossing/SS·8 개 spec 판정. 외삽·clamp 없이 PASS/FAIL/ERROR 구분 |
| `project1/part1.py` | 구조를 한번 저장하고 bias/T case 마다 reload, CSV·metrics·source hash 저장. 모든 spec 이 같은 소자인지 보장 |
| `project1/validate_part1.py` | 20/10 mV 비교, 전류 보존, raw 재추출, fresh live/reload. grading_condition_checks_pass 와 double diagnostic 분리 |
| `project1/part1_experiment.py` | 허용 설계 knob·단일 변수·횟수/시간/중복/timeout 검사, 새 폴더에 원 입력·실패 보존 |
| `project1/mosfet_tool/cell.py` | Capacitor/CellSimulator, plate dQ/dV, signed READ, adaptive retention. 기존 transistor physics 를 재사용 |
| `project1/part2.py` | 두 상태 READ10/5 ps·64 ms retention, checkpoint·fresh checker·metrics. 중단/부분 계산을 전체 PASS 로 숨기지 않음 |
| `project1/part2_design.py` | ChannelDoping/BodyTap/ProfileCellSimulator. 실제 공간 분포를 NetDoping 에 기록하여 조교가 그대로 읽도록 함 |
| `project1/part2_experiment.py` | 초기 READ/누설 screen, Data1 endpoint/retention 비교. 비용 큰 전체 검증을 후보 선택 후 수행 |
| `project1/check_structure_file.py` | region/contact/material/naming·구조-only 규약 검사. **전기적 spec checker 는 아님** |
| `project1/part1_baseline.yaml` | 원래 Part1 baseline. 최종 후보 config 와 혼동하지 않음 |
| `project1/part2_initial.yaml` | TaN 초기 셀 |
| `project1/part2_final.yaml` | 첫 합격 #11 입력 (역사적 final) |
| `project1/part2_robust.yaml` | **현재 추천 #19 입력** |
| `project1/tests/test_part1.py` | 독립 추출 기대값·잘못된 입력·공식 physics·flat-band·source snapshot·저장/reload |
| `project1/tests/test_part1_experiment.py` | 탐색 예산·물리/측정 보호·timeout/실패 보존 |
| `project1/tests/test_part2.py` | 폭/부호/시간/전하, reverse/body current, degraded READ failure, native cap/reload |
| `project1/tests/test_part2_design.py` | 도핑 영역/경계·비대칭 농도 범위·tap 검증 |

`results/retention_estimate_20261005_111911/measure.py`의 continuation 은64 ms 이후 실제 누설/재 READ 를 이어간다. 후속 robust run 의 `launch.py`, `verify_candidate.py`, `audit.py`, `summarize.py`, `package_result.py`는 해당 세션용 실행·독립 감사·export 스크립트이며 새 물리 모델이나 외부 agent framework 가 아니다.

Project1 의 구현 구조는 Python 모듈+CLI+YAML+CSV/JSON 다. Streamlit GUI 는 HW1 reference 이며 새 Project1 GUI 를 만들었다는 근거는 없다. 별도 source build 단계는 없다.

## 3. 핵심 물리·알고리즘과 선택 이유

### 3.1 HW1 재사용과 실제 물리 보완

HW1 의 DEVSIM 경로에는 이미 Poisson, 전자/정공 drift-diffusion 과 DEVSIM helper 의 **SRH**가 있었다. Project1 에서 이 모델을 처음 발명/추가한 것이 아니다. 부족한 gate 재료 반영·고온 ni/SRH 정합성·공식 온도 의존 mobility 를 보완했다.

최종 공식 모델은 다음과 같다 (`physics.py`; model id `qa_varshni_midgap_mobility_v1`).

```text
Eg(T) = 1.17 − 4.73e−4 T²/(T+636) [eV]
ni(300) = 1e10 [cm⁻³]
ni(T) = ni(300) (T/300)^(3/2)
        × exp[Eg(300)/(2k_eV·300) − Eg(T)/(2k_eV·T)]
k_eV = 1.3806503e−23 / 1.6e−19 [eV/K]  (코드 상수)
n1 = p1 = ni(T)
USRH = (np−ni²)/[τp(n+n1)+τn(p+p1)]
μn(T) = 400 (T/300)^(-2.4)
μp(T) = 200 (T/300)^(-2.2) [cm²/(V·s)]
Φms′ = Φm − [4.05+Eg(T)/2]
Potential_gate = VG − Φms′
```

398 K 에서 Eg1.097539 eV, ni4.757304e12 cm⁻³, μn202.969896/μp107.387566 cm²/(V·s). W gate 의Φm4.60 eV. Gate body Fermi offset 을 중복 가산하지 않는다. 초기 모델의 χ+Vt ln(Nc/ni) 기준과 상수400/200 이동도는 **공식 Q&A 이전** 기록이며 최종 식과 구분한다.

온도 변화가 고온 누설과 gate 조건에 함께 영향을 주므로 ni 를 equilibrium/contact/수송/SRH 에 일관되게 적용했다. 공식 식에 없는 velocity saturation·doping-dependent mobility·Fermi–Dirac·bandgap narrowing·tunneling/gate leakage 를 추가하지 않았다. Boltzmann/완전 이온화·기존 수명·ideal ohmic 가정은 남아 있다.

### 3.2 Mesh·도핑·저장

내부 길이는 cm (`UM=1e−4`, `NM=1e−7`)다. Surface y=0, bulk y>0, oxide y<0이며 source는 왼쪽, drain은 오른쪽, gate는 planar 배치다. Default mesh 기준은 channel x25 nm, oxide y2.5 nm, junction y10 nm, bulk y50 nm이며 경계선 추가 후 DEVSIM mesh가 생성된다. 완전한 mesh 수렴 검증을 수행했다거나 모든 실제 간격이 이 값이라는 뜻은 아니다.

S/D 는 x/y 방향 erfc product×0.25 로 donor plateau 와 부드러운 접합을 만든다. `NetDoping=SourceDoping+DrainDoping−NA`이며 profile/tap 사용 시 공간 억셉터와 tap 을 추가 차감한다. 감쇠 길이 x12.5/y5 nm 를 명시해 mesh 와 물리 도핑 길이의 혼동을 피한다. Mesh 변경을 순수한 수치 변경으로 단정하지 않는다.

Build 순서는 `clear→mesh→doping→.devsim 저장→physics`다. 저장 내용은 mesh·region/contact/interface·material·NetDoping이며, physics·bias·해 결과는 제외한다. Fresh reload는 단일 device와 physics 부재를 검사하고 gate 재료를 실제 파일에서 읽는다. DEVSIM은 프로세스 전체 상태를 공유하므로 새 build는 이전 device/mesh를 삭제한다. 독립 replay는 새 프로세스에서 수행한다.

### 3.3 Part1 측정

한 구조를 저장한 뒤 VD0.05/2 V, VB0/−0.5 V, T300/398 K를 바꾸어 평가한다. Vth는 target current의 **유일한 양의 상승 crossing을 log10(ID)에서 보간**한다. SS는 `[VG(1e−8)−VG(1e−10)]/2`를 mV/dec로 환산한다. Ion/Ioff는 VG2/0 V의 실제 sample이며 외삽·전류 clamp를 쓰지 않는다. 측정 불가인 ERROR와 측정 가능하지만 spec 미달인 FAIL을 구분한다.

Bias ramp0.1 V로 DC 상태를 이동한다. 이는 측정 sweep0.02/0.01 V와 다른 개념이다. 수렴 메시지만 보지 않고 source/drain/body 전류의 합과 raw 결과를 확인한다. Eox는 과제 정의의 VDD/tox이며 국소 최대 전계가 아니다.

### 3.4 Capacitor 와 CSTORE

Source contact 위에 `metal_storage` pillar와 좌우 `hk_l/hk_r` ZrO2 slab을 배치했다. Storage 접점은 source 전위, plate 접점은1 V다. Source 전체 contact 위 배치는 Q&A에서 허용됐으며 실제로 접하지 않는 bulk-hk interface를 임의로 만들지 않았다.

전체 plate charge의 중앙차분 `C=[Q(1+δV)−Q(1−δV)]/(2δV)`를 사용한다. δV10/5 mV를 비교하고 2D charge(per-cm)에 폭(cm)을 적용한다. 전류의 A/µm 폭 변환과 구분한다. 양 slab의 기하 추정 `2κ ε0 h W/tdiel`은 교차 확인용이며 측정값을 대체하지 않는다.

### 3.5 READ 와 retention

과제가 허용한 **DC→단자 전류→ΔQ=IΔt→외부 capacitor 전압 갱신**의 Python 시간 루프다. Native transient PDE를 새로 구현한 것으로 쓰지 않는다.

```text
Is_A = Is_A_per_um × 0.1; Id_A = Id_A_per_um × 0.1
Vcell_next = Vcell − Is_A·dt/CSTORE
VBL_next = VBL − Id_A·dt/CBL
Qbody += Ib_A·dt
잔차 = CSTORE·Vcell + CBL·VBL − Qinitial − Qbody
```

Signed terminal current를 사용하여 Data0/1의 전하 이동 방향을 보존하고 body 전하도 검증한다. 전류를 abs로 바꾸어 전압을 갱신하거나 비정상 전압을 clamp하여 숨기지 않는다. 공식 READ는10 ps/50 steps/0.5 ns이며,5 ps는 민감도 검사다.

Retention은 WL0·worst-case BL에서 signed source current로 Vcell을 적분한다. `dt=min(8 ms,남은시간,ΔVmax·CSTORE/abs(Is_A))`이며 ΔVmax는 기본3/미세1.5 mV다. 실제 열화 전압에서 BL1 V로 재READ하여60 mV와 비교하고 실패 구간을 재적분·bisection으로 좁힌다. Null READ margin은 그 step에서 재READ하지 않았다는 뜻이다. Checkpoint 사이 단일 crossing을 가정하며 연속 시간의 모든 지점을 검증한 것은 아니다.

### 3.6 비균일/비대칭 doping 와 bottom tap

`ProfileCellSimulator`는 gate 왼쪽/오른쪽 x구간의 NA와 S/D별 ND를 분리한다. 설계명은 ‘채널 도핑’이지만 코드에서는 해당 x구간의 bulk 깊이에도 적용된다. Background는 gate 밖에서 유지한다. p+ tap은 실리콘 하단0.05 µm의 추가 acceptor이며 source 옆 표면 tap이 아니다. 저장된 실제 NetDoping을 위치별 기대값과 대조하여 미인식 LDD/Halo 모델에 의존하지 않게 했다.

## 4. Project1 에서 추가·수정한 범위

아래는 HW1 reference와 현재 코드·로그를 비교하여 확인한 **프로젝트 수행 중 변경**이다. 사용자가 모든 줄을 직접 타이핑했는지, starter의 개인별 작성 기여율은 **확인 불가**다. 보고서에서는 ‘프로젝트에서 구현·확장했다’고 기술하고 DEVSIM/HW1 재사용을 명시한다.

- 구조만 포함하는 export/reload, gate_metal/material table, gate offset, 온도 모델/μ(T)/SRH 매개변수 정합성.
- 동일 소자의 8항목 측정·추출, 실패 구분, fine/coarse·전류·정밀도·reload 검증과 unittest.
- 제한된 Part1 탐색 runner, 출처 hash, 입력·오류·timeout 보존.
- 1T1C mesh/접점, plate C 추출, signed READ/adaptive retention과 checkpoint.
- 비균일 채널·비대칭 ND·bottom p+ tap을 NetDoping에 반영하는 Part2 설계 경로.
- 선택 소자의 64 ms 이후 실제 누설 적분·재READ·failure bracket, 후속 여유 개선 실험·raw audit.
- AGENTS/PLAN/PROGRESS_LOG, 공식 Q&A·결과 요약, Git 제외 정리·UTF-8 복구. 연구 보고서 본문에서는 운영 세부를 간략히 처리한다.
- Project1의 불필요한 HW1 복사 예제·launcher·옛 출력 17개 정리. HW1 원본, 일반 Id–Vg/Id–Vd/C–V의 기존 API·열 이름과 legacy 동작을 보존했다.

## 5. 설계 이력과 ‘왜’에 해당하는 판단

### 5.1 Part1: baseline→10 회→공식 재검증

초기 소자는 Lg1.0 µm/tox10 nm/NA1e16/gateW, xj0.1/tSi0.5/S,D각0.5 µm/ND1e19였다. Q&A 전 baseline은6/8 PASS(Vth0.550307 V/Ion142.052640 µA/µm FAIL). 공식 모델 재측정도 같은 구조에서6/8 PASS(Vth0.551164 V/Ion141.892671)였다. 이 baseline은 임의 최적값을 넣은 것이 아니라 기존 설정의 실제 측정이었다.

총10회는 단일 변수4→조합4→주변2의 순서다. 처음 시간 예산30분은 사용자가 해제하고10회 횟수 제한을 유지했다. 다음 표는 **Q&A 전 모델의 역사적 결과**이며 최종 제출값은1절의 공식 fine 표다.

| 회차 | 설계(gate/tox/Lg/NA 중 변경) | Vth(V) | Ion(µA/µm) | Ioff398(pA/µm) | PASS |
|---|---|---:|---:|---:|---|
| 1 | Lg0.5 | 0.486906 | 333.485 | 482.344 | 5/8 |
| 2 | tox5 | 0.477942 | 292.908 | 40.117 | 7/8 |
| 3 | NA3e15 | 0.469888 | 156.775 | 225.832 | 6/8 |
| 4 | TaN | 0.399957 | 171.100 | 225.858 | 5/8 |
| 5 | Lg0.5/tox5/W | 0.432120 | 641.838 | 397.194 | 7/8 |
| 6 | Lg0.5/tox5/TiN | 0.482026 | 604.311 | 169.236 | 7/8 |
| 7 | Lg0.6/tox4.5/TiN | 0.490584 | 538.507 | 53.693 | 8/8 |
| 8 | Lg0.6/tox4.5/W/NA2e16 | 0.479354 | 544.826 | 21.547 | 8/8 |
| 9 | Lg0.55/tox4.5/TiN | 0.484180 | 595.166 | 78.455 | 8/8 |
| 10 | Lg0.6/tox4.75/W/NA2e16 | 0.484072 | 516.697 | 20.859 | 8/8 |

짧은 Lg는 Ion을 높이지만 DIBL·고온 누설과 충돌했다. 얇은 oxide는 gate control·Ion에 유리하지만 Eox를 높인다. Gate·NA는 Vth·Ion·누설을 함께 바꾼다. #8의 Ion이 더 크지만 #10은 전계와 최악 정규화 여유를 고려해 선택했다. 공식 재측정에서도 #10/#8 모두 PASS였고, 최악 정규화 여유 #10≈0.11704/#8≈0.11111로 #10을 유지했다. 이것이 공정 변동 robustness의 증명은 아니다.

**최종 Part1 #10:** gateW/Lg0.6 µm/tox4.75 nm/xj0.1/tSi0.5/S,D각0.5 µm/NA2e16/ND1e19, erfc 감쇠12.5/5 nm다. 별도 p+ tap은 없고 하단 ideal ohmic body다. 공식 fine0.01 V/201점으로1절의8 PASS를 확인했다. 구조를 갈아엎지 않고 기존 winner를 재사용했다.

### 5.2 Part1 one-knob ablation (공식 모델)

0.02 V의 공통 control로 한 변수씩 비교했다. Tox 비교에는 다른 설정이 같은 공식 #8 primary를 재사용했다. 최종 fine와 coarse ablation을 같은 간격의 결과처럼 섞지 않는다.

| 경우 | 변경 | Vth(V) | Ion(µA/µm) | Ioff398(pA/µm) | DIBL(mV/V) | Body(V) | Eox(MV/cm) |
|---|---|---:|---:|---:|---:|---:|---:|
| #10 control | 없음 | 0.484952 | 516.138 | 10.3755 | 13.0928 | 0.0266803 | 4.21053 |
| tox only | 4.75→4.5 nm | 0.480203 | 544.237 | 10.7140 | 12.6401 | 0.0256577 | 4.44444 |
| Lg only | 0.60→0.65 µm | 0.490253 | 470.975 | 8.58376 | 11.5361 | 0.0273168 | 4.21053 |
| NA only | 2e16→2.5e16 | 0.500344 | 504.666 | 6.30789 | 11.6853 | 0.0297400 | 4.21053 |

얇은 oxide는 Ion↑/Eox↑, 긴 Lg는 Ion↓/leakage↓/DIBL↓, 높은 NA는 Vth↑/Ion↓/leakage↓/body effect↑라는 실측 tradeoff를 보인다. NA ablation의 Vth는 상한을0.344 mV 넘는 coarse 경계 FAIL이며 이 ablation의 fine 검증은 미완료다. 이는 최종 소자의 fine8 PASS를 취소하지 않는다.

### 5.3 Part2 baseline 실패와 첫 탐색

초기 설계는 TaN/tox5/xj0.05/tSi0.3/S,D 각0.2 µm/NA7e16/ND1e19, ZrO2 h0.9 µm/tdiel3 nm이며 tap은 없었다. C18.585 fF, initial READ0/1=128.264/84.102 mV는 모두 PASS였다. Data0≥64 ms였지만 Data1의 failure2.62732~2.64281 ms는 FAIL이었다. 초기 storage 누설2.9877 pA, 열화 Vcell1.604 V에서 재READ59.095 mV가 관측됐다. 미세 간격과 fresh replay에서도 같은 실패를 확인해 소자 성능 부족으로 판단했다.

처음 Part2 계산은 사용자의 ‘Part1까지만’ 지시로 중단하고 checkpoint를 보존했다가 재개했다. 중단 당시 data0 결과와 data1 미완료를 전체 PASS로 쓰지 않았다. 이후 baseline 전체 검증의 수치 PASS와 소자 spec FAIL을 구분했다.

약 1시간의 첫 탐색에서는 **새 물리 후보 11개**를 측정했다. #06은 입력 생성 오류로 native 측정 전에 중단했으므로 별도로 표시한다.

| 첫탐색후보 | 변경 | InitialREAD1(mV) | Data1 판정 |
|---|---|---:|---|
| #01 | W | 67.391 | 40.11~40.51 msFAIL |
| #02 | TiN | 61.373 | 20.71~20.84 msFAIL |
| #03 | NA1e17 | 76.409 | retention 미측정 |
| #04 | xj0.03 | 80.011 | retention 미측정 |
| #05 | W+h0.96 | 67.750 | 64 ms 끝점 FAIL |
| #06 | 잘못생성된 gate 이름 | — | ERROR,물리미측정 |
| #07 | W+NA1e15/7e16 | 77.307 | retention 미측정 |
| #08 | TiN+NA1e15/7e16 | 71.640 | retention 미측정 |
| #09 | W+h0.96+NA5e16/1e17 | 66.169 | 64 ms 끝점 FAIL |
| #10 | W+h0.96+NA3e16/1e17 | 68.917 | 64 ms 끝점 FAIL |
| **#11** | **W+h0.96+bottomtap1e19/0.05 µm** | **67.301** | **양상태≥64 msPASS** |
| #12 | TiN+h0.96+sourceND1e21/drainND1e19 | 67.914 | 64 ms59.145 mVFAIL |

Gate 변경은 누설을 낮추지만 READ 마진도 줄인다. 용량 증가만으로는64 ms를 넘지 못했다. #11 tap을 추가한 실제 저장 누설0.069343 pA는 baseline보다 약43배 작았다. Tap이 없는 W+h0.96에 비해 body 방향 성분0.046614→0.001049 pA, drain 방향0.060072→0.068294 pA로 변했다. 이는 접점 성분의 관측이며 누설의 미시적 메커니즘을 완전히 규명한 것은 아니다.

#11의 64 ms Data1 마진60.417968 mV, C19.824 fF, Eox5 MV/cm는 기준에 대한 여유가 작았다. 2026-10-05 구조를 유지한 추가 측정에서 미세 cell estimate **67.203479 ms**(bracket67.171761~67.235196), 기본67.190534 ms, Data0≥72.597648 ms를 확인했다. 처음의 ≥64 ms 하한과 이후의 한계 추정을 구분한다.

### 5.4 후속 여유 개선과 조기 종료

최대 2시간 예산으로 단일 변수→유망 조합→주변 탐색을 진행했다. 충분히 좋으면 시간을 채우지 말라는 지시를 반영해 **12개의 실제 screen**과 유망 2개의 64 ms endpoint를 비교한 후 후속 #19를 선택했다. 입력 registry의 최대 번호 21을 실제 실험 21회라고 세지 않는다.

| 후속후보 | 변경(#11 기준) | InitialREAD1(mV) | Initialstorage 누설(pA) | 판정 |
|---|---|---:|---:|---|
| #01 | TaN | 84.561 | 2.877892 | READ 이득/높은누설,hold 미측정 |
| #02 | tap0.10 µm | 66.178 | 0.065032 | hold 미측정 |
| #03 | NA1e17 | 58.929 | — | 초기 READ FAIL |
| #04 | xj0.03 | 62.974 | 0.040868 | READ 손실,hold 미측정 |
| #05 | 좌우 NA1e15/7e16 | 76.523 | 0.226621 | READ↑/누설↑,hold 미측정 |
| #06 | tox5.5 | 59.899 | — | 초기 READ FAIL |
| #07 | sourceND1e21 | 73.762 | 0.131049 | READ↑/누설↑,hold 미측정 |
| #10 | 좌우 NA1e15/1e17 | 71.951 | 0.057507 | 64 ms Data1=65.279763 mV,전체 미검증 |
| #16 | sourceND1e21+xj0.03 | 69.086 | 0.060577 | hold 미측정 |
| #17 | source/drainND1e21/1e18 | 51.168 | — | 초기 READ FAIL |
| **#19** | **NA1e15/1e17,ND1e20/1e19,tox5.3,cap1.245/4** | **69.463** | **0.053334** | **전체로컬검증 PASS** |
| #21 | #19 의 lowNA 비율0.5→0.3 | 63.182 | 0.023552 | READ 손실,hold 미측정 |

후속 #10은 READ가 더 좋아도 C19.824/Eox5의 경계에 남는다. #19는 마진·보존·C·전계의 균형으로 골랐다. Source 쪽 low NA/high ND로 READ를 돕고 drain 쪽 high NA로 누설을 억제하려는 설계 의도다. 다변수 조합이므로 각 변수의 독립적인 인과 증명이라고 쓰지 않는다.

초기 희망 목표인 READ75 mV/64 ms 마진64~65 mV/retention96 ms/C≤19 fF는 일부 미달이다. 이 희망값들은 과제 필수 기준60 mV/64 ms/20 fF와 구분한다. #19의 두 상태·기본/미세·연장 보존·구조·raw 검증을 마치고 약 77분에 실험과 수치 검증을 종료했다. 전역 최적해나 극한 탐색 완료를 주장하지 않는다.

## 6. 최종 Part2 소자와 성능

| Parameter | 이전#11 | 현재추천#19 |
|---|---|---|
| Gate/Lg/폭 W | W/0.3 µm/0.1 µm | 동일 |
| tox | 5 nm | **5.3 nm** |
| xj/tSi/S,D 길이 | 0.05/0.3/각0.2 µm | 동일 |
| BackgroundNA | 7e16 cm⁻³ | 동일 |
| Gate 아래좌/우 NA | 7e16/7e16 | **1e15/1e17**,Lg 각절반 |
| Source/drainND | 1e19/1e19 | **1e20/1e19** cm⁻³ |
| Bottomtap | 추가 acceptor1e19,두께0.05 µm | 동일 |
| Cap | ZrO2h0.96 µm/tdiel3 nm | **h1.245 µm/tdiel4 nm** |
| Pillar 폭/clearance | 0.1/0.05 µm | 동일 |

| Metric | 과제기준 | #11 | #19 기본 | #19 미세 retention |
|---|---|---:|---:|---:|
| 초기 READ0(mV) | ≥60@0.5 ns | 127.319535 | 127.806239 | 127.806239 |
| 초기 READ1(mV) | ≥60@0.5 ns | 67.300905 | 69.463266 | 69.463266 |
| 64 msREAD0(mV) | ≥60 | 117.214382 | 112.955710 | 113.056656 |
| 64 msREAD1(mV) | ≥60 | 60.417968 | 63.557209 | 63.559235 |
| Cell/data1retention(ms) | ≥64 | 67.203479(미세) | 95.190207 | **95.198837** |
| Data0retention(ms) | ≥64 | ≥72.597648 | ≥128 | **≥128** |
| CSTORE(fF) | ≤20 | 19.824 | 19.281938 | 19.281938 |
| Gatefield(MV/cm) | ≤5 | 5.000 | 4.716981 | 4.716981 |
| Capfield(MV/cm) | ≤4 | 3.333333 | 2.500 | 2.500 |

표의 READ 는 모두 10 ps, 미세 retention 은 ΔVmax=1.5 mV 다. 별도 5 ps initial READ0/1=127.364070/69.361273 mV 이며 이 값을 10 ps 결과와 혼합하지 않는다.

Data1 미세 실패 구간은94.937594~95.460080 ms, 양끝 마진은60.030102/59.966779 mV다. Midpoint95.198837 ms는 유한 bracket/model 추정으로 정확한 시각이나 통계적 신뢰구간이 아니다. 기본 구간은94.929035~95.451378 ms다. Data0는 미세128 ms에서109.821026 mV로 통과하므로 cell은 Data1이 제한한다. Data0의 정확한 최대 시간은 **확인 불가**다.

Cell estimate는 **41.66% 개선**됐다. 64 ms Data1의60 mV 기준 초과분0.417968→3.559235 mV가 약8.5배이며 마진 전체가8.5배가 아니다. Data0의64 ms 마진은 이전보다 낮지만 충분히 통과한다. S/D·tSi는 허용 최솟값, drain-side NA는 허용 상한이며 모든 parameter가 범위 중앙인 것은 아니다.

실제 plate 전하(폭적용후):

| Vplate(V) | 전체 Qplate(C) |
|---:|---:|
| 0.99 | 1.908911812499996e−14 |
| 1.00 | 1.928193749999996e−14 |
| 1.01 | 1.9474756874999963e−14 |

`[Q(1.01)−Q(0.99)]/0.02=19.2819375 fF`이며 δV5 mV 결과와 일치했다. 최종 저장 NetDoping의 1785개 node와 donor plateau의 source399/drain42 지점을 대조해 PASS를 확인했다.

## 7. 발생한 문제와 해결·남은 한계

| 문제 | 조사/대응 | 최종 해석 |
|---|---|---|
| 초기 Part1 Vth/Ion FAIL | 실제 baseline 측정 후 10회 구조·도핑·gate 탐색 | 최종 공식 8 PASS, baseline FAIL 보존 |
| Double 수렴·전류 보존 FAIL | 독립 프로세스·bias 로그·extended 비교 | 공식 128비트 필수 검증과 구분. 과거 FAIL을 삭제하거나 PASS로 전환하지 않음 |
| 기존 physics와 Q&A 차이 | μ(T)/gate 기준 코드 대조·공식 식 수정·기존 후보 새 run 재측정 | 이전 10회 값과 최종 공식 값 구분 |
| Part2 사용자 중단 | checkpoint/raw/exit 정보를 보존하고 승인 범위에서 재개 | 중단만으로 native 성능 FAIL이나 전체 PASS를 판단하지 않음 |
| 초기 Data1 retention2.64 ms | fine/fresh replay·signed 누설·degraded READ 재현 | 수치 검증은 PASS지만 소자는 FAIL. gate/cap/tap 재설계 |
| 첫 합격 #11의 작은 여유 | 64 ms 이후 실제 적분으로 67.2 ms 확인→후속 탐색 | #19의 95.2 ms·마진·전계 여유 개선 |
| 입력 #06의 잘못된 gate 이름 | native 실행 전 오류 확인·입력 보존·유효 후보 별도 실행 | 물리 실험 수에 포함하지 않음 |
| 경계 도핑 분류·직렬화 | 등록된 소수 경계와 기대값 경계 일치·test·저장 NetDoping 대조 | 재로딩 분포 검증 PASS |
| 계산 도중 source 편집의 출처 문제 | 시작 snapshot 도입, 과거 baseline 출처 보완·raw 재추출 | 과거 실행과 현재 source가 같다고 무조건 주장하지 않음 |
| C–V 최하위 비트 차이 | 원본 source 반복에서도 2 ULP 변동, 초기 strict3 ULP 실패 조사 | 재실행 일치·조사 근거 보존, 수치 허용값 조작으로 숨기지 않음 |
| UTF-16 로그·한글 물음표 손상 | BOM에 맞춘 reader, 확인 가능한 원문 복원, UTF-8 파일 직접 작성 | 수치 판정 불변, 실제 한글·log prefix 검증 |
| bare Part2 build의 profile/tap 미반영 | 최종 저장 구조의 reload 명령 명시 | 아래 재현 주의 필수. 이번 문서 작업에서 core를 재작성하지 않음 |

조교 전체 evaluator·독립 mesh 수렴·실험 소자 정확성·Data0 자체 최대 보존 시간·실제 공정 변동 안전성은 **확인 불가**다. 작은 전류를 수렴 메시지만으로 정확하다고 주장하지 않는다. 기여자의 수작업 여부와 processor 내부 double 실패 메커니즘 전체도 확정되지 않았다.

## 8. 실험·테스트·validation 방법

실행 환경은 루트 `.conda/python.exe`, DEVSIM2.10.0과 Windows DLL 경로다. `environment.yml`은 Python3.11, numpy/pandas, devsim/plotly/streamlit/pyyaml을 정의한다. 실제 측정별 Python/DEVSIM 정보는 metrics에 보존되어 있으며 설정 파일만으로 모든 설치 버전을 단정하지 않는다.

공식 수치 조건은 extended_solver/model/equation=true, ramp0.1 V다. 측정 간격이나 retention step을 줄이는 민감도 검사는 물리 모델·spec threshold 변경과 구분한다.

- **Part1:** exponential 기대값·잘못된 crossing·온도/gate/flat-band·저장/reload unittest, 20/10 mV 곡선과 8개 spec, source/drain/body 합, raw 재추출, critical bias의 fresh live/reload를 검증했다. 최종 검증 당시 21 tests와 legacy3 CLI가 PASS였다.
- **Part2 baseline:** 당시 29 tests, plate δV10/5 mV·기하 추정, READ10/5 ps·signed charge, retention3/1.5 mV, fresh9 cases는 PASS였다. 소자의 Data1 spec FAIL과 구분한다.
- **첫 Part2 선택:** 당시 전체 35 tests PASS와 추가 후 profile7 tests PASS를 확인했다. 두 실행에 중복이 있으므로 ‘42개 서로 다른 tests’로 합산하지 않는다.
- **후속#19:** 4 개 fresh process(verify0/verify1/fine0/fine1)의 정상 완료와 실제 source/구조/config hash, 단자 전류·전하·Euler·step·실패 양끝·관측 단조성·geometry·NetDoping 을 확인했다. READ50/100steps,dt≤8 ms,ΔV≤3/1.5 mV,charge 잔차≤1e−24 C 등 사전 기준을 사용했다.
- #19 기본/미세 64 ms margin 차이 Data0/1=0.100946/0.002026 mV(기준≤2), estimate 차이0.008630 ms/0.009066%(기준≤1%)는 PASS였다. Analytic 상수·반대 부호·zero-current continuation 3건도 검증했다.
- 구조 checker OK·test PASS·수치 안정·전기적 spec PASS·조교 채점은 서로 다른 증거다. CLI exit0이나 measurement_complete만으로 spec PASS를 판정하지 않는다.

이 컨텍스트 작성에서는 새 TCAD/tests를 실행하지 않고 기존 결과·현재 코드·파일 hash를 대조했다. 시뮬레이션이 완료된 문서 작업에 새 실험을 추가하지 않았다.

```powershell
# repository root에서 실행 준비 (이미 있는 환경을 재생성하지 않음)
$repoRoot = (Get-Location).Path
$pythonExe = Join-Path $repoRoot '.conda\python.exe'
$env:PATH = "$repoRoot\.conda\Library\bin;$repoRoot\.conda;$repoRoot\.conda\Scripts;$env:PATH"
$env:PYTHONIOENCODING = 'utf-8'

# tests: 아래는 재현용 명령이며 이번 문서 작업에서 새로 실행한 결과가 아님
& $pythonExe -B -m unittest discover -s .\project1\tests -v

# Part1 최종 입력에는fine0.01 V가 반영되어 있음
& $pythonExe -B .\project1\part1.py --config .\project1\results\official_20261004_155839\part1\selected\config.yaml --output-dir .\project1\tmp\report_replay_part1_new

# Part2의profile/tap은 반드시 저장 구조에서 reload
& $pythonExe -B .\project1\part2.py --config .\project1\part2_robust.yaml --reload-structure .\project1\results\part2_robust_search_20261005_115807\selected\part2_2022142233.devsim --output-dir .\project1\tmp\report_replay_part2_new

& $pythonExe -B .\project1\check_structure_file.py .\project1\part1_2022142233.devsim
& $pythonExe -B .\project1\check_structure_file.py .\project1\results\part2_robust_search_20261005_115807\selected\part2_2022142233.devsim
```

Output 은매번새빈폴더여야한다. Generic `part2.py`의 barebuild 는 body_tap/doping_profile 을생성하지않으므로`--config part2_robust.yaml`만으로최종소자를재현하면안된다. 저장파일을읽는조교경로와구분한다.

## 9. 결과·그래프·이미지 자료 지도

긴 경로를 줄이기 위해 다음 별칭을 사용한다. 모든 실제 경로는 repository root 기준이다. 예를 들어 `OFF/candidate_10/fine/metrics.json`은 `project1/results/official_20261004_155839/part1/candidate_10/fine/metrics.json`이다.

```text
P1OLD = project1/results/part1_search_20261004
OFF   = project1/results/official_20261004_155839/part1
B2    = project1/results/part2_baseline_20261004_175214
S2    = project1/results/part2_optimization_20261004_202430
R11   = project1/results/retention_estimate_20261005_111911
R19   = project1/results/part2_robust_search_20261005_115807
```

| 위치 | 의미와 보고서 활용 |
|---|---|
| `project1/results/part1_baseline/primary/metrics.json` | Q&A 전초기6/8FAIL 상세 |
| `P1OLD/summary.csv`, `final_summary.json` | 당시10 회변경·metric·후보선정/double 진단 |
| `OFF/summary.json` | 공식 baseline/#10/#8/Lg/NAablation,모델정합화후값 |
| `OFF/candidate_10/fine/metrics.json` | **최종 Part1 수치의정본**,실제 fine 간격·조건·hash |
| 같은 fine 폴더 `idvg_low.csv` | VD0.05 의 Vth/SS |
| `idvg_high.csv` | VD2 의 Ion/Ioff/고 VD Vth·DIBL |
| `idvg_body.csv` | VB−0.5 의 bodyeffect |
| `off_398K.csv` | 고온 off 실제한점,곡선으로지어내지않음 |
| `OFF/candidate_10/primary`, `candidate_08/primary`, `ablation_lg/primary`, `ablation_na/primary` | 같은0.02 Vcontrol·one-knob 표/곡선 |
| `OFF/candidate_10/numerical_validation.json` | grading 조건 PASS/선택 double 필드구분 |
| `B2/README.md`, `primary/metrics.json`, `retention_fine/metrics.json` | 초기 Data1FAIL/수치 PASS |
| `B2/curves.html` | **초기 TaN 셀**READ/retention 기본·미세그래프;최종#19 그림이아님 |
| `S2/comparison.csv`, `project1/PART2_OPTIMIZATION_LOG.md` | 첫11 물리후보+입력 ERROR 의원시이력 |
| `S2/experiments/11_W_cap096_bodytap/combined_final/metrics.json`, `combined_fine/metrics.json` | #11 상태별완료결과의종합·출처 |
| `S2/read_retention_comparison.html` | **이전#11**의실제 READ/hold 그래프;현재#19 와혼동금지 |
| `project1/PART2_RETENTION_ESTIMATE.md`, `R11/validation.json` | #11 의67.2 ms 실제측정과검증 |
| `project1/PART2_ROBUST_SEARCH.md`, `R19/result_summary.json` | **현재최종#19**수치/변경/선택이유 |
| `R19/results_matrix.csv` | 후속12 실행과준비만한 not_run 구분 |
| `R19/experiments/19_balanced_ND20/{verify0,verify1,fine0,fine1}/initial_read.csv` | Data0/1 의10 ps VBL/Vcell/signedId/Is/Ib/전하잔차 |
| 같은폴더 `initial_read_5ps.csv` | READ 간격민감도,공식10 ps 대체아님 |
| `retention64.csv`, `continuation.csv` | hold 시간–Vcell/signed 누설/실제 READ checkpoint,64 ms 와이후 |
| `refinement.json`, `degraded_read_*.csv`, `metrics.json` | 실패양끝재 READ 와각 curve 의원래 hold 시각 metadata |
| `R19/validation.json`, `basic64_validation.json`, `fine64_validation.json` | raw 재계산/보존/적분/민감도검증 |
| `R19/selected_geometry/validation.json`, `netdoping.csv` | 실제저장 geometry/공간 NetDoping 그림근거 |
| `R19/selected_checker.json`, `selected_checker.log` | 새학번 Part2 파일의 freshcheckerOK,실제 UI 화면은아님 |
| `project1/results/submission_check_20261004_231707/validation.json` | Part1 및이전 Part2 제출명/해시/checker |
| `output/pdf/part1_report_draft.pdf` | 7 쪽 Part1 초안,학번미확인/Part2 미완료라는과거문구수정필요 |

기존 Part1 그림 PNG는 로컬 `project1/tmp/official_20261004_155839/`의 보고서 렌더 scratch에 있다. 안정된 독립 최종 #19 보고서 PNG/그래프 파일은 **현재 확인되지 않았다**. GPT가 위 CSV로 새 그림을 작성해야 한다. 실제 checker OK 화면 캡처도 **확인 불가/미확보**다. PDF 예시 이미지를 우리 소자의 성공 화면으로 사용하면 안 된다.

CSV 열 해석: Part1은 `Vg_V`, `Id_A_per_um`, `Is_A_per_um`, `Ib_A_per_um`, 전류 잔차를 기록한다. Part2 READ는 `time_s`, `Vcell_V`, `VBL_V`, `Id_A`, `Is_A`, `Ib_A`, `charge_residual_C`다. 이미 physical 폭이 적용된 A 열에 폭을 다시 곱하지 않는다. Retention의 주요 열은 `time_s`, `Vcell_V`, `read_margin_V`, `dt_s`, `Istorage_A`다.

그림을 작성할 때 READ 시간은ns, hold 시간은ms, ΔVBL=(VBL−1)×1000 mV로 표시한다. Data0 ΔVBL은 음수, Data1은 양수이며 마진 표는 절댓값이다. I(t)는 signed Id_A라고 정의하고 t0의 null을 측정0으로 꾸미지 않는다. 0.5 ns/±60 mV, hold64 ms/60 mV 기준선을 표시한다. `degraded_reads` metadata로 실제 hold 시각과 곡선을 연결하며 파일 번호만으로 추측하지 않는다. Continuation 마지막 sample 약97 ms와 refined failure95.2 ms를 혼동하지 않는다.

최종 소자 그림은 not-to-scale/schematic 인지 명시하고 치수·도핑·gate 재료·접점/연결을 표시한다. Part2 는 **source contact 위 cap·bottom p+ tap·좌우 도핑**을 실제대로 그리며 예제의 표면 tap 을 복제하지 않는다.

## 10. 진행 문서에서 활용할 내용

- `PROGRESS_LOG.md`: 2026-10-04 02:02 baseline, 14:20 열 회 탐색, 15:25 Q&A 모델 차이, 16:53 공식 재검증, 17:24 보고서 초안, 19:47 Part2 baseline FAIL, 20:06 추가 Q&A, 첫 탐색 종료, 2026-10-05 11:39 cell67.2 ms, 12:25 새 후보 선택, 13:17 최종95.2 ms, 14:29 제출 준비 확인을 연결할 수 있다. 표제는 기록 시각이며 개별 실험의 정확한 시작 시각과 같다고 가정하지 않는다.
- `PLAN.md`: 현재 작업의 living document로 새 요청마다 바뀐다. 전체 history는 PROGRESS·세션 JSON·각 run의 prior_PLAN으로 확인한다. 과거 계획을 실행 완료의 증거로 쓰지 않는다.
- `PART1_BASELINE.md`: 온도·전위·추출의 초기 설명과 원 baseline의 한계. 처음 모델 식은 과거 것이므로 공식 최종 physics.py와 구분한다.
- `OFF/selected/README.md`, `PART1_REQUIREMENTS_AUDIT.md`: 공식 Part1 선택 이유·8항목 표·ablation·검증. 학번 미확인 등 당시 미완료 항목은 후속 학번 파일 준비로 해결됐다.
- `PART2_OPTIMIZATION_LOG.md`/`PART2_OPTIMIZATION_SUMMARY.md`: 첫 합격까지의 시도→지표→판단, 입력 ERROR·미측정·끝점 FAIL을 보존한다.
- `PART2_RETENTION_ESTIMATE.md`: ≥64 ms 하한을 실제 67.2 ms 추정으로 구체화한 근거.
- `PART2_ROBUST_SEARCH.md`: 새 추천 #19를 선택한 tradeoff·한계·기본/미세 값. 현재 최종 보고서 Part2의 정본이다.
- `PART1_PART2_COMPLETION_AUDIT.md`/`project1/README.md`에는 이전 작성 시점의 Part2 중단·Part1 학번 없음 등이 남아 있다. 현재 완료 상태 판단은 새 결과와 이 문서를 우선한다. 당시 기록을 현재 실행 결과인 것처럼 바꾸지 않는다.

## 11. 보고서에 반드시 언급할 기술 포인트와 제출 상태

1. HW1/DEVSIM physics 재사용과 이번 추가 내용을 구분한다. SRH/drift-diffusion을 처음 만들었다고 쓰지 않는다.
2. 동일 Part1 소자의 8항목, 측정 조건·전류 단위·정전류 log 보간·평균 SS·DIBL·body effect 정의.
3. 공식 μ(T)/Varshni ni/n1,p1/gate 식과 모델 보완 전후 결과를 구분한다.
4. Part1 optimization 이력(b)과 one-knob 원인 비교(c)의 목적·간격을 구분하고 실패도 포함한다.
5. Part1/2는 독립 설계다. Part2 Lg0.3/폭0.1은 고정이며 재료 W와 폭 W는 별개다.
6. 실제 한 device의 1T1C, storage/source·plate1 V 연결, 두 plate 전체 dQ/dV, 2D 폭 변환 한 번.
7. Signed DC-current 시간 적분, body 전하 보존, READ10 ps/0.5 ns/두 상태60 mV.
8. Retention worst-case BL, adaptive dt, 열화 상태의 재 READ 판정. 초기 누설의 상수 외삽·임의 Vcell threshold 금지.
9. #11 이전 합격과 #19 현재 추천을 구분한다. Data1 cell 한계95.2 ms, Data0≥128 ms 하한, 유한 failure bracket의 의미.
10. 용량·전계 여유 개선과 Data0 마진 감소의 tradeoff, 일부 희망 목표 미달, 전역 최적화 미검증.
11. 허용 비균일·비대칭 profile과 bottom tap의 실제 NetDoping 직렬화. Structure checker와 전기적 spec 검증을 구분한다.
12. 구조만 저장하는 export, fresh reload, 128비트/ramp0.1, 기본/미세·current/charge 검증과 조교/mesh 미검증을 구분한다.

**올바른 소자 파일:**

- Part1: `project1/part1_2022142233.devsim`, SHA256=`41c6f8f6ff5782c8ec3ecbc98d39bd264149ec076630f8bad0c9c98d6f06d07c`.
- **현재추천 Part2:** `project1/results/part2_robust_search_20261005_115807/selected/part2_2022142233.devsim`, SHA256=`376b392d2a81e9016f89c811f382a8f2d81e065dbeff9eef6072eab052753c11`.
- 루트 `project1/part2_2022142233.devsim`은 이전 #11(SHA=f2442ee257af6dfcb610db5928d0ff5d3b8e5bce1d2423d72e00c7fb099fe62e)이다. **95.2 ms 보고서에는 현재 추천 #19 파일이 대응한다.**

남은 필수 준비는 통합 약12쪽 PDF·두 실제 checker OK 화면·올바른 학번 파일 묶음이다. 이름·분반은 **확인 불가**이며 임의 인물을 쓰지 않는다. 없는 화면·그림은 명시적인 삽입 표시를 남긴다. 추가 극한 탐색이나 Data0 최대 시간 측정이 보고서 작성의 필수 선행조건은 아니다.

GPT는 이 문서를 배경 자료로 사용하고 보고서 본문에는 코드 전체·긴 hash·개발 로그를 그대로 붙이지 않는다. ‘시도→지표→판단’과 검증 근거가 보이는 공학 보고서로 재구성한다. 확인되지 않은 출처·수치·실험·성공 화면은 생성하지 않으며 **확인 불가**로 표시한다.
