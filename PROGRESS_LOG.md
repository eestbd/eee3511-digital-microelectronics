# PROGRESS_LOG.md

이 저장소의 의미 있는 작업 이력을 시간순으로 누적하는 append-only log다. 현재 목표·계획·상태는 `PLAN.md`, 기본 작업 규칙은 `AGENTS.md`에서 관리한다.

시간대: Asia/Seoul (KST, UTC+9).
기록 표제: `## YYYY-MM-DD HH:mm:ss KST`.
기존 기록을 수정·삭제·덮어쓰거나 재정렬하지 않는다. 정정은 대상 기록의 시각과 이유를 포함한 새 기록으로 남긴다.

## 2026-10-04 00:49:58 KST

### 수행한 작업

- M1: 기존 AGENTS·PLAN, Git 상태와 누적 로그 유무를 확인했다.
- 현재 요청의 목표·요구사항·가정·milestone·validation으로 PLAN을 갱신하고 PROGRESS_LOG를 초기화했다.

### 현재 상태

- 조사와 계획 수립이 완료되었다. 기존 코드·설정·결과·reference 77개 파일의 SHA-256 기준값을 확보했다.
- 이번 변경 범위는 PROGRESS_LOG 생성과 AGENTS·PLAN의 문서 갱신이다. Logging 규칙 연결과 최종 validation은 남아 있다.

### 발견 / 이슈

- 기존 누적 로그는 없었다. 이전 작업의 정확한 시각을 알 수 없어 로그는 이번 요청부터 기록한다.
- 기록 시각은 조회한 UTC 현재 시각을 명시적으로 UTC+9로 변환한다.

### 다음 작업

- AGENTS에 기록 trigger·필수 항목·KST·append-only·최종 기록과 PLAN 동기화 규칙을 추가한다.
- 구현 완료 기록을 append한 뒤 형식·이전 내용 보존·변경 범위를 검증한다.

## 2026-10-04 00:51:07 KST

### 수행한 작업

- M2: PROGRESS_LOG를 생성하고 AGENTS의 기본 workflow·PLAN 운영·최종 review에 progress logging을 연결했다.
- Append-only 보존, KST 기록, 네 가지 필수 section, 중요한 검증·계획 변경 이유, 정정과 최종 기록 규칙을 추가했다.

### 현재 상태

- M1 조사·계획과 M2 logging 문서 연결이 완료되었다.
- PLAN의 현재 요청·요구사항·가정·milestone을 갱신했다. 실제 project feature·환경·참조 코드는 변경하지 않았다.

### 발견 / 이슈

- 과거 기록의 당시 상태는 보존하고 최신 기록과 PLAN의 현재 상태를 비교해야 한다.
- 문서만 변경하므로 TCAD·GUI·CLI·구조 checker는 이번에 재실행하지 않는다. 형식·append 보존·변경 범위 검증은 다음 milestone에서 수행한다.

### 다음 작업

- 모든 기록의 필수 항목과 KST 시간순서를 검증한다.
- 기존 기록의 byte prefix, 보호 파일 77개의 해시, 문서 diff와 PLAN 동기화를 검토한 뒤 최종 종료 기록을 append한다.

## 2026-10-04 00:53:34 KST

### 수행한 작업

- M3 완료: 기록 형식·KST 시간순서·append-only 보존·문서 상태·변경 범위를 검증하고 전체 문서 diff를 review했다.
- PLAN의 milestone·발견·Final Review를 실제 완료 상태로 갱신하고 이 종료 기록을 추가했다.

### 현재 상태

- 이번 요청 완료: PROGRESS_LOG 생성, AGENTS의 progress logging 규칙, PLAN의 역할·동기화 규칙을 모두 반영했다.
- PLAN의 M1/M2/M3는 완료 상태다. 기존 프로젝트 파일 77개의 SHA-256은 동일하며 변경 범위는 세 루트 Markdown 문서다.

### 발견 / 이슈

- 문서 validation 통과: PLAN 8개 필수 section, workflow 15단계, UTF-8·code fence, 기록별 네 필수 항목, UTC+9 변환·시간순서, 기존 기록 byte prefix 보존, diff·Git whitespace 검사.
- 이번 요청의 계획 방향 변경이나 새로운 blocking 이슈는 없다. 과거 기록의 당시 진행 상태는 그대로 보존한다.
- 기능 변경이 없어 TCAD·GUI·CLI·구조 checker는 이번 요청에서 재실행하지 않았다. 기존 launcher 경로·물리 모델·미구현 spec 한계는 이번 범위 밖으로 남아 있다.

