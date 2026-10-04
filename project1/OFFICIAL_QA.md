# Project 1 공식 Q&A와 현재 구현 대조

수신일: 2026-10-04, Asia/Seoul. 사용자가 제공한 교수·조교 수업 톡방 공식 답변 정리본을 근거로 한다. 원래 답변별 날짜는 미제공이며 아래는 당시 작업 이력을 재구성한 것이 아니다.

조건 기준은 [최신 PDF](Project1_Assignment_0927.pdf)와 이후 교수·조교의 공식 확인이다. 후속 공식 답변이 명확히 확인한 구조·설계 자유도는 PDF 예시의 해석을 보완한다. 이전 assignment/HW1/manual보다 9월 27일 개정 Part 2 조건을 사용한다. 이 문서는 공식 조건의 지속 참조 자료이며 현재 작업 상태는 [PLAN](../PLAN.md), 시간순 이력은 [PROGRESS_LOG](../PROGRESS_LOG.md)에서 관리한다.

## 공통·제출

- 마감: **2026-10-07 23:59 KST**.
- 보고서 PDF, `part1_[학번].devsim`, `part2_[학번].devsim` 제출. 두 구조의 self-check OK 결과 화면을 보고서에 포함한다. 약 12페이지가 기준이며 조금 넘는 것은 허용된다. 지나치게 작은 글씨·좁은 간격으로 분량을 맞추지 않는다.
- 조교는 저장 구조를 재시뮬레이션한다. 구조는 doping 적용 후, physics 구축 전에 저장한다. 실행 성공·구조 검사 통과·전기적 spec 충족은 별도 증거다.
- 분석→설계→검증→재설계 과정을 기록한다. 문제, 변경 변수, 선택 이유, metric 변화, 다음 결정을 남긴다. 실패도 실제 조건과 함께 보존한다.
- 그림은 구조를 이해할 수준이면 된다. Part 1에는 접점·Lg/tox/xj·doping·gate 재료, Part 2에는 pass transistor·storage/dielectric/plate·BL/WL·주요 치수/재료를 표시한다.

## Part 1 공식 조건

- 최신 PDF의 8개 spec을 **동일 구조·doping·gate 재료**로 평가한다. 정확한 bias·수치는 PDF와 [AGENTS](../AGENTS.md)의 Part 1 표를 사용한다.
- 개발 시 ramp<0.1 V(예: 0.05 V)는 허용된다. 채점은 **0.1 V ramp·128비트 확장 정밀도**다. `extended_solver`, `extended_model`, `extended_equation`을 모두 켜는 것이 권장된다. Ramp를 바꿔 다른 DC 값을 얻는 것으로 실패를 숨기지 않는다.
- `ni(T) ∝ T^1.5 exp[−Eg(T)/(2kT)]`, ni(300 K)=1e10 cm⁻³로 normalize. Varshni Eg(300)≈1.1245 eV, Eg(398)≈1.0975 eV. ni·SRH n1/p1·gate offset의 Eg/2에 같은 온도 모델을 사용한다.
- `μn(T)=400*(T/300)^(-2.4)`, `μp(T)=200*(T/300)^(-2.2)` cm²/(V·s). 채점기에는 velocity saturation·doping-dependent mobility가 없으므로 임의로 추가하지 않는다.
- `Potential = VG−Φms′`, `Φms′=Φm−[χ+Eg(T)/2]`, χ=4.05 eV. 398 K에서도 Eg(T)를 사용한다.
- 누락 physics는 HW1의 부족한 모델과 필요성을 설명하고 실제 구현·검증한다. Helper의 다른 함수를 호출했다는 사실만으로 충족했다고 판단하지 않는다.
- 보고서 1(b)는 실제 optimization 이력이며 다변수 변경 가능. 1(c)는 한 번에 한 knob씩 바꾸는 ablation으로 원인을 설명한다. 두 실험 목적을 구분한다.
- p-body background NA 범위와 p+ contact tap은 별개다. 별도 p+ tap 고농도는 허용된다. 예제 NA=7e16·tap=1e19 cm⁻³는 필수값이 아니다. 별도 tap이 있으면 `NetDoping=SourceDoping+DrainDoping−NA−TapDoping`처럼 실제 profile에 반영한다.

