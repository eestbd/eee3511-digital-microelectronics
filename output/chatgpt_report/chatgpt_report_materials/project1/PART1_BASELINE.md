# Part 1 초기 소자 측정 — 1~5번

> 이 문서의 모델 설명·`results/part1_baseline/` 수치는 공식 Q&A 수신 전 baseline 기록이다. 2026-10-04부터 현재 varshni 경로는 공식 온도 의존 mobility·midgap gate 기준을 적용한다. 최신 조건은 [OFFICIAL_QA.md](OFFICIAL_QA.md), 현재 실행·결과는 [README.md](README.md)와 루트 PLAN/log를 참조한다. 과거 raw·FAIL·source hash는 그대로 보존한다.

이 경로는 동일한 초기 nMOS에서 8개 spec을 측정한다. **6번 설계 변수·조합 탐색은 수행하지 않는다.** Spec FAIL은 측정 실패와 다르며, 측정할 수 없는 항목은 ERROR다. 로컬 모델의 결과이지 조교 채점 통과나 실험 정확성을 보장하는 결과가 아니다.

## 초기 설정과 결과 파일

`part1_baseline.yaml`은 기존 `config.yaml`의 치수·도핑·이동도를 유지한다.

| 항목 | 초기 값 |
|---|---|
| Gate 길이 / source·drain 길이 | 1.0 / 각각 0.5 µm |
| SiO2 두께 / Si 두께 / 접합 깊이 | 10 nm / 0.5 µm / 0.1 µm |
| NA / ND | 1e16 / 1e19 cm^-3 |
| 전자 / 정공 이동도 | 400 / 200 cm²/(V·s), 기존 상수값 |
| Gate 재료 | W, 과제 표의 4.60 eV |
| 도핑 erfc 감쇠 길이 x / y | 12.5 / 5 nm, 기존 profile 유지 |

기존 gate는 재료가 미지정이었다. W는 기존 intrinsic-reference 조건에 가장 가까운 과제 재료로 초기 기준을 정한 것이다. Spec을 맞추기 위해 재료를 탐색한 결과가 아니다.

`results/part1_baseline/`의 결과는 다음과 같다.

- `legacy/`: 변경 전 기존 3종 CLI의 CSV·원본 config·환경 및 source hash manifest.
- `primary/`: 20 mV 간격의 기준 측정. `idvg_low.csv`, `idvg_high.csv`, `idvg_body.csv`, `off_398K.csv`, `metrics.json`, `config.yaml`, `checker.log` 및 진단 구조.
- `fine/`: 동일한 물리 설정, 10 mV 간격으로 측정 안정성을 확인하는 비교 실행.
- `numerical_validation.json`: 측정 간격·단자 전류 보존·double/extended precision·live/export-reload 비교 결과.
- `legacy_regression.json`: 기존 CLI 결과와 변경 전 결과 비교.
- `provenance_review.json`: 실행 중 source 편집에 관한 출처 보완 및 최종 source hash.
- `double_precision_diagnosis.json`, `ion_scale_check.json`, `hw1_scale_reference_check.json`: 독립 double 저전압 진단과 기존 HW1 모델의 전류 규모 확인.

`metrics.json`은 실제 geometry·bias/온도·정밀도·단위·solver 기준·소스 및 구조 hash를 포함한다. CSV에는 signed source/drain/body 전류와 합계 잔차가 있으며, 전류는 A/µm다. µA·pA는 결과를 읽기 쉽게 환산한 단위다.

앞으로 실행할 CLI는 긴 계산 전에 source hash를 확보하고 실제 읽은 config text를 보존한다. 이번 `fine/` 실행은 review 수정과 동시에 진행되어 실행 종료 시 기록된 extractor hash가 시작 때 로드한 버전과 다르다. 작업 순서상 두 실행의 초기 extractor는 `primary/`에 기록된 이전 버전으로 판단하며, 이는 startup snapshot으로 직접 확보한 자료와 구분한다. 최종 extractor로 raw CSV를 재평가한 결과와 출처 보완 사항은 `numerical_validation.json` 및 `provenance_review.json`에 남긴다. 원래 산출물은 덮어쓰지 않는다.

