# PLAN.md

현재 요청의 계획·상태를 유지하며 시간순 이력은 append-only `PROGRESS_LOG.md`에 누적한다.

현재 작업: Project 1 Part 1 순서 1~5 구현·검증과 초기 소자 baseline
상태: 이번 요청 완료 — 1~5번 구현·초기 측정·검토 완료, 사용자 확인 대기. 6번 설계 탐색 미실행.
최종 갱신: 2026-10-04 (Asia/Seoul)

## Goal

앞서 분석한 1~5번(측정 기준·기존 baseline 보존, 제출 구조, 누락 physics 보완·검증, 8항목 measurement, 초기 소자의 결과표)을 완료한다. 결과와 원인을 사용자가 이해할 수 있도록 PROGRESS_LOG에 기록한다. 6번 설계 변수 탐색은 사용자 확인 이후의 별도 요청까지 실행하지 않는다.

## Current State

- 시작 시 Git HEAD는 8809257eb154ecdbeeacd55f4f0cbf6857302fbf이고 worktree는 깨끗했다. Tracked 파일 69개의 해시와 기존 로그 byte를 확보했고 원본 config/결과/PDF·HW1을 보호한다.
- 기존 Id–Vg/Id–Vd/C–V 경로를 유지하면서 gate 재료/일함수·구조-only 저장/reload·8항목 evaluator와 Part 1 전용 CLI를 추가했다.
- Body bias를 workflow에도 노출했다. 새 Part 1 온도 모델은 ni/n1/p1을 300/398 K에서 갱신하며 도핑 erfc 감쇠 길이는 mesh와 독립이다. 기존 config는 legacy physics다.
- Body는 기존 bulk 아랫면의 ideal ohmic 접점을 유지하며 PDF의 표면 p+ tap 예시와의 차이는 제한사항이다.
- 초기 W 소자의 20/10 mV 결과는 각각 8개 모두 측정 완료, 동일한 6 PASS/2 FAIL이다. 14개 단위/native/입력 보존 test·기존 3종 CLI 회귀·extended 기준의 간격/전류 보존/재로딩 검증이 통과했다. Double 비교는 5점 중 3점의 초기 bias ramp 수렴 실패로 완료되지 않았다.
- 과제 기준은 PDF 실제 41/42·50/51쪽, 제출·이름 규약은 45~48·54~57쪽을 따른다.

## Requirements

- 기존 code/config/CSV·HW1 reference를 기준으로 보존하고 비교 증거를 확보한다.
- 구조는 bulk/Silicon, oxide/Oxide, gate_metal/표의 이름, gate/source/drain/body, bulk_oxide, bulk.NetDoping을 포함한다. gate 접점은 oxide에 유지한다. 파일은 doping 이후·physics 이전에 저장하고 소자는 하나만 포함한다.
- Part 1의 gate 일함수를 intrinsic potential 기준과 일관되게 적용하고, 300/398 K의 carrier·SRH intrinsic 값 갱신을 검증한다. Mobility·ramp·허용 오차를 spec 통과 목적으로 조정하지 않는다.
- 같은 구조·도핑·gate 재료에 8항목을 측정한다. 기본 VS=VB=0, T=300 K이며 body 항목만 VB=-0.5 V, 고온 항목만 T=398 K다.
- Vth: VD=0.05 V, ID=1e-7 A/µm, 0.40~0.50 V. Ion: VG=VD=2 V, ≥450 µA/µm. Ioff: VG=0/VD=2 V, ≤1 pA/µm.
- SS: VD=0.05 V, ID=1e-10~1e-8 A/µm의 평균, ≤75 mV/dec. 고온 Ioff≤100 pA/µm. DIBL=(Vth_low−Vth_high)/1.95, ≤30 mV/V. Body effect=Vth(VB=-0.5)−Vth(VB=0)≤0.08 V. Eox=2 V/tox≤5 MV/cm.
- 측정 실패·전류 구간 미도달·solver 문제를 실패 상태로 명시한다. 결과를 clamp하거나 외삽해 숨기지 않는다.
- 기존 CLI/config/workflow 기본 동작을 보존한다. Physics는 project1의 모듈에 두고 설치된 DEVSIM package나 HW1을 수정하지 않는다.
- 결과 CSV·JSON·해시·측정 정의·실행 방법을 저장하고 PROGRESS_LOG에 읽기 쉬운 결과표와 제한사항을 남긴다.
- 최종 목표는 baseline의 모든 spec을 정직하게 측정하는 것이다. 이번 단계에서 spec 통과를 위해 설계 변수를 바꾸지 않는다.