### 다음 작업

- 현재 요청을 완료했으며 다음 요청을 대기한다.
- 다음 non-trivial task에서 PLAN을 새 목표에 맞게 갱신하고, 의미 있는 사건마다 기존 로그를 보존하여 아래에 추가한다.

## 2026-10-04 00:55:04 KST

### 수행한 작업

- 종료 기록 이후 최종 validation의 Git 종료 코드 판정 원인을 조사하고 검증 방법을 보완했다.
- 정상 LF 입력과 trailing-space 입력의 Git 결과를 비교한 뒤 세 문서의 whitespace 검사를 다시 수행했다.

### 현재 상태

- 이번 요청은 완료 상태다. 세 문서의 whitespace 검사와 PLAN·로그 형식·시각·기존 파일 보존 검증이 통과했다.
- PLAN에 원인과 검사 기준을 반영했고, 기존 로그는 수정 없이 보존했다.

### 발견 / 이슈

- 2026-10-04 00:53:34 KST 기록의 validation 결과에 검사 방법을 보완한다. Git `--no-index` 종료 코드 1은 차이를 뜻하며 whitespace 오류가 없을 때도 나온다. 이를 오류로 처리한 검증 스크립트가 원인이었다.
- 재현 결과 정상 입력은 코드 1·진단 없음, trailing-space 입력은 코드 3·오류 진단이었다. 세 문서는 코드 1·진단 없음으로 통과했다.
- 변경 이유는 검증의 잘못된 실패 판정을 바로잡기 위해서다. 구현이나 계획 방향의 변경, 새로운 프로젝트 버그는 없다.

### 다음 작업

- 현재 요청의 최종 validation과 종료 기록을 완료했으며 다음 요청을 대기한다.

## 2026-10-04 01:02:12 KST

### 수행한 작업

- Project 1 Part 1 분석 M1/M2: 과제 PDF와 config·simulator·workflows·구조 checker, 설치된 DEVSIM physics helper를 읽어 대조했다.
- PDF 실제 41/42·50/51쪽의 영문/국문 요구사항과 45~48·54~57쪽의 제출 규칙을 확인했다. 핵심 표·구조도·checker 예시를 렌더 이미지로 검토했다.
- PLAN을 이번 분석 요청에 맞게 갱신하고 기존 source/config/PDF·결과물의 해시 기준과 이전 로그 byte를 확보했다.

### 현재 상태

- M1 원문 요구사항과 M2 구현 격차 조사가 완료되었다. 현재는 작업 순서와 검증 기준을 정리하고 있으며 기능 구현·설계 탐색은 수행하지 않았다.
- Part 1 목표는 같은 소자로 8개 spec을 만족시키고 물리 보완·검증, 탐색 과정, 단일 변수 영향과 최종 구조를 보고하는 것이다.

### 발견 / 이슈

- gate 재료·일함수, 물리 등록 전 구조-only 저장, 8개 spec evaluator가 없다. 온도 입력만으로 n_i/n1/p1의 온도 의존성이 구현되는 것은 아니다.
- PDF는 표면 p+ body tap을 설명하지만 현재는 bulk 아랫면의 이상적 ohmic body 접점이다. Checker 통과가 접점 가정·physics·spec 검증을 대신하지 않는다.
- Mesh 변경이 도핑 감쇠 길이도 바꾸며 조교 physics의 상세 모델·허용 오차는 저장소에 없다.
- 기존 scratch PDF reader의 sandbox 접근 제한은 허용된 로컬 읽기로 해결했다. 프로젝트 환경이나 의존성을 변경하지 않았다.

### 다음 작업

- 의존관계에 따라 제출 구조·physics 검증·measurement·baseline·설계 탐색·최종 검증·보고서 순서를 정리한다.
- 수치·단위·과제 규약을 재검토하고 기존 파일·append-only·문서 상태를 검증한 뒤 분석 완료 기록을 남긴다.

## 2026-10-04 01:05:09 KST