## Part 2 최신 조건

구버전 retention BL=1 V·read 판정 1 ns·40 mV는 **사용하지 않는다**.

| 항목 | 최신 기준 |
|---|---|
| 공통 | VDD=2 V, T=398 K, VB=−0.5 V |
| Pass transistor | Lg=0.3 µm 고정, W=100 nm=0.1 µm, tox≥5 nm |
| READ | BL precharge=1 V, WL=2.5 V, CBL=100 fF, dt=10 ps |
| Storage | CSTORE≤20 fF, source 위 capacitor, plate bias=VDD/2=1 V |
| Data 0/1 | 초기 Vcell=0/2 V, 두 상태 모두 0.5 ns에 \|VBL−1 V\|≥60 mV |
| Retention | WL=0; data 0 BL=2 V, data 1 BL=0 V; ≥64 ms |

- 최신 PDF: capacitor height 0.2…1.5 µm, dielectric thickness 3…10 nm, SiO2(κ=3.9)·Al2O3(9)·HfO2(20)·ZrO2(35). Gate 전계 2.5 V/tox≤5 MV/cm, capacitor 전계 1 V/tdiel≤4 MV/cm.
- Pass transistor와 capacitor를 한 device 구조로 저장한다. PDF/checker의 bulk/oxide/gate_metal, bulk_oxide, NetDoping 및 hk/storage/plate naming을 따른다. Plate contact 전체 전하의 dQ/dV로 plate bias 1 V에서 실제 CSTORE를 추출한다.
- READ: DC solve→signed terminal current→ΔQ=IΔt→두 capacitor 전압 갱신→다음 DC solve. 각 terminal current를 쓰거나 하나의 공통 current를 쓰는 방식 모두 허용되며 선택·부호·전하 보존 검증을 설명한다. 기존 A/µm 전류에 W=0.1 µm를 정확히 한 번 곱한다.
- READ 그래프는 data 0/1 VBL(t), 0.5 ns의 ΔVBL과 60 mV 기준을 보여준다. 가능하면 0.5 ns 세로선과 ±60 mV 기준선을 표시한다.
- Retention은 storage-node charge 변화에 해당하는 전류로 Vcell을 추적한다. READ와 달리 큰/adaptive dt를 사용하되 step당 Vcell 변화가 수 mV 이하가 되도록 제한한다.
- Retention failure는 임의 Vcell threshold가 아니다. **열화된 Vcell에서 BL=1 V로 다시 0.5 ns READ하여 |ΔVBL|<60 mV가 되는 최초 시각**이다. 두 저장 상태를 각각 검사한다. 64 ms 이상이 필수이며 길수록 좋다.
- Vth↓는 READ 전류/속도 개선과 leakage/retention 악화를 함께 만들 수 있다. CSTORE↑는 margin·retention에 유리하지만 ≤20 fF 제약이 있다. TR과 capacitor를 함께 설계한다.

## 추가 공식 Q&A: Part 2 구조·설계 자유도

수신일: 2026-10-04, Asia/Seoul. 사용자가 전달한 장이준 조교의 추가 공식 확인을 근거로 한다. 답변 자체의 시각은 미제공이다. 아래 내용은 허용 범위이며 새 후보의 spec PASS 또는 현재 코드의 비균일/asymmetric profile 지원 완료를 뜻하지 않는다.

### Capacitor 배치

- Source n+ 윗면 전체의 source contact 바로 위에 metal pillar와 hk_l/hk_r slab을 배치해도 된다. Bare n+ silicon 위 배치나 source contact 축소를 강제하지 않는다.
- 이 배치에서 hk 바닥이 bulk silicon에 직접 닿지 않아 bulk_hk_l/bulk_hk_r interface가 node 0개여도 조교 테스트상 문제가 없다고 확인됐다. 이 확인 때문에 접하지 않는 영역에 interface를 새로 만들 필요는 없다.
- 판정의 핵심은 self-checker 통과, naming rule, storage=source/plate=VDD/2 연결, plate 전체 dQ/dV로 정상 CSTORE 추출이다. 구조 허용과 READ/retention 충족은 따로 검증한다.

### 비균일·비대칭 doping