## Assumptions

- 기존 치수·NA/ND·mu_n=400/mu_p=200·ramp/solver 기준을 유지한다. Gate가 미지정이므로 기존 intrinsic-reference gate에 가까운 W(4.60 eV)를 기준으로 하나 정한다. 재료 sweep이나 spec에 맞춘 선택은 하지 않는다.
- 새 Part 1 physics는 명시적으로 선택하고 기존 YAML/CLI는 legacy 동작을 유지한다. ni(T)는 기존 ni(300)=1e10 cm^-3에 고정한 Varshni Eg(T)와 DOS T^(3/2) 비율로 계산한다. 계수와 근거를 문서화한다.
- Gate boundary는 psi_gate=VG+[chi+Vt*ln(Nc/ni)]−PhiM를 사용한다. Body doping의 Fermi offset은 기존 ohmic 접점에 이미 있으므로 중복 반영하지 않는다. chi=4.05 eV와 Nc300=2.8e19 cm^-3의 출처를 확인한다.
- 이상적 ohmic body 접점의 하부 배치는 baseline에 유지한다. PDF p+ tap 예시와의 차이를 한계로 명시한다. Checker는 이를 금지하지 않으며 Schottky/contact-resistance 모델의 의무 조건이나 계수는 공개되어 있지 않다. 실제 제출 설계에서 표면 tap은 후속 검토한다.
- 실제 학번을 추측하지 않는다. 이번 구조 파일은 part1_baseline_diagnostic.devsim이며 제출 파일이 아니다.
- SS 평균은 VG(I=1e-8)−VG(I=1e-10)를 2 decade로 나눈 값이다. Vth·SS 경계는 log10(ID)에서 bracket 보간하고 전압 간격 감소로 확인한다. 조교 세부 추출법·허용 오차는 미공개다.
- 새 고온 모델은 bandgap·ni·n1/p1을 일관되게 갱신한다. 기존 상수 mobility·수명, Boltzmann 통계·ideal ohmic·SRH를 유지하며 velocity saturation/BGN/tunneling 등을 검증 없이 추가하지 않는다.
- 결과는 검증한 로컬 모델의 baseline이다. 구조 checker 통과·단위/추출 test·모델 내부 일관성과 조교 채점 통과/실험 정확성은 구분한다.

## Plan

- [x] M1 — 기존 3종 CLI 결과·설정·환경·source hash를 별도 경로에 보존하고 측정 정의·모델 근거를 확정한다.
- [x] M2 — gate_metal·재료 선택·구조-only export와 reload를 추가하고 새 프로세스 checker와 구조 내용 검증을 수행한다.
- [x] M3 — Part 1 gate boundary·ni(T)/SRH 갱신과 mesh/도핑 길이 분리를 구현한다. 물성·평형·work-function 부호/크기를 독립적으로 검증한다.
- [x] M4 — bias/온도 조건과 8항목 추출·판정·오류 처리를 구현하고 의미 있는 단위·edge-case test를 실행한다.
- [x] M5 — 같은 초기 소자에서 raw sweep·조건·8항목 결과표를 생성한다. 전압 간격·작은 전류 안정성·구조 reload 결과를 확인하고 해석을 기록한다. Extended 기준 검증 통과, double의 실패/제한사항을 분리해 보존했다.
- [x] 마무리 — 전체 diff·기존 3종 회귀·HW1/결과 보호·문서/로그/산출물 일치를 review하고 문제 수정 및 final validation 후 사용자 확인 대기로 종료한다. 이는 설계 탐색 6번이 아니다.

## Validation