### 수행한 작업

- Project 1 Part 1 분석 M3 완료: 8개 spec·설계 범위·gate 재료·제출 규약을 대조하고 현재 코드의 격차와 향후 9단계 작업 순서·완료 기준을 정리했다.
- PLAN의 요구사항·가정·발견·최종 review를 갱신했다. PDF의 핵심 표·그림 확인 후 이번에 만든 임시 PNG 57개를 제거했다.

### 현재 상태

- 사용자 요청인 Part 1 분석과 순서 정리는 완료했다. 구현·설계 탐색·최종 소자 선정·spec 판정은 수행하지 않았다.
- 변경은 PLAN 갱신과 PROGRESS_LOG append뿐이다. Tracked 파일 66개와 AGENTS의 SHA-256은 동일하며 기존 code/config/PDF/HW1·결과·환경은 그대로다.

### 발견 / 이슈

- 과제는 같은 구조·도핑·gate 재료의 8항목 검증, physics 보완·검증, 시도→지표→판단의 탐색 기록, 단일 변수 영향과 최종 구조를 요구한다.
- 구조 checker 통과와 전기적 합격은 별도다. 저장은 doping 이후·physics 이전이고 gate 재료 이름을 구조에 포함해야 한다.
- Validation 결과: PDF 추출·시각 대조, 원문과 코드/helper/checker 대조, PLAN 8개 section·8개 spec·9단계·UTF-8·diff·Git whitespace·변경 범위·해시·이전 log byte 보존 검증 통과.
- TA physics·추출 세부 방식·허용 오차와 실제 학번은 미확인이다. body tap/ohmic 가정과 mesh-doping 결합도 후속 구현에서 검토해야 한다. 분석 범위에 따라 simulation·checker·parameter 탐색은 실행하지 않았다.

### 다음 작업

- 현재 분석 요청을 완료했으며 다음 요청을 대기한다.
- 후속 구현 요청 시 요구사항/기준 보존→제출 구조→physics 검증→measurement→baseline→설계 탐색→최종 검증→저장 구조 재검증→보고서 순서로 계획을 구체화한다.

## 2026-10-04 01:16:46 KST

### 수행한 작업

- Part 1 순서 1 완료: 현재 소스·설정·로그를 조사하고 1~5번 구현 계획과 검증 기준을 PLAN에 작성했다.
- 코드 변경 전 기존 CLI idvg/idvd/cv를 원본 config로 실행해 project1/results/part1_baseline/legacy에 CSV·config·환경/명령/source hash manifest를 보존했다.

### 현재 상태

- Legacy 검증 통과: Id–Vg 21점, Id–Vd 21점, C–V 31점이며 모든 값이 유한하다.
- 기존 Ion(VG=VD=2 V)은 약 139.625 µA/µm이다. 이는 새 Part 1 모델의 결과표가 아니라 변경 전 비교 기준이다.
- 2~5번 구조·physics·measurement·새 baseline은 구현 전이며 변수 탐색은 진행하지 않는다.

### 발견 / 이슈

- Gate 재료가 없어 기존 intrinsic-reference gate와 가까운 표의 W(4.60 eV)를 baseline에 선택한다. 이는 최적화나 재료 탐색 결과가 아니다.
- 실제 학번이 없으므로 part1_baseline_diagnostic.devsim을 사용한다. 이 파일은 제출용 이름이 아니다.
- Body는 기존 하부 ideal ohmic 배치를 유지하고 PDF의 표면 p+ tap과의 차이를 한계로 기록한다.
- 공식 MOSFET/재료 자료로 기준 전위·DOS·electron affinity를 확인했다. 고온 ni는 300 K 값에 anchor한 모델로 구현하며 상수 이동도·SRH 수명 가정은 유지한다.

### 다음 작업

- Gate 재료 라벨과 physics 이전 구조 export/reload를 구현하고 새 프로세스 구조 checker를 실행한다.
- 이어서 gate·온도 모델과 8항목 추출기를 검증해 새 baseline 결과를 만든다.

## 2026-10-04 01:28:49 KST

### 수행한 작업