진단 구조 `part1_baseline_diagnostic.devsim`은 **제출 파일이 아니다.** 실제 학번을 확인한 최종 제출에는 `part1_[studentID].devsim` 규칙을 적용해야 한다. 구조를 doping 이후·physics 이전에 저장하며, 저장 파일에는 physics equation·bias·해 변수를 넣지 않는다. 모든 측정 case가 같은 저장 구조를 로드하고 재료를 파일에서 읽는다.

## 실행

Repository root의 PowerShell에서 기존 환경을 사용한다. 출력 경로는 새로운 빈 디렉터리를 지정한다. 기존 결과를 덮어쓰지 않는다.

```powershell
$env:PATH = "$PWD\.conda\Library\bin;$PWD\.conda;$PWD\.conda\Scripts;$env:PATH"
$env:PYTHONIOENCODING = 'utf-8'
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
& .\.conda\python.exe -B -m unittest discover -s .\project1\tests -v
& .\.conda\python.exe -B .\project1\part1.py --output-dir .\project1\results\my_baseline\primary
& .\.conda\python.exe -B .\project1\part1.py --step-v 0.01 --output-dir .\project1\results\my_baseline\fine
& .\.conda\python.exe -B .\project1\validate_part1.py --primary .\project1\results\my_baseline\primary --fine .\project1\results\my_baseline\fine --output .\project1\results\my_baseline\numerical_validation.json --probe-log-dir .\project1\tmp\my_baseline_probes
```

`part1.py`는 8개 측정이 완료되면 exit 0이다. 설계의 spec FAIL 여부는 JSON/표에서 확인한다. 측정 ERROR는 exit 1이며 solver 오류는 예외와 로그로 드러난다. `validate_part1.py`는 수치 안정성 기준 미달 시 exit 1로 결과 JSON을 남긴다. 실행 도중 실패한 디렉터리에는 일부 산출물만 있을 수 있으므로 `metrics.json`과 `measurement_complete`까지 확인한다.

기존 `mosfet.py idvg/idvd/cv --config project1/config.yaml`은 legacy 동작을 유지한다. 이 CLI 결과만으로 새 Part 1 8개 spec을 측정했다고 판단하지 않는다.

## 측정 정의

기본 VS=VB=0, T=300 K. Vth·SS 경계는 양의 전류의 유일한 상승 crossing을 log10(ID)에서 보간한다. 외삽·전류 clamp·여러 crossing 중 임의 선택은 하지 않는다.

| 항목 | 측정 조건 / 계산 | 기준 |
|---|---|---|
| Vth | VD=0.05 V, ID=1e-7 A/µm의 VG | 0.40~0.50 V |
| Ion | 실제 VG=VD=2 V sample | ≥450 µA/µm |
| Ioff | 실제 VG=0, VD=2 V sample | ≤1 pA/µm |
| SS | VD=0.05 V, [VG(1e-8)−VG(1e-10)] / 2 | ≤75 mV/dec |
| 고온 Ioff | T=398 K, VG=0, VD=2 V | ≤100 pA/µm |
| DIBL | [Vth(VD=0.05)−Vth(VD=2)] / 1.95 | ≤30 mV/V |
| Body effect | VD=0.05 V, Vth(VB=−0.5)−Vth(VB=0) | ≤0.08 V |
| Eox | VDD / 실제 저장 구조의 tox | ≤5 MV/cm |

SS는 지정된 2-decade 구간의 평균이다. Eox는 과제 정의의 2 V/tox이며 시뮬레이션의 국소 최대 산화막 전계를 뜻하지 않는다. 조교의 내부 보간·정밀도·세부 모델은 공개되지 않아 로컬 판정과 차이가 날 수 있다.

## Gate 전위 모델

DEVSIM의 기존 Silicon helper는 intrinsic carrier 기준의 전위를 사용하고 body의 Fermi offset을 ohmic 접점에서 이미 반영한다. 따라서 gate에 body doping offset을 중복해서 더하지 않는다.