- Legacy: 기존 config로 idvg/idvd/cv 실행, 각각 21/21/31점·단위·유한값을 보존하고 변경 후 같은 결과와 비교한다.
- Structure: physics/bias/result 이전 저장, 하나의 device, 필요한 이름·재료·NetDoping·geometry·node/edge 모델 확인. 새 Python 프로세스에서 checker와 reload 검증.
- Physics: Eg/ni(300·398), SRH n1=p1=ni, gate 기준/부호, 재료 차이에 따른 gate potential/Vth 변화, 평형 carrier·접점 일관성을 확인한다. 이 검증의 재료 비교는 모델 구현 검증이며 설계 탐색이 아니다.
- Measurement: 독립 exponential Id–Vg 기대값으로 Vth/SS/DIBL/body effect·단위 환산, exact crossing·비유한 값·비단조·구간 부족·solver 실패를 검증한다.
- Baseline: low/high VD·body bias sweep와 398 K off-point, VG=VD=2의 Ion, Eox 계산. Raw currents와 수렴·전류 보존을 함께 저장한다. 전압 간격을 줄여 추출 변화와 작은 전류 재현성을 확인한다.
- Scope: 원본 config/CSV/PDF·HW1·환경 hash를 비교하고 설계 탐색이나 spec용 상수 조정이 없음을 확인한다.
- Memory: PLAN 8개 section·실제 checklist와 최신 log의 상태를 맞추고 과거 log byte prefix·필수 항목·KST 시간순서를 검증한다.

## Progress / Discoveries