- Part 1 순서 2~3 완료: gate_metal/W 라벨, 도핑 직후 구조 export, 저장 재료를 읽는 reload, gate 일함수와 ni(T)/SRH 갱신을 구현했다.
- 도핑 감쇠 길이를 기존 값(12.5/5 nm)으로 유지하면서 mesh 상수에서 분리했다.
- 새 프로세스 checker와 구조 내용 검증, 300/398 K uniform MOS flat-band 검증을 수행했다.

### 현재 상태

- 구조 checker OK. 진단 파일에는 physics equation·Potential/Electrons/Holes·bias가 없고 실제 gate 접점은 oxide에 붙어 있다.
- Gate 라벨 추가 전후 live bulk mesh와 doping은 정확히 같다. 기준 치수·도핑·이동도는 변경하지 않았다.
- ni(300)=1e10, ni(398)=4.7573e12 cm^-3로 n1/p1도 함께 갱신한다. Flat-band 전위의 기대값 오차는 300/398 K에서 약 1.23e-15/5.56e-17 V다.

### 발견 / 이슈

- 구조 재로딩의 엄격한 숫자 비교는 직렬화 roundoff로 실패했다. Live 구조끼리는 0 차이지만 저장/로드 좌표 오차는 최대 5.42e-20 cm이며 doping 오차는 ND의 약 1.22e-14였다. 비트 동일성과 물리 규모를 구분하고 전류 재현성까지 확인하기로 했다.
- W 기준 gate offset은 300 K에서 약 -0.01312 V다. 큰 body Fermi offset을 중복해서 더하지 않도록 flat-band로 검증했다.
- 기존 CSV·config·HW1·설치 package는 보존한다. 보고 수치는 로컬 Boltzmann/ideal-ohmic/SRH 모델에 대한 것이며 조교 모델 일치나 최종 합격을 보장하지 않는다.

### 다음 작업

- 8항목 추출기와 독립 기대 곡선·edge-case·native model test를 실행한다.
- 동일한 저장 구조에서 baseline을 측정하고 전압 간격·정밀도에 따른 재현성과 전류 보존을 확인한다.

## 2026-10-04 01:33:51 KST

### 수행한 작업

- **4번 완료 — 8개 spec 측정과 판정 구현.** Vth·Ion·Ioff·SS·398 K Ioff·DIBL·body effect·Eox를 조건별로 측정하고 PASS/FAIL/ERROR를 구분한다.
- 정전류 지점은 log10(ID)에서 보간하고, Ion/Ioff는 실제 지정 전압점에서 읽는다. 데이터가 부족하면 외삽하거나 0으로 바꾸지 않고 ERROR로 남긴다.
- 독립적으로 만든 기대 곡선, 단위 변환, 잘못된 입력, 물리 모델과 구조 파일의 test를 실행했다.

### 현재 상태

- `.conda\python.exe -B -m unittest discover -s project1/tests -v`: **13개 test 통과**.
- **1~4번 완료, 5번 초기 소자 결과 계산 중.** 동일한 소자를 20 mV와 10 mV 측정 간격으로 계산 중이며 설계값 탐색은 시작하지 않았다.
- 원본 config와 HW1은 유지했고 이동도·ramp·solver 허용 오차를 바꾸지 않았다.

### 발견 / 이슈

- 첫 test 실행의 파일 정리 실패를 조사했다. DEVSIM 2.10의 Windows loader는 파일을 로드하면 device/mesh 삭제 후에도 프로세스 종료까지 파일을 열어둔다.
- write/로드/clear 단계별 rename 실험으로 원인을 확인했다. 구조 test를 별도 프로세스로 분리해 종료 후 안전하게 정리하도록 수정했고 전체 test가 통과했다.
- 이번 수치 검증은 측정 간격·정밀도·저장/재로딩의 안정성을 확인한다. Mesh 수렴과 조교 채점 모델 일치는 별도 확인 사항이다.

### 다음 작업

- 5번의 초기 소자 8개 결과를 완성하고, 전류 보존·정밀도·측정 간격 검증 및 기존 CLI 회귀 비교를 진행한다.
- 결과표에서 미충족 항목과 모델 한계를 쉽게 설명하고 최종 review 후 기록한다. **6번 변수 조합 탐색은 사용자 확인 후 별도 요청에서 진행한다.**

## 2026-10-04 01:40:16 KST

### 수행한 작업