- 허용 범위 안의 spatially nonuniform doping과 source/drain asymmetric design이 가능하다.
- 채점기는 제출 구조의 bulk.NetDoping spatial distribution을 그대로 읽는다. Source/drain별 profile, 국소 도핑 등의 실제 최종 분포를 NetDoping에 반영한다.
- 제출 구조는 조교가 인식하지 못하는 LDDDoping/HaloDoping 등 새로운 node-model 이름에 의존하면 안 된다. 새 profile 도입 시 저장·fresh reload한 NetDoping의 위치별 값과 구조 checker를 검증한다.

### Part 1과 Part 2의 독립 설계

- Part 1은 해당 8개 electrical spec을 만족하는 nMOS, Part 2는 DRAM READ/retention에 맞춘 pass transistor+capacitor co-design이다. 두 transistor parameter가 같을 필요는 없다.
- Part 1 physics/code/simulation infrastructure/설계 경험은 재사용할 수 있지만 Part 2 최종 parameter는 독립적으로 정한다.
- Part 2는 Lg=0.3 µm 고정, gate 전계=2.5 V/tox 등 고유 조건으로 최적화한다. 완료된 Part 1 결과는 보존한다.
- 후속 실험에서 gate/cap 조정과 함께 비균일·비대칭 doping도 후보로 검토할 수 있다. 이번 Q&A 반영에서는 코드/입력 변경이나 실험을 수행하지 않는다.

## 2026-10-04 15:25 최초 구현 대조 결과

이 표는 코드·기존 결과·최신 PDF를 직접 조사한 상태다. 이번에 모델을 수정하거나 새 simulation을 수행하지 않았다.

| 항목 | 현재 구현 | 공식 조건과의 관계 |
|---|---|---|
| Part 1 측정 | 8개 spec·same structure reload·10회 탐색·후보 2개 fine/검증 | 경로 구현됨. 공식 모델 재측정 필요 |
| Eg/ni/SRH | Varshni·ni300 anchor·n1/p1 적용 | 공지 식/anchor와 일치. 실제 채점기 전체 동일성은 미확인 |
| Mobility | 300/398 K 모두 μn=400, μp=200 | **고온 T 의존 법칙 누락**. 398 K 공식값 약 202.970/107.388 |
| Gate offset | Φm−[χ+Vt ln(Nc/ni)] | **공지 χ+Eg(T)/2와 다름**. Offset 차이 300 K +0.8615 mV, 398 K +1.1430 mV |
| 수치 조건 | Extended 3종=true, ramp=0.1 V | 알려진 채점 설정과 부합. Double 실패를 필수 채점 실패와 구분해야 함 |
| 전체 validator | Extended와 double PASS를 AND | 채점 요구보다 넓은 판정. 기존 false/실패는 보존하고 향후 필수/진단 판정 분리 제안 |
| Body | 바닥 ohmic contact, 별도 p+ tap 없음 | PDF 그림과 차이. Q&A가 허용한 tap을 검토; 예제 형태의 의무 여부는 단정하지 않음 |
| Part 2 | Checker naming 검사만 존재 | 구조·CSTORE·READ·retention 미구현. 기존 Part 1 Lg=0.6·tox<5 후보를 그대로 사용 불가 |

기존 후보 #10/#8의 “8 PASS”는 **당시 모델에서의 결과**로 보존한다. Double 실패만으로 채점 탈락이라고 설명한 해석은 새 공지로 정정한다. 현재 가장 먼저 할 일은 추가 탐색이나 double 통과 강제가 아니라 **물리 모델 정합화→기존 소자 재측정**이다. 수정 후에도 기존 후보가 통과할지는 아직 알 수 없다.

첫 구현 제안은 T 의존 mobility·gate offset의 최소 수정과 독립 test다. 전체 Part 1→Part 2 순서는 PLAN에 있다. 첨부 §7에 따라 사용자가 계획을 확인한 뒤 구현을 시작한다.

이후 사용자는 기존 후보를 보존하고 해당 두 식부터 수정하는 방법을 승인했다. 위 표는 **수정 전 조사 상태**이며 이후 구현·측정 상태는 PLAN 및 최신 PROGRESS_LOG를 따른다. 조건 자체는 그대로 적용한다.