- 앞선 분석의 핵심 요구사항과 현재 코드/helper를 재확인했다. 사용자는 5번 baseline 결과를 본 뒤 6번 탐색을 진행하므로 이번 요청의 종료 지점은 검증된 초기 소자 결과표다.
- DEVSIM 2.10.0 로컬 설치는 extended precision을 지원한다. 필요 시 PDF에 명시된 정밀도 검증을 별도로 수행하며 ramp나 physics 상수를 임의 변경하지 않는다.
- M1: 변경 전 CLI idvg/idvd/cv가 21/21/31점·유한값으로 정상 종료했다. project1/results/part1_baseline/legacy에 CSV·원본 config·환경/명령/source hash manifest를 보존했다. 기본 Ion(VD=VG=2)은 약 139.625 µA/µm이며 아직 Part 1 physics를 적용한 결과는 아니다.
- Gate 기준 전위는 COMSOL 공식 MOSFET 설명의 flat-band 정의 및 chi/Nc 자료로 대조했다. ni(T)는 300 K 기존 값에 anchor하는 Varshni/DOS 모델이며 empirical normalization과 기존 mobility·수명 가정을 명시한다. 실제 조교 모델과 동일하다고 주장하지 않는다.
- M2: gate 재료 라벨과 physics 이전 export/reload를 구현했고 새 프로세스 checker가 OK였다. 파일에 equations·Potential/Electrons/Holes·bias parameter가 없음을 확인했다. Live gate 라벨 추가 전후 bulk mesh와 doping은 정확히 동일하다.
- Reload 데이터의 매우 엄격한 비교가 실패해 원인을 조사했다. 저장 좌표의 소수점 직렬화로 x 차이≤5.42e-20 cm, y≤6.78e-21 cm, 도핑 차이≤1.22e5 cm^-3(ND의 약 1.22e-14)가 생겼다. Live 구조 변경은 0 차이였으며 profile 설계 변경이 아닌 직렬화 roundoff였다. 비교는 bit 동일성과 물리 규모 기준을 구분하고 실제 전류 재현성도 확인한다.
- M3: gate offset 및 ni/n1/p1 갱신·도핑 감쇠 길이 독립화를 구현했다. Uniform MOS flat-band 검증에서 300/398 K의 bulk/oxide 전위가 독립 charge-neutral 기대값과 각각 1.23e-15/5.56e-17 V 이내로 일치했다. ni(398)=4.7573e12 cm^-3이며 ni(300)=1e10을 유지한다.
- M4에서 8항목 추출·오류 판정, 진단 구조에서 모든 case를 재로딩하는 실행 경로와 독립 곡선/native model test를 작성했다. Part 1의 pA 누설을 검증하기 위해 PDF가 허용한 extended precision으로 기준 계산하고 double precision도 별도 비교한다. Ramp·solver 허용 오차는 기존 값 그대로다.
- M4 완료: 독립 exponential 곡선의 8개 기대값·단위, 실제 endpoint, 미도달/중복 crossing·비유한값·음수 전류, 물리 모델 및 구조 export/reload의 13개 test가 통과했다. 처음에는 Windows에서 load_devices가 열린 파일을 device/mesh 삭제 뒤에도 프로세스 종료까지 유지해 temporary-directory cleanup이 실패했다. write 직후/로드 직후/clear 직후 rename으로 원인을 분리했고, 구조 test를 자식 프로세스로 격리해 정상 정리하도록 수정했다. 설치 package나 solver 설정은 변경하지 않았다.
- M5 수치 검증은 같은 구조의 20→10 mV sweep 간격 비교, double/extended 전류 비교, live/export-reload 전류 비교 및 단자 전류 보존을 사용한다. Sweep 차이는 Vth/body effect 1 mV·SS 0.2 mV/dec·DIBL 0.5 mV/V 이내, 동일 bias 전류 재현은 상대 1e-6 또는 절대 1e-17 A/µm 이내를 기준으로 삼는다. 이는 spec 기준 변경이 아니라 측정 안정성 점검이며 미달하면 차이와 원인을 기록한다. Mesh 수렴과 실제 조교 모델 비교는 이번 단계에서 보장하지 않는다.
- 초기 20 mV 측정의 8개 항목이 모두 완료됐다(ERROR 없음). 6개 PASS, Vth=0.550307 V 및 Ion=142.052640 µA/µm는 FAIL이다. 실패를 없애기 위해 설계값을 바꾸지 않았다. 10 mV 비교 계산은 진행 중이다.
- Legacy 회귀의 최초 상대 1e-9/절대 1e-24 비교는 VG=0의 2.25e-23 A/µm 차이로 실패했다. HEAD의 원본 코드를 scratch에 추출해 같은 환경에서 반복했고 원본도 최대 1.69e-20 A/µm의 재실행 차이가 있었다. 원본/새 코드의 bulk x/y/NetDoping은 bit 동일하다. 이미 정한 전류 검증의 절대 floor 1e-17 A/µm와 상대 1e-9로 평가한 21/21점 I–V가 통과했고 전압 열·31점 C–V는 정확히 동일했다. 작은 수치 잔차와 functional regression을 구분한 근거를 legacy_regression.json에 보존했다.
- Final review에서 exact target sample의 양옆을 검사하지 않아 하강 crossing/target에 접하기만 하는 곡선을 측정할 수 있는 bug를 발견했다. 3개 재현 사례가 실패함을 확인하고 유일한 상승 crossing 조건으로 수정했으며 13개 test가 다시 통과했다. 기존 raw baseline에는 이 사례가 없지만 최종 extractor로 CSV를 재추출해 저장 결과와 일치를 확인한다. 원래 실행 source hash는 그대로 보존하고 최종 extractor hash·재검증은 numerical_validation.json에 별도로 남긴다.
- 10 mV 측정도 8개 모두 완료됐고 6 PASS/2 FAIL 판정이 같다. 20 mV와 Vth 차이 0.35152 mV, SS 0.03638 mV/dec, DIBL 0.13172 mV/V, body effect 0.07181 mV다. Ion/Ioff/고온 Ioff/Eox 값은 같다.
- 최초 한 프로세스의 extended→double 비교에서 수렴 실패가 났다. 새 프로세스 double의 VD=0.05/VG=0 진단은 수렴했지만 단자 전류 보존 상대 잔차 약 1.01%, 절대 1.90e-17 A/µm였다. 정밀도 전환/프로세스 상태의 영향을 분리하기 위해 각 case·정밀도 replay를 새 프로세스로 실행하도록 validation 계획을 수정했다. Solver/ramp/물리 설정은 유지하고 실패·잔차를 별도 기록한다.
- Source/config snapshot을 계산 종료 시 다시 읽는 provenance bug를 확인했다. Fine 계산 중 extractor를 수정했으므로 fine JSON의 extractor hash는 시작 때 로드한 버전과 다를 수 있다. 향후 CLI는 계산 전에 source hash와 실제 읽은 config text를 보존하도록 수정했고, 계산 중 disk 파일이 바뀌는 독립 회귀 test를 추가해 14개 test가 통과했다. 이번 산출물은 덮어쓰지 않고 provenance_review.json에서 출처를 보완하며 최종 extractor로 재평가한다.
- 독립 프로세스 replay 15개를 완료했다. Extended live/reload 10개 모두 전류/전류 보존 기준을 만족했고 최대 기준 전류 차이는 약 7.70e-18 A/µm다. 두 raw dataset의 최종 extractor 재평가도 원래 결과와 일치했다. numerical_validation.json의 extended_baseline_checks_pass=true다.
- Double은 저전압/문턱 부근·body bias 2점만 측정/비교를 완료했고, 고전압 off/on 및 398 K off 3점은 target gate 설정 전 drain ramp에서 실패했다(300 K VD=1.7 V, 398 K VD=1.3 V). 독립 프로세스에서도 재현되어 정밀도 전환에만 한정된 문제라는 초기 가능성은 지지되지 않는다. 300 K ElectronContinuity 상대 오차가 약 1.90e-3에 정체되고 Potential 오차는 약 1e-13였으며 같은 설정의 extended는 수렴했다. 수치 정밀도 한계를 뒷받침하지만 내부 발생 연산을 완전히 특정한 것은 아니다. double_precision_complete=false/all_checks_pass=false를 유지한다.
- 기존 HW1 SimpleMosfet을 읽기 전용으로 이용한 square-law 규모 확인에서 약 145.07 µA/µm였고 TCAD는 142.05 µA/µm다. 측정 Vth를 입력으로 쓰는 근사 비교이며 독립 Vth 검증이나 조교 정확성 증거가 아니다.