- **5번 초기 소자 측정 완료 — 수치 안정성 검증은 진행 중.** 20 mV 간격의 세 Id–Vg 곡선과 398 K off-current로 8개 spec을 모두 측정했다.
- 기존 CLI 3종의 변경 전/후 결과를 비교하고, 최종 코드 검토에서 발견한 extractor edge case를 재현·수정했다.

### 현재 상태

- 로컬 모델에서 **6개 PASS, 2개 FAIL, 측정 ERROR 0개**다.
- Vth **0.550307 V**는 0.40~0.50 V 범위를 벗어난다. Ion **142.052640 µA/µm**는 목표 450 µA/µm의 약 **31.6%**다.
- Ioff·SS·398 K Ioff·DIBL·body effect·Eox는 기준을 충족한다. 전체 표는 검증을 마친 최종 기록에 정리한다.
- `project1/results/part1_baseline/primary/metrics.json`과 raw CSV를 보존했다. 10 mV 비교 실행은 진행 중이다.

### 발견 / 이슈

- Legacy의 VG=0에서 아주 엄격한 비교가 실패했다(차이 2.25e-23 A/µm). 원본 코드도 같은 환경에서 재실행하면 작은 차이가 났으며, 원본/새 코드의 mesh·doping 배열은 정확히 같았다.
- 사전에 정한 절대 전류 검증 기준 1e-17 A/µm를 함께 적용해 I–V 21/21점 회귀가 통과했다. 전압점과 C–V 31점은 정확히 동일하다. 근거는 `legacy_regression.json`에 남겼다.
- 목표 전류와 정확히 같은 sample이 있는 하강 곡선이나 접점 곡선도 Vth로 읽을 수 있는 bug를 발견했다. 3개 실패 사례로 재현한 뒤 상승 crossing만 허용하도록 수정했고 **13개 test가 다시 통과**했다.
- 기준 실행의 source hash는 실제 당시 버전으로 보존한다. 최종 extractor로 같은 CSV를 다시 평가해 동일 결과인지 별도로 검증한다.

### 다음 작업

- 10 mV 결과와 비교하고 주요 off/on/문턱 부근 전류의 정밀도·재로딩 재현성을 확인한다.
- 전체 diff·원본 파일 보호·문서/로그 일치를 최종 검토하고 결과표·한계를 정리한다. 설계 변수 조합 탐색은 하지 않는다.

## 2026-10-04 01:52:52 KST

### 수행한 작업

- 같은 초기 소자를 10 mV 간격으로 다시 측정했다. 20 mV 결과와 **8개 판정이 모두 같다**.
- 최종 review에서 입력/source 기록 시점을 수정하고, 계산 중 파일을 편집하는 회귀 test를 추가했다.
- 추가 정밀도 검증의 수렴 실패를 조사하고 replay 방법을 새 프로세스 방식으로 변경했다.

### 현재 상태

- Vth 차이 **0.352 mV**, SS 차이 **0.036 mV/dec**, DIBL 차이 **0.132 mV/V**, body effect 차이 **0.072 mV**로 사전에 정한 측정 간격 검증 범위 안이다.
- Ion·300/398 K Ioff·Eox는 두 간격에서 같은 값이다. 기능/모델/추출/기록 보존 test **14개 통과**.
- 초기 소자의 미충족 항목은 계속 Vth와 Ion이다. 새 프로세스별 정밀도·live/reload 전류 비교는 진행 중이다.

### 발견 / 이슈

- 같은 프로세스에서 extended→double로 전환한 최초 비교가 수렴 실패로 중단됐다. 새 프로세스 double 저전압 off 진단은 수렴했지만 전류 보존 잔차가 약 **1.01% (1.90e-17 A/µm)**였다.
- 프로세스 상태와 정밀도 전환 영향을 섞지 않도록 각 측정점·정밀도를 독립 Python 프로세스로 비교한다. 이동도·ramp·solver 허용 오차는 그대로다. Double 결과의 실패나 부정확성을 PASS로 덮지 않는다.
- 앞선 기록의 source hash 보존 설명을 보완한다. 초기 실행 코드는 source/config를 계산 종료 시 다시 읽었다. Fine 계산 중 extractor를 수정했으므로 fine JSON의 extractor hash는 시작 때 로드한 코드와 다르다. 원본 결과를 덮어쓰지 않고 `provenance_review.json`에서 이 차이를 설명한다.
- 향후 CLI는 긴 계산 전에 source hash와 실제 읽은 config text를 확보한다. 수정 중 disk 입력이 바뀌는 경우의 test가 통과했다. 실제 물리 방정식은 이 기록 개선으로 바뀌지 않았다.