```text
Vt = kT/q
Nc(T) = 2.8e19 (T/300)^(3/2) cm^-3
Phi_i(T) = chi + Vt ln(Nc(T)/ni(T)), chi=4.05 eV
offset = Phi_M - Phi_i(T)
psi_gate = VG - offset
gate contact residual = Potential - gate_bias + offset
```

에너지의 eV 수치와 전위의 V 수치는 전자 전하로 환산한 위 관계에서 대응한다. 금속 일함수가 0.1 eV 증가하면 같은 상태를 얻는 VG가 0.1 V 증가해야 한다. 이 부호·크기는 W/Mo의 보상 전압 모델 test로 확인했으며, 재료 설계 탐색이 아니다. 균일 p형 MOS의 charge-neutral 전위 및 flat-band 전압을 독립적으로 계산해 300/398 K에서 bulk/oxide 전위와 비교한다.

Gate 재료와 일함수는 과제 PDF/`check_structure_file.py`의 표를 따른다. Gate metal은 physics가 없는 재료 라벨 영역이며 `gate` 접점은 oxide에 있다. 전위 정의의 근거는 [COMSOL 공식 MOSFET 설명의 flat-band 식](https://doc.comsol.com/6.4/doc/com.comsol.help.semicond/IntroductionToSemiconductorModule.pdf)과 [공식 재료 가이드의 Silicon Nc·전자 친화도](https://doc.comsol.com/6.4/doc/com.comsol.help.matlib/MaterialLibraryUsersGuide.pdf)다. 이 자료의 다른 이동도 값으로 기존 이동도를 바꾸지 않았다.

## 온도 모델

`silicon_temperature_model: varshni`를 명시한 새 Part 1 경로에만 적용한다. 기존 설정은 `legacy`이며 ni=1e10을 유지한다.

```text
Eg(T) = 1.17 - 4.73e-4 T²/(T+636) eV
ni(300) = 1e10 cm^-3
ni(T)/ni(300) = (T/300)^(3/2)
                 × exp[Eg(300)/(2k_eV·300) - Eg(T)/(2k_eV·T)]
k_eV = (1.3806503e-23)/(1.6e-19) eV/K
```

Varshni 식과 Silicon 계수의 근거는 [Varshni 원 논문](https://doi.org/10.1016/0031-8914(67)90062-6), [Thurmond의 Silicon 물성 연구](https://doi.org/10.1149/1.2134410), 같은 계수와 DOS 온도 의존성을 명시한 [Silicon DOS 연구](https://www.sciencedirect.com/science/article/abs/pii/S0921452606014578)다. k/q는 로컬 DEVSIM helper와 같게 유지한다. 기존 ni(300)를 보존하는 **empirical normalization**을 사용하므로 Nc·Nv·Eg의 독립적인 절대 물성 fit이나 조교 모델을 재현했다는 주장은 하지 않는다.

| T | Eg | ni | intrinsic 일함수 |
|---|---|---|---|
| 300 K | 1.124519 eV | 1.0000e10 cm^-3 | 4.613121 eV |
| 398 K | 1.097539 eV | 4.7573e12 cm^-3 | 4.599912 eV |

Boltzmann equilibrium·ohmic carrier 조건·수송 및 SRH에 동일한 ni(T)를 전달하며 `n1=p1=ni`도 갱신한다. 수명과 이동도는 기존 상수다. Bandgap narrowing, Fermi–Dirac 통계, field-dependent mobility/velocity saturation, tunneling/gate leakage 등은 이번에 임의로 추가하지 않았다. 300/398 K 이외의 정확성은 검증하지 않았다.

## 검증과 한계

- 독립 exponential 곡선과 edge case의 추출 test, 300/398 K 균일 MOS flat-band 및 gate offset test, 새 프로세스 구조 export/reload test를 수행한다.
- 계산은 로컬 DEVSIM 2.10.0의 extended solver/model/equation으로 수행하고 주요 off/on/문턱 부근 점을 double precision으로 재측정한다. 각 정밀도·측정점은 새 Python 프로세스로 격리한다. Double 고전압 수렴 실패는 독립 프로세스에서도 재현되었다. [DEVSIM 공식 precision 설명](https://devsim.net/solver.html)을 참고했으며 mobility·0.1 V ramp·기존 solver 오차 기준은 유지한다.
- `extended_baseline_checks_pass`는 기준 결과의 안정성, `double_precision_complete`는 double 측정의 완료 여부, `all_checks_pass`는 double 결과까지 포함한 전체 검증이다. Double의 수렴 실패나 기준 미달은 ERROR/false로 보존하고 기준 결과의 PASS로 바꿔 쓰지 않는다.
- 20→10 mV sweep 비교 기준은 Vth/body effect ≤1 mV, SS ≤0.2 mV/dec, DIBL ≤0.5 mV/V이며 판정도 같아야 한다. 동일 bias 전류·전류 보존 기준은 상대 1e-6 또는 절대 1e-17 A/µm 이내다. 이 기준은 측정 검증용이며 과제 spec 상한을 변경하지 않는다.
- DEVSIM 텍스트 직렬화가 mesh 좌표를 아주 조금 반올림하므로 저장/재로딩 bit 동일성을 요구하지 않는다. 실제 전류 재현성으로도 확인한다. Windows loader의 파일 handle은 프로세스 종료까지 유지되어 구조 test를 자식 프로세스로 분리했다.
- Body는 기존 **하단 ideal ohmic** 접점이다. 과제 그림의 표면 p+ body tap과 차이가 있고 checker OK만으로 접점 물리나 최종 설계 적합성을 증명하지 않는다. [Ideal ohmic 모델 설명](https://doc.comsol.com/6.3/doc/com.comsol.help.semicond/semicond_ug_semiconductor.6.63.html)에 해당하는 가정을 유지한 baseline이다.
- Mesh 수렴, 표면 body tap, 접촉 저항/Schottky 모델 및 조교 실제 측정 모델의 일치는 별도 확인이 필요하다. 이번에 설계 변수를 바꾸지 않았다. 원본 `config.yaml`, 기존 결과 및 `hw1/`도 보호한다.

## 이번 측정의 최종 상태

20 mV 기준 결과는 Vth **0.550307 V**, Ion **142.052640 µA/µm**가 미충족이고 나머지 6항목은 PASS다. 10 mV에서도 판정은 같다. Vth는 상한보다 약 50.3 mV 높고 Ion은 목표의 약 31.6%다. 기존 HW1 `SimpleMosfet`에 동일 치수의 Cox/이동도와 측정 Vth를 넣은 square-law 근사 전류는 약 145.07 µA/µm였다. 이는 전류 규모 확인이며 독립 Vth 검증은 아니다.

- **기준 extended 검증 통과:** 14개 unittest, 구조 checker, 20→10 mV 측정 간격·공통 전압점·전류 보존, 10개 live/reload replay, 최종 extractor의 raw CSV 재평가, 기존 3종 CLI 회귀.
- **Double 전체 비교 미완료:** 5점 중 저전압/문턱 부근·body bias 2점은 완료했다. 고전압 off/on은 VG=0의 초기 drain ramp에서 VD=1.7 V, 398 K off는 VD=1.3 V에서 수렴 실패했다. Target gate에 도달하기 전 실패이므로 double Ion 값을 측정했다고 주장하지 않는다.
- `numerical_validation.json`은 `extended_baseline_checks_pass=true`, `double_precision_complete=false`, `all_checks_pass=false`다. Validation CLI의 exit 1은 이 double 비교 실패를 반영한다. 실패를 허용 오차 조정으로 제거하지 않았다.
- 같은 설정의 extended는 수렴하고 double은 전자 방정식 상대 오차 약 1.90e-3에 정체된 관찰이 수치 정밀도 한계를 뒷받침한다. 내부 연산의 상세 발생 원인을 완전히 특정한 것은 아니다. 기준 결과의 최대 단자 전류 보존 상대 잔차는 약 3.87e-16이다.

전체 8개 결과표·쉽게 읽는 해석·검증 실패와 한계는 repository root `PROGRESS_LOG.md`의 이번 작업 최종 기록과 raw/JSON을 함께 확인한다. **1~5번 완료, 6번 미실행이며 사용자 결과 확인 대기 상태다.**