## Final Review

- 승인 범위 1~5번 완료. Gate 재료/일함수, 구조-only export/reload, 300/398 K ni/SRH, body 조건 및 8항목 추출을 구현했다. 6번 설계 변수 탐색은 하지 않았다.
- 20 mV 기준: Vth=0.550307 V(FAIL), Ion=142.052640 µA/µm(FAIL), Ioff=0.003296 pA/µm, SS=69.035679 mV/dec, 398 K Ioff=34.431302 pA/µm, DIBL=13.431727 mV/V, body effect=0.042099 V, Eox=2 MV/cm(나머지 PASS). 10 mV에서도 판정이 같다.
- 실행 검증: 14개 unittest 통과, 새 프로세스 구조 checker OK 및 physics/해 변수/bias 없는 저장 확인, 균일 MOS flat-band·work-function 부호/크기 확인, 기존 idvg/idvd/cv 21/21/31점 회귀 통과, 같은 구조의 101/201점 sweep 비교와 10개 extended live/reload replay 통과. 기준/미세 sweep 단자 전류 보존 최대 상대 잔차는 약 3.87e-16이다.
- 발견 문제를 수정했다: Windows loader 파일 잠금의 test 격리, exact target의 잘못된 crossing 허용, 계산 중 편집에 취약한 source/config snapshot. 원본 산출물은 보존하고 출처 및 최종 extractor 재평가 기록을 추가했다.
- 원본 config/CSV/PDF·HW1 등 보호 대상 63개 tracked 파일의 SHA256은 시작과 같다. 변경된 기존 파일은 AGENTS/PLAN/PROGRESS_LOG 및 project1의 config/simulator/workflows 6개뿐이다. 환경/설치 package, mobility·ramp·solver 허용 오차는 변경하지 않았다.
- 제한사항: Double 전체 비교는 3점 수렴 실패로 미완료이며 전체 수치 검증을 PASS라고 주장하지 않는다. Extended 기준의 안정성만 검증했다. 하단 ideal ohmic body, 상수 이동도·수명/Boltzmann/SRH 모델을 유지했고 mesh 수렴·표면 p+ tap·추가 고농도/고전계 물리·조교 모델 일치는 미검증이다. 진단 구조는 실제 학번을 넣은 제출 파일이 아니다.
- 결과·원인·8개 표·검증 실패와 한계는 PROGRESS_LOG 최종 기록, 모델/실행은 project1/PART1_BASELINE.md, raw 및 JSON은 project1/results/part1_baseline에 남겼다. 최종 diff·문서/산출물 일치·append-only 보존을 확인한다. 다음 동작은 사용자의 결과 확인 이후 별도 요청에 따른 6번이다.