### 다음 작업

- 독립 프로세스의 전류 replay를 완료해 extended 기준 결과의 검증 상태와 double 비교 한계를 확정한다.
- 8개 결과표·검증·모델 한계를 최종 로그에 정리하고 PLAN을 완료 상태로 맞춘다. **6번 설계 변수 탐색은 사용자 확인 전까지 수행하지 않는다.**

## 2026-10-04 02:02:40 KST

### 수행한 작업

- **이번 요청 최종 완료 — 앞서 정리한 1~5번까지 진행했다.**
- 기존 CLI 결과를 보존하고, Part 1 필수 구조·gate 재료·physics 이전 저장/재로딩을 구현했다.
- Gate 일함수, 300/398 K intrinsic carrier·SRH 갱신 및 body bias 조건을 적용하고, 8개 spec의 측정·판정·오류 처리를 구현했다.
- 초기 소자를 20/10 mV 간격으로 측정하고 코드 검토·문제 수정·최종 검증을 마쳤다. **6번 설계 변수/조합 탐색은 실행하지 않았다.**
- `PLAN.md`를 실제 최종 상태로 갱신했고, `AGENTS.md`에 새 실행/검증 경로와 결과 해석 규칙을 반영했다.

### 현재 상태

**기준 소자:** W(4.60 eV), Lg=1.0 µm, source/drain 각각 0.5 µm, tox=10 nm, tSi=0.5 µm, xj=0.1 µm, NA=1e16/ND=1e19 cm^-3. 기존 이동도 400/200과 도핑 감쇠 길이 12.5/5 nm를 유지했다.

**결과: 로컬 extended 모델에서 6개 충족, 2개 미충족, 측정 ERROR 0개.** 아래는 20 mV 기준이며 10 mV에서도 판정이 같다. 기본 T=300 K, VS=VB=0이며 body/고온 항목만 해당 조건을 바꾼다.

| 항목 | 초기 소자 결과 | 과제 기준 | 판정 |
|---|---:|---:|---|
| Vth (VD=0.05 V) | **0.5503 V** | 0.40~0.50 V | **미충족** |
| Ion (VG=VD=2 V) | **142.05 µA/µm** | ≥450 µA/µm | **미충족** |
| Ioff (VG=0, VD=2 V) | 0.003296 pA/µm | ≤1 pA/µm | 충족 |
| SS (VD=0.05 V, 1e-10~1e-8 A/µm 평균) | 69.04 mV/dec | ≤75 mV/dec | 충족 |
| Ioff (398 K, VG=0, VD=2 V) | 34.43 pA/µm | ≤100 pA/µm | 충족 |
| DIBL (VD=0.05/2 V) | 13.43 mV/V | ≤30 mV/V | 충족 |
| Body effect (VB=−0.5 V, VD=0.05 V) | 0.04210 V | ≤0.08 V | 충족 |
| Eox (2 V/tox) | 2.00 MV/cm | ≤5 MV/cm | 충족 |

**읽는 방법**

- Vth는 상한보다 약 **50.3 mV 높다**. Ion은 목표의 약 **31.6%**이며 약 307.95 µA/µm 부족하다. 다음 설계 탐색에서는 이 두 항목을 개선하면서 현재 충족한 항목도 유지해야 한다.
- 기존 HW1 `SimpleMosfet`을 읽기 전용으로 이용한 square-law 근사도 약 **145.07 µA/µm**로 현재 전류 규모와 가깝다. 측정 Vth를 입력으로 쓴 근사이며 독립 Vth 검증이나 실제 소자 정확성 보장은 아니다.
- Spec 미충족은 초기 설계의 결과다. 통과시키기 위해 치수·도핑·재료를 탐색하거나 이동도·solver 오차·ramp를 조정하지 않았다.

**검증 결과**

- `.conda\python.exe -B -m unittest discover -s project1/tests -v`: **14개 test 통과**.
- 구조 checker **OK**, 하나의 device 및 구조/도핑만 저장됨을 확인했다. Gate 전위의 부호·크기와 300/398 K 균일 MOS flat-band도 검증했다.
- 기존 Id–Vg/Id–Vd/C–V **21/21/31점 회귀 통과**. 전압 열과 C–V 값은 정확히 같으며 I–V 차이는 기록한 수치 허용 범위 안이다.
- 같은 구조의 **101/201점 비교 통과**. Vth 차이 0.352 mV, SS 0.036 mV/dec, DIBL 0.132 mV/V, body effect 0.072 mV로 정한 범위 안이다. Ion·두 온도의 Ioff·Eox는 같다.
- **Extended의 live/reload replay 10개 모두 통과**. 기준 전류와 최대 차이 약 7.70e-18 A/µm, 기준/미세 sweep의 전류 보존 최대 상대 잔차 약 3.87e-16이다.
- 최종 extractor로 두 raw dataset을 재평가해 원래 8개 결과와 일치함을 확인했다.
- 원본 config/CSV/PDF·HW1 등 보호 대상 **63개 tracked 파일의 해시가 그대로**다. 기존 로그 byte도 전부 보존했다.

**산출물**

- 기준 결과/CSV: [primary](project1/results/part1_baseline/primary/metrics.json)
- 10 mV 비교: [fine](project1/results/part1_baseline/fine/metrics.json)
- 수치 검증과 실패 기록: [numerical_validation.json](project1/results/part1_baseline/numerical_validation.json)
- 기존 CLI 회귀/출처 보완: [legacy_regression.json](project1/results/part1_baseline/legacy_regression.json), [provenance_review.json](project1/results/part1_baseline/provenance_review.json)
- 모델 식·계수·근거·실행 방법·한계: [PART1_BASELINE.md](project1/PART1_BASELINE.md)

### 발견 / 이슈

- **Double 전체 비교는 미완료다.** 저전압 문턱 부근·body bias 2점은 비교를 완료했지만 고전압 off/on·398 K off 3점은 초기 drain ramp 중 실패했다. 300 K에서는 VD=1.7 V, 398 K에서는 VD=1.3 V이며 target gate를 설정하기 전이었다.
- 이전에 조사한 정밀도 전환/프로세스 상태의 영향 가능성과 구분해, 독립 프로세스에서도 같은 고전압 실패를 재현했다. 따라서 한 프로세스에서 정밀도를 전환할 때만 생기는 문제로 해석하지 않는다.
- 300 K double에서 전자 방정식 상대 오차가 약 1.90e-3에 정체되고 Potential 오차는 약 1e-13였다. 같은 물리/solver 설정의 extended가 수렴한 비교는 수치 정밀도 한계를 뒷받침한다. 내부 어느 연산에서 발생하는지까지 완전히 특정한 것은 아니다.
- `extended_baseline_checks_pass=true`, `double_precision_complete=false`, `all_checks_pass=false`를 그대로 보존했다. 검증 CLI의 exit 1은 double 비교 실패를 반영하며 **전체 검증이 모두 통과했다고 주장하지 않는다.**
- Review에서 exact target의 잘못된 crossing 허용 및 계산 중 편집에 취약한 source/config 기록을 수정했다. Fine source hash의 시점 차이는 원본을 덮어쓰지 않고 출처 보완 파일에 설명했으며, 최종 코드로 raw 결과를 다시 평가했다.
- **남은 모델 한계:** 하단 ideal ohmic body 접점을 유지한다. PDF의 표면 p+ tap과 다르며 mesh 수렴·고농도/고전계 추가 물리·조교 모델 일치·실험 정확성은 별도 확인이 필요하다. 현재 값은 로컬 모델 결과이며 실제 채점 통과를 보장하지 않는다.
- `part1_baseline_diagnostic.devsim`은 학번을 넣은 최종 제출 파일이 아니다. 환경/설치 package·HW1 및 원래 결과는 수정하지 않았다.

### 다음 작업

- **현재 요청의 1~5번은 완료했다. 사용자가 결과를 확인하는 단계다.**
- 사용자의 확인과 별도 진행 요청 이후 **6번: 변수를 하나씩 바꾼 뒤 조합 탐색**을 시작한다. 아직 후보 설계나 변수 sweep은 만들지 않았다.
