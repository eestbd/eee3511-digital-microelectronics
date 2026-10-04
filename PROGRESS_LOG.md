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

## 2026-10-04 12:59:07 KST

### ??? ??

- Step 6?7?8 ?? M1: ?? evaluator?validator??? ???baseline??? ??? ???? PLAN? ? ???? ????.
- ??? ??? ?? ?? ??? **?? 10??30?**, ?? ?? ??? ?? 2?? ????. ?? 30??? ???? ???.

### ?? ??

- ?? TCAD ?? ??? ???? ???. ?? 104? tracked ??? log byte? ??? ?? snapshot? ????.
- ???????? ??? ?? wrapper? ?? ?? edge case ???? ????. ?? physics/CLI/solver? baseline? ????.

### ?? / ??

- 30?? ? ???? ?? ??? ??? wall-clock ????, ? child?? ?? ??? timeout?? ????. ??? 10?? ????.
- ?? ??? final validation? ???? ??? ??? ????? ???? ?? ???? ???. ??? ?? ???? ?????.
- Single 4? ? ?? ?? ??/?? ??? ????, double ??? ??? ???? ??? ????.

### ?? ??

- ?? 14?+? 4? test? ???? ?? ?? 4?? ???? ????.

## 2026-10-04 13:04:44 KST

### ??? ??

- Step 6 ?? ?? ? ??: gate ??? 1.0?0.5 ?m? ?? 8? ??? ?? ????.
- ?? 14?? ? ????? ???timeout ?? 5?, **? 19? unittest ??**.

### ?? ??

- ?? **1/10? ??**, ?? 279.6?. ?? tox? 10?5 nm? ??? 2??? ?? ???.
- Lg=0.5 ??: Vth 0.4869 V(PASS), Ion 333.49 ?A/?m(FAIL), Ioff 0.6850 pA/?m(PASS), SS 72.67 mV/dec(PASS), ?? Ioff 482.34 pA/?m(FAIL), DIBL 40.92 mV/V(FAIL), body 0.03291 V(PASS), Eox 2 MV/cm(PASS).

### ?? / ??

- ??? ??? Vth?Ion? ????? ?? ??? DIBL? ???? **5 PASS/3 FAIL**??. ?? ?????? ????? ???? ???.
- ??? ? raw CSV? ?? ?? ?? ??? ?? ????. ?? baseline? physics/solver ??? ???? ???.
- ?? CLI? ?? ???/?? purpose ??? ?? baseline? ??? ?????. ?? ??? ?? ??? trial.json/input.yaml? ??? ????. ?? ?? ??? ???.

### ?? ??

- ??? ????? ???gate ?? ??? ?? ?? ??? ???? ?? ??? ?? ??? ????.

## 2026-10-04 13:11:35 KST

### ??? ??

- Step 6 ?? ?? #2: tox? 10?5 nm? ?? ??? 8? ?? ?? ??.
- ?? ??? ?? ?? ?? ??? ??? **4??3?**? ????. Gate ??? ?? ?? ???? ????.

### ?? ??

- **2/10? ??**, ?? #3 NA=3e15? ?? ???. #2 ?? 373.2?.
- tox=5 ??: Vth 0.47794 V(PASS), Ion 292.91 ?A/?m(FAIL), Ioff 0.010663 pA/?m(PASS), SS 65.31 mV/dec(PASS), ?? Ioff 40.12 pA/?m(PASS), DIBL 9.42 mV/V(PASS), body 0.02373 V(PASS), Eox 4 MV/cm(PASS). **7 PASS/1 FAIL**.

### ?? / ??

- ??? ??? Ion? ? 2.06?? ???? DIBL?SS?body effect? ????. Lg ?? ??? ??? ??? ?? ??? ???. ? ?? ??? ?? ??? ????? ???? ???.
- ? ? ??? 4.7/6.2???? ?? single 4? ??? ??/?? ?? ??? ???? ?? ? ??. ??? gate ?? ??? ???? ?? 30? ??? ????. 10??30? ??? ??? ???.
- #2 ? raw CSV? ?????? ?? ?? ?? ??.

### ?? ??

- NA ?? ?? ??? ??? ? Lg=0.5/tox=5? ?? ????, ?? ??? ??? ?? ?? ?? ?? ????.

## 2026-10-04 13:13:29 KST

### ??? ??

- Step 6 ?? ??: ???? ?? ??? ??? **?? ?? ?? ? 10? ??**, ?? ?? ?? 2? ???? ????.
- PLAN?session budget? ???? wrapper? ?? ?? None ??? ?? ?? ?? test? ????.

### ?? ??

- #1 Lg=0.5, #2 tox=5 ??. #3 NA=3e15 ?? ???. ?? 30? ??? ? ?? ?? ??? ???.
- ?? ?? ?? #3? ?? timeout ? 1098?? ????? ?? ?? ???? ??? ??. ?? ????? timeout=None??.

### ?? / ??

- ?? ??? ?? ? ??? ? 5~6? ?? 30? ?? ?? ??? ??? ???? ???? ??? ????. ??? ?? 10?? ??? ?? ??? ? 10?? ????.
- 30? ??? 4?3?? ?? single ??? ???? ??/??? ?? ??? ??. ?? ??? ?? ?? ?? ??? ???? ???.

### ?? ??

- ? ?? ?? test? ???? NA ???gate ?? ?? ?? ?? ? ?? ??? ????.

## 2026-10-04 13:18:06 KST

### ??? ??

- Step 6 ?? ?? #3: NA? 1e16?3e15 cm^-3? ?? ?? ?? ??.
- ?? ?? None? 10? ?? ?? ???? **20? unittest ??**.

### ?? ??

- **3/10? ??**, #4 gate? W?TaN?? ??? ??? ?? ?? ?? ?? ???. #3 ?? 366.1?.
- #3: Vth 0.46989 V, Ion 156.77 ?A/?m, Ioff 0.05702 pA/?m, SS 68.57 mV/dec, ?? Ioff 225.83 pA/?m, DIBL 17.36 mV/V, body 0.03457 V, Eox 2 MV/cm. Ion/?? ??? FAIL? **6 PASS/2 FAIL**.

### ?? / ??

- ?? ??? Vth/body effect? ????? Ion ??? ? 10%? ??? ?? ??? baseline? ? 6.6?? ????. ?? ??? ?? NA=1e16? ????.
- #3 ? raw CSV? ?????? ?? ??. ?? ? #4? ?? ?? ?? ???? ??/???? ????.

### ?? ??

- #4 ?? ? single 4?? ???? Lg/tox ??? ??? gate ??? ?? ????.

## 2026-10-04 13:24:50 KST

### ??? ??

- M2 / step 6a ??: baseline?? ? ??? ?? 4? ??? ?? ???? ????.
- #4 Gate TaN ???? ???? #5 Lg=0.5/tox=5/W ??? ????.

### ?? ??

- **4/10? ??, #5 ?? ?? ?**. ?? ??? ?? ???? ?? ?? ??? ?? ???? ???.

| ?? | ?? ?? | Vth(V) | Ion(?A/?m) | ?? Ioff(pA/?m) | DIBL(mV/V) | ?? | ??? |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | gate_length_um=0.5 | 0.486906 | 333.49 | 482.34 | 40.92 | 5/8 | Ion, Ioff_398K, DIBL |
| 2 | oxide_thickness_nm=5.0 | 0.477942 | 292.91 | 40.12 | 9.42 | 7/8 | Ion |
| 3 | body_doping_cm3=3000000000000000.0 | 0.469888 | 156.77 | 225.83 | 17.36 | 6/8 | Ion, Ioff_398K |
| 4 | gate_material=TaN | 0.399957 | 171.10 | 225.86 | 13.24 | 5/8 | Vth, Ion, Ioff_398K |

### ?? / ??

- Lg ??? Ion? ?? ???? DIBL??? ??? ????. tox ??? Ion? ???? SS/DIBL/body ??? ???? ?? ??? ????. ? ??? ?? ?? ??? ????.
- NA ??? ?? ??? TaN? ?? ??? ??? ???. #5??? baseline NA=1e16?W? ????.
- TaN Vth? 0.399957 V? **???? ? 43 ?V ?? FAIL**??. 0.400?? ???? ?? ???? ???. ?? ???? ?? ?? ??? ??? ?? ????.
- Single 4? ?? ?? ERROR ???? raw CSV? ???/?? ?? ??. ??/solver/???/?? ??? ???? ???.
- ?? ??? baseline?? ???? ??? part1.py? ??/purpose ? ???? ?? ?? ???? ???. --help ???? ?? ??? ??. ?? ??? source hash? ???? ???.

### ?? ??

- #5? 8? ??? ???? gate/?? ??? ?? ?? ?? ?? 6? ??? ????.

## 2026-10-04 13:31:43 KST

### ??? ??

- Step 6 ?? #5: Lg=0.5 ?m/tox=5 nm/W, ??? baseline ???? 8??? ????.
- ?? ??? ??? ??? ???? #6? ?? ??/???? gate? TiN?? ?? ????.

### ?? ??

- **5/10? ??, #6 ?? ?**. ?? 8? ?? ??? ??? ??. #5 ?? 330.8?.
- #5: Vth 0.43212 V, Ion 641.84 ?A/?m, Ioff 0.54998 pA/?m, SS 67.69 mV/dec, ?? Ioff **397.19 pA/?m(FAIL)**, DIBL 26.34 mV/V, body 0.01937 V, Eox 4 MV/cm. **7 PASS/1 FAIL**.

### ?? / ??

- ?? ????? Vth/Ion? ????? ?? ??? ? bottleneck??. 300 K ????? ??? ?? ???? ???.
- TiN? W?? ???? 0.05 eV ?? ??? gate ????? ??? ??? ????. ?? ???? ?? ??/??/??? ??? ?? ??? ????.
- #5 raw ? CSV ???/?? ?? ?? ??. ?? 30?? ?? ???? ?? ?? ?? ?? ?? ??? ?? ??? ? 10? ??? ????.

### ?? ??

- #6 ??? ?? gate ??/??/??? ????, ??? ? ?? ?? ?? ??? ????.

## 2026-10-04 13:39:39 KST

### ??? ??

- Step 6 ?? #6: #5? ?? ??/???? gate W?TiN??? ?? 8?? ?? ??.
- #7 Lg=0.6 ?m/tox=4.5 nm/TiN/NA=1e16 ??? ????.

### ?? ??

- **6/10? ??, #7 ?? ?**. #6 ?? 298.7?.
- #6: Vth 0.48203 V, Ion 604.31 ?A/?m, Ioff 0.12864 pA/?m, SS 67.70 mV/dec, ?? Ioff **169.24 pA/?m(FAIL)**, DIBL 26.25 mV/V, body 0.01935 V, Eox 4 MV/cm. **7 PASS/1 FAIL**.

### ?? / ??

- TiN? ??? ? 50 mV ??? 300 K ??? ? 76.6%, ?? ??? ? 57.4% ???. Ion? ? 5.8% ????? ??? ???. Gate ??????? ?? ??? ??? ???? ???.
- DIBL? ?? ???? ???? gate ??? ??? ?? ???. Lg? ?? ??? ???? tox? 4.5? ?? Vth ??/Ion? ???? ?? #7? ?? ???.
- #6 ? raw CSV ???/?? ?? ?? ??. ?? ??/solver/???/?? ?? ??.

### ?? ??

- #7 ??? ?? ??? ?? #8? ?? #9?#10? ???? ?? ?? ???? ????.

## 2026-10-04 13:43:41 KST

### ??? ??

- Step 6 ?? #7 ?? ??. **???? 8? spec? ?? ??? ??? ????.**
- #8? Lg=0.6/tox=4.5? ???? gate W?NA=2e16? ?? ??? ????.

### ?? ??

- **7/10? ??**, #8 ?? ?. #7 ?? 299.1?. ?? ??? ?? ???? ???.
- #7 ??: Lg=0.6 ?m, tox=4.5 nm, TiN(4.65 eV), NA=1e16, ? ? baseline ??.

| ?? | #7 ?? | ?? | ?? |
|---|---:|---:|---|
| Vth | 0.490584 V | 0.40~0.50 V | PASS |
| Ion | 538.51 ?A/?m | ?450 | PASS |
| Ioff | 0.017475 pA/?m | ?1 | PASS |
| SS | 66.08 mV/dec | ?75 | PASS |
| 398 K Ioff | 53.69 pA/?m | ?100 | PASS |
| DIBL | 17.63 mV/V | ?30 | PASS |
| Body effect | 0.019260 V | ?0.08 | PASS |
| Eox | 4.44444 MV/cm | ?5 | PASS |

### ?? / ??

- #6?? ??? ??? ???? ?? ??? ?? ??? DIBL? ???? Ion? ?? ???? ????.
- Vth ?? ??? ? 9.4 mV? ?? ?? ??? 10 mV/fresh replay ??? ????. ?? PASS? ?? extended/20 mV ??? spec ???? ?? ??/?? ??? ??? ???.
- #7 ? raw CSV ???/?? ??? ?? checker ??. ?? baseline?????solver??? ??? ????.
- #8 ?? NA/W ??? ?? NA? ?? ??? ???? ??? ?? ?? ????. ??? ???? ?? ?? ???? ????? ???.

### ?? ??

- #8 ??? ???? ??? #9?#10? ?? ?? ??? ????. ?? ?? ?? ?? 2?? ????.

## 2026-10-04 13:49:28 KST

### ??? ??

- M3a / step 6b ?? ?? ??: #5~#8? ???? #7?#8 ? ?? 8 PASS ??? ????.
- #8? ?? Lg/tox?? W+NA=2e16 ?? ??? ????, #9 ?? ??? ????.

### ?? ??

- **8/10? ??, #9 ?? ?**. ?? ??? #9?#10 ? ???. #8 ?? 290.6?.
- #8: Vth 0.479354 V, Ion 544.83 ?A/?m, Ioff 0.014048 pA/?m, SS 65.99 mV/dec, ?? Ioff 21.55 pA/?m, DIBL 12.64 mV/V, body 0.025630 V, Eox 4.44444 MV/cm. **8? ?? PASS**.

### ?? / ??

- #8? #7(TiN/NA=1e16)?? Vth ?? ??? ?? ?? ??/DIBL? ??. Body effect? 0.01926?0.02563 V? ???? 0.08 V ?? ???. Gate? NA? ?? ?? ????? ?? ??? ? ??? ??? ???? ???.
- #8 ?? checker? ? raw CSV? ???/?? ?? ??. ?? PASS? 20 mV/extended ???? final fine/precision/reload ?? ???.
- #9? #7?? Lg? 0.6?0.55? ?? ??/?? ??? ?? ?? ??? ???? ?? ????.

### ?? ??

- #9?#10 ?? ? spec? ??? ?? ??? ?? ?? ?? 2?? ???? step 7?8? ????.

## 2026-10-04 13:57:10 KST

### ??? ??

- Step 6c ?? #9 ??: #7? Lg? 0.6?0.55 ?m? ?? 8??? ????.
- ??? #10? #8? tox? 4.5?4.75 nm? ?? ?? ???.

### ?? ??

- **9/10? ??, #10 ?? ?**. #7?#8?#9 ? ??? 8 PASS?. #9 ?? 291.4?.
- #9: Vth 0.484180 V, Ion 595.17 ?A/?m, Ioff 0.037661 pA/?m, SS 66.55 mV/dec, ?? Ioff 78.45 pA/?m, DIBL 20.62 mV/V, body 0.018631 V, Eox 4.44444 MV/cm. **8 PASS**.

### ?? / ??

- #7 ?? Ion? ? 10.5% ???? Vth ?? ??? ????, ?? ??? 53.69?78.45, DIBL? 17.63?20.62? ????. ?? Ion??? ??? ??? ???.
- #9 ?? checker/? CSV ?????? ?? ??. #10? ??? oxide? Eox? ??? ???? ?? Ion/??/??? ???? ????.
- ?? ??? PLAN? ?????: 8 PASS+?? ?? ??? ?? ??? spec ??? ???? ???? ?? ??? ????. ?? ?? ?? ???? ?? ??? ???? ???.

### ?? ??

- #10 ?? ? ? 10? ??? ?? ?? ?? 2?? ????. ?? ??? fine/precision/reload ??? ??? ????.

## 2026-10-04 14:03:00 KST

### ??? ??

- **Step 6 ??: ?? ?? 4? ? ?? 4? ? ?? ?? 2?, ? 10?? ???? ??? ????.**
- #10? tox 4.75 nm ???? ????, ?? ?? **#10?#8** ? ?? ????.
- Step 7? ?? ?? 10 mV ???? ?? Python ????? ????. ? ?? ??? ???? ???.

### ?? ??

- 10? ?? 8?? ?? ??(ERROR 0), ?? checker/? raw CSV ?????? ?? ??. **4? ??(#7?#8?#9?#10)? 8? spec? ????.**
- PDE ?? ?? ?? **53.06?**, ? ?????? ?? wall-clock **59.79?**??. ??? ???? ?? ??? ??? ? ???? ? 10?? ???.

| ?? | ?? | Lg(?m) | tox(nm) | NA(cm^-3) | Gate | Vth(V) | Ion(?A/?m) | 398 K Ioff(pA/?m) | ?? | ??? |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---|
| 1 | ?? ?? | 0.5 | 10 | 1.0e+16 | W | 0.486906 | 333.49 | 482.34 | 5/8 | Ion, Ioff_398K, DIBL |
| 2 | ?? ?? | 1 | 5 | 1.0e+16 | W | 0.477942 | 292.91 | 40.12 | 7/8 | Ion |
| 3 | ?? ?? | 1 | 10 | 3.0e+15 | W | 0.469888 | 156.77 | 225.83 | 6/8 | Ion, Ioff_398K |
| 4 | ?? ?? | 1 | 10 | 1.0e+16 | TaN | 0.399957 | 171.10 | 225.86 | 5/8 | Vth, Ion, Ioff_398K |
| 5 | ?? | 0.5 | 5 | 1.0e+16 | W | 0.432120 | 641.84 | 397.19 | 7/8 | Ioff_398K |
| 6 | ?? | 0.5 | 5 | 1.0e+16 | TiN | 0.482026 | 604.31 | 169.24 | 7/8 | Ioff_398K |
| 7 | ?? | 0.6 | 4.5 | 1.0e+16 | TiN | 0.490584 | 538.51 | 53.69 | 8/8 | ?? |
| 8 | ?? | 0.6 | 4.5 | 2.0e+16 | W | 0.479354 | 544.83 | 21.55 | 8/8 | ?? |
| 9 | ?? | 0.55 | 4.5 | 1.0e+16 | TiN | 0.484180 | 595.17 | 78.45 | 8/8 | ?? |
| 10 | ?? | 0.6 | 4.75 | 2.0e+16 | W | 0.484072 | 516.70 | 20.86 | 8/8 | ?? |

- ?? ?? #10: W, Lg=0.6 ?m, tox=4.75 nm, NA=2e16. Vth 0.484072 V, Ion 516.70 ?A/?m, ?? Ioff 20.86 pA/?m, Eox 4.21053 MV/cm.
- ?? ?? #8: W, Lg=0.6 ?m, tox=4.5 nm, NA=2e16. Vth 0.479354 V, Ion 544.83 ?A/?m, ?? Ioff 21.55 pA/?m, Eox 4.44444 MV/cm.
- ? ??? ? ? ?? source/drain ? 0.5 ?m, tSi=0.5 ?m, xj=0.1 ?m, ND=1e19, mu=400/200, ?? 12.5/5 nm? baseline? ??.

### ?? / ??

- #10? tox? ?? ?? Eox ??? ??? Ion? 516.70?? ??? ????. ?? ?? ??? spec ??? #10=0.116927, #8=0.111111??. ?? ???? #9?? #8? ?? ??? ? 2??? ???. Threshold/?? ??? ??? ?? ???.
- ?? Ion? ?? #9? ??? ?? ?? ??? ??. #7? Vth ??? ? ???. ?? ??? ??? ??? ?? ? ??? ????.
- ?? 8 PASS? 20 mV/extended? ?? ????. Fine?precision?fresh reload ??? ?? ??? ?? ??/?? ???? ???? ???.

### ?? ??

- ? ??? 10 mV ?? ?? ? numerical validation? ?? ?? ???? ????. ?? ??? ???? ?? ??? ????.

## 2026-10-04 14:11:54 KST

### 수행한 작업

- **Step 6 완료 내용 정정 및 검증 중간 기록.** 이번 작업의 12:59:07~14:03:00 KST 기록에 PowerShell stdin 인코딩으로 한국어가 `?`로 저장된 문제가 발견됐다. 해당 기록의 본문·표제를 수정하지 않고, 확인된 입력·trial JSON·raw CSV·session·test 로그를 근거로 아래에 다시 정리한다. 원래 수행 시각을 새로 만들지 않는다.
- `PLAN.md`를 정상 UTF-8로 갱신했다. 이후 한국어 문서는 apply_patch로 UTF-8 파일을 만들고 기존 로그 아래에 byte 그대로 추가한다.
- C–V strict 비교 실패를 원본 코드 재실행으로 조사하고 `project1/results/part1_search_20261004/legacy_regression_review.json`에 결과를 보존했다.

### 현재 상태

- 최초 승인 단계는 단일 변수 → 유망 조합 → 후보 주변 탐색이다. 13:13:29 KST 사용자 지시로 **시간 제한을 해제했고, 전체 횟수는 총 10회로 유지**했다. 후보 검증은 최대 2개이며 신규 설계 탐색과 구분한다.
- 단일 변수 4회·조합 4회·주변 2회, **총 10회 완료, ERROR 0**. 모든 trial의 8개 측정·구조 checker·raw CSV 전류 보존을 확인했다. PDE 실행 합계 53.06분, 첫 시작부터 마지막 종료까지 59.79분이다.

| 번호 | 단계 | Lg (µm) | tox (nm) | NA (cm⁻³) | Gate | Vth (V) | Ion (µA/µm) | 398 K Ioff (pA/µm) | 충족 | 미충족 |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---|
| 1 | 단일 변수 | 0.5 | 10 | 1e16 | W | 0.486906 | 333.49 | 482.34 | 5/8 | Ion, 고온 Ioff, DIBL |
| 2 | 단일 변수 | 1 | 5 | 1e16 | W | 0.477942 | 292.91 | 40.12 | 7/8 | Ion |
| 3 | 단일 변수 | 1 | 10 | 3e15 | W | 0.469888 | 156.77 | 225.83 | 6/8 | Ion, 고온 Ioff |
| 4 | 단일 변수 | 1 | 10 | 1e16 | TaN | 0.399957 | 171.10 | 225.86 | 5/8 | Vth, Ion, 고온 Ioff |
| 5 | 조합 | 0.5 | 5 | 1e16 | W | 0.432120 | 641.84 | 397.19 | 7/8 | 고온 Ioff |
| 6 | 조합 | 0.5 | 5 | 1e16 | TiN | 0.482026 | 604.31 | 169.24 | 7/8 | 고온 Ioff |
| 7 | 조합 | 0.6 | 4.5 | 1e16 | TiN | 0.490584 | 538.51 | 53.69 | 8/8 | 없음 |
| 8 | 조합 | 0.6 | 4.5 | 2e16 | W | 0.479354 | 544.83 | 21.55 | 8/8 | 없음 |
| 9 | 주변 | 0.55 | 4.5 | 1e16 | TiN | 0.484180 | 595.17 | 78.45 | 8/8 | 없음 |
| 10 | 주변 | 0.6 | 4.75 | 2e16 | W | 0.484072 | 516.70 | 20.86 | 8/8 | 없음 |

- **선정 후보는 #10(1순위), #8(2순위)**이다. 모든 spec과 전류 보존을 만족한 후보의 최소 정규화 여유·평균 여유 순으로 선택했다. #10 최소 여유 0.116927, #8 0.111111이며 동일 최소 여유의 #9보다 #8의 평균 여유가 크다. 입력과 선정 당시 판단은 `selection.json`에 보존했다.
- 두 후보 모두 source/drain 각각 0.5 µm, tSi=0.5 µm, xj=0.1 µm, ND=1e19, μn/μp=400/200, doping 감쇠 12.5/5 nm와 기존 물리·ramp·solver 설정을 유지한다.
- Step 7의 두 후보 10 mV fine 계산이 별도 Python 프로세스에서 진행 중이다. Step 7·8은 아직 검증 완료로 표시하지 않는다. 단일 agent 작업이며 새 agent 시스템은 없다.

### 발견 / 이슈

- 탐색 흐름: 짧은 Lg는 Ion을 높이나 leakage/DIBL을 악화시켰다. 얇은 tox는 Vth/Ion을 개선했다. 낮은 NA·TaN만으로는 Ion과 고온 leakage를 함께 해결하지 못했다. #4 Vth는 실제 0.399957 V이므로 반올림으로 PASS 처리하지 않았다.
- #5·#6은 Ion을 충족했으나 고온 leakage가 남았다. #7에서 긴 Lg와 더 얇은 tox로 8 PASS를 확보했다. #8은 W/NA=2e16으로 Vth·leakage·DIBL 여유를 높였고, #9는 높은 Ion과 leakage 악화의 tradeoff를 확인했다. #10은 tox=4.75 nm로 Eox 여유를 늘리면서 Ion을 유지했다.
- 기존 14개와 wrapper 6개, **20개 unittest 통과**. 명령: `.conda\python.exe -B -m unittest discover -s project1/tests -v`. 횟수 상한·시간 제한 해제·허용 변수/범위·고정 physics·실패 시 1회 소비를 확인했다. `part1.py`의 docstring/purpose 두 문구만 일반 후보 측정에 맞게 바꾸고 `--help`도 확인했다. 측정과 physics 동작은 변경하지 않았다.
- 기존 CLI idvg/idvd/cv는 21/21/31점·정상 종료·bias/열/유한값을 확인했다. I–V 비교는 통과했다. C–V 첫 bit-exact 비교는 최대 2.9582e-31 F/µm(3 ULP) 차이로 실패했고 `legacy_regression.json`을 그대로 보존했다.
- 정확한 원본 코드 5개 파일은 LF→기존 CRLF 복원 후 당시 manifest hash와 모두 일치했다. **원본 코드 반복도 2 ULP 차이, 현재 코드 재실행은 baseline과 bit-exact 일치**했다. 재현되는 기능 회귀 증거는 없으며 마지막 자리의 native 수치 반복 변동으로 판단한다. 해당 변동이 생기는 내부 연산은 특정하지 못했다. 실패를 없애기 위해 solver·모델·spec 또는 허용 오차를 변경하지 않았다.
- 로그 손상은 문서 저장 인코딩 문제다. 이번 작업 시작 전 로그 25,266 byte와 기존 기록은 그대로 보존됐음을 확인했다. 손상된 새 기록을 재작성하지 않고 본 정정으로 보완했다.

### 다음 작업

- 선정 두 후보의 fine 측정을 마친 뒤 20→10 mV 비교, 전류 보존, extended/double precision, 저장 구조 fresh reload/live 재현 검증을 수행한다.
- 전체 diff·원본 보호·결과 요약·PLAN/log 일치를 확인하고 최종 종료 기록을 남긴다. 추가 설계 실험은 수행하지 않는다.

## 2026-10-04 14:14:01 KST

### 수행한 작업

- **Step 7 fine 측정 완료**, 두 후보의 gate 간격을 20→10 mV로 줄여 각각 201점씩 3개 Id–Vg와 398 K off-point를 같은 소자로 측정했다.
- **Step 8 구조 보존 확인**: 선정 구조와 입력을 `project1/results/part1_search_20261004/selected/`에 복사하고, 원본·fine·복사본 SHA 일치와 새 Python 프로세스 checker를 확인했다.
- 후보별 15개 fresh precision/live/reload probe의 numerical validation을 시작했다.

### 현재 상태

- 두 후보 모두 fine에서도 **8 PASS**. 설계 탐색은 총 10회로 종료한 상태다.

| 항목 | 요구 기준 | #10: tox 4.75 nm | #8: tox 4.5 nm |
|---|---|---:|---:|
| Vth (V) | 0.40~0.50 | 0.483985 | 0.479344 |
| Ion (µA/µm) | ≥450 | 516.697 | 544.826 |
| Ioff (pA/µm) | ≤1 | 0.013011 | 0.014048 |
| SS (mV/dec) | ≤75 | 66.2216 | 65.9750 |
| 398 K Ioff (pA/µm) | ≤100 | 20.8587 | 21.5467 |
| DIBL (mV/V) | ≤30 | 13.0377 | 12.6640 |
| Body effect (V) | ≤0.08 | 0.026610 | 0.025537 |
| Eox (MV/cm) | ≤5 | 4.21053 | 4.44444 |

- 공통 설계: W, Lg=0.6 µm, NA=2e16 cm⁻³. 모델·mobility·solver·추출 기준은 그대로다.
- 구조 파일: `selected/candidate_10_diagnostic.devsim`, `selected/candidate_08_diagnostic.devsim`. 실제 학번을 모르므로 제출 이름을 만들지 않았다.

### 발견 / 이슈

- 20→10 mV의 Vth 변화는 #10 0.086608 mV, #8 0.010199 mV로 기존 1 mV 기준 안에 있다. 전체 resolution·전류 보존·fresh replay의 통과 여부는 validator 종료 후 확정한다.
- 실행 명령: `part1.py --config <trial>/input.yaml --step-v 0.01 --output-dir <candidate>/fine`. 두 프로세스 exit 0, 각 `metrics.json`에서 measurement_complete=true, all_specs_pass=true를 확인했다.
- 구조 검증 명령: `.conda\python.exe -B project1/check_structure_file.py <selected diagnostic>`. 두 복사본의 실제 검증 exit 0, W/bulk/oxide·contact/interface 확인. 원본과 fine의 구조 hash도 동일하다.
- 패키징 보조 스크립트가 UTF-8 trial.json을 호스트 기본 cp949로 읽어 실패했다. 원인은 인코딩이며 UTF-8을 명시해 해결했다. 복사 전 존재하지 않는 파일을 검사한 최초 checker 실패 로그를 보존했고, 복사 완료 후 별도 `candidate_XX_checker_retry.log`에 실제 통과를 남겼다. 소자 파일이나 checker는 수정하지 않았다.
- 비교 그림은 matplotlib이 설치되어 있지 않아 생성하지 않았다. 추가 의존성은 도입하지 않고 위 표와 raw CSV로 결과를 제공한다.

### 다음 작업

- 각 후보의 15개 precision/live/reload probe 결과를 확인하고 실패가 있으면 native 로그를 조사한다.
- 전체 diff·원본 보호·로그 보존을 확인하고 최종 요약과 종료 기록을 남긴다.

## 2026-10-04 14:20:18 KST

### 수행한 작업

- **Project 1 Part 1 step 6·7·8 수행 종료.** 단일 변수 → 유망 조합 → 주변 탐색을 총 10회 진행하고, 선정한 최대 2개 후보의 fine·precision·전류 보존·저장 구조 재현성 검증을 마쳤다.
- 전체 diff와 원본 파일·기존 로그 보존을 검토하고 `PLAN.md`를 실제 결과에 맞췄다. 결과 요약은 `project1/results/part1_search_20261004/final_summary.json`이다.

### 현재 상태

- **총 10회 설계 측정 완료, 시간 제한 없음, 추가 탐색 없음.** 단일 변수 4회·조합 4회·주변 2회이며, #7·#8·#9·#10이 8개 spec을 충족했다. 설계 측정 ERROR는 0이다. 개별 10회 표와 변경 이유는 위 **14:11:54 KST 정정 기록**과 `summary.csv`에 있다.
- PDE 실행 합계 53.06분, 첫 탐색부터 마지막 설계 측정 종료까지 59.79분이다. 시간 제한 해제는 사용자 지시를 반영한 것이며 session의 budget_changes에도 보존했다.
- **1순위 #10**: W, Lg=0.6 µm, tox=4.75 nm, NA=2e16 cm⁻³. 가장 부족한 spec의 정규화 여유를 기준으로 선정했으며 #8보다 Eox 여유가 크다.
- **2순위 #8**: W, Lg=0.6 µm, tox=4.5 nm, NA=2e16 cm⁻³. Ion이 더 높지만 Eox 여유는 더 작다. 두 후보 모두 나머지 구조·doping·mobility·물리 모델·solver는 기존 조건을 유지한다.

| Spec | 요구 기준 | #10 최종 fine | #8 최종 fine | 현 모델 판정 |
|---|---|---:|---:|---|
| Vth (V) | 0.40~0.50 | 0.483985 | 0.479344 | 둘 다 PASS |
| Ion (µA/µm) | ≥450 | 516.697 | 544.826 | 둘 다 PASS |
| Ioff (pA/µm) | ≤1 | 0.013011 | 0.014048 | 둘 다 PASS |
| SS (mV/dec) | ≤75 | 66.2216 | 65.9750 | 둘 다 PASS |
| 398 K Ioff (pA/µm) | ≤100 | 20.8587 | 21.5467 | 둘 다 PASS |
| DIBL (mV/V) | ≤30 | 13.0377 | 12.6640 | 둘 다 PASS |
| Body effect (V) | ≤0.08 | 0.026610 | 0.025537 | 둘 다 PASS |
| Eox (MV/cm) | ≤5 | 4.21053 | 4.44444 | 둘 다 PASS |

- Baseline의 6 PASS/2 FAIL(Vth/Ion)에서 두 후보 모두 8 PASS로 개선됐다. #10 Ion은 baseline 142.05 대비 약 3.64배다. 표는 **extended 정밀도와 기존 물리 모델의 계산 결과**다.
- 진단 구조와 설정: `selected/candidate_10_diagnostic.devsim`, `selected/candidate_08_diagnostic.devsim`, 각각의 config·manifest. 실제 학번·제출 이름·보고서·commit/push는 만들거나 수행하지 않았다.

### 발견 / 이슈

- **Step 7 extended 검증 통과**: 20→10 mV 간격 비교·공통 bias·raw 전류 보존·최종 재추출 전 항목 통과. Vth 변화 #10 0.086608 mV, #8 0.010199 mV(허용 1 mV). SS 변화 0.008818/0.014472 mV/dec(허용 0.2), DIBL 변화 0.037454/0.022478 mV/V(허용 0.5).
- **Step 8 extended 재현성 통과**: 후보별 5개 중요 bias를 fresh live/reload로 다시 계산해 총 20/20 통과했다. Coarse·fine·복사 구조 hash 일치 및 두 선정 파일의 fresh checker 통과도 확인했다.
- **Double 전체 검증은 실패 상태**다. 후보별 15개, 총 30개 fresh probe를 실행했다. Double은 4/10 통과했고, 수렴 ERROR 5개와 수렴 후 전류 비교/보존 FAIL 1개가 남았다. 따라서 두 numerical validator는 **exit 1**, `extended_baseline_checks_pass=true`지만 `double_precision_complete=false`, `double_precision_checks_pass=false`, **`all_checks_pass=false`**다. 실패를 숨기거나 PASS로 바꾸지 않았다.
- Double 실패 세부: #10의 300 K 고전압 두 목표점은 VG=0/VD=1.2 V ramp에서, 398 K off는 VD=0.8 V에서 수렴 실패했다. #8의 300 K 두 목표점은 VG=0/VD=1.5 V에서 실패했다. #8 398 K는 종료됐지만 전류 balance 7.3704e-16 A/µm·상대 3.4208e-5가 기준을 넘었고 sweep 전류와의 차이도 기준을 넘었다.
- 원인 조사: Double 실패는 전위가 아닌 전자 연속 방정식 상대 오차가 80 iteration 후에도 1e-6 아래로 떨어지지 않는 경로였다. 같은 조건의 extended live/reload는 안정적으로 재현됐다. 정밀도 의존 수치 문제로 판단하되 정확한 native 내부 연산까지 특정하지 못했다. Ramp·solver 기준·mobility·물리 모델·추출 기준을 변경하지 않았다.
- 검증 명령: `part1.py --config <trial>/input.yaml --step-v 0.01 --output-dir <candidate>/fine`; `validate_part1.py --primary <trial>/primary --fine <candidate>/fine --output <candidate>/numerical_validation.json --probe-log-dir <candidate>/probes`; `check_structure_file.py <selected diagnostic>`. Raw CSV·JSON·native 로그는 후보별 경로에 보존했다.
- 기존 14개와 wrapper 6개 **20개 unittest 통과**. 명령: `.conda\python.exe -B -m unittest discover -s project1/tests -v`. 실제 test log 확인. 변경은 작은 sequential wrapper·tests와 part1.py의 문구 2개, PLAN/log 및 실험 결과다.
- 기존 CLI 21/21/31점 정상 실행과 I–V 비교 통과. 최초 C–V bit-exact 3 ULP 실패는 원본 코드 반복에서도 2 ULP 변동이 나타났고 현재 재실행은 baseline과 일치했다. Strict 실패 기록과 조사 결과를 각각 `legacy_regression.json`, `legacy_regression_review.json`에 보존했다.
- 최종 검토: 처음 tracked 104개 중 PLAN/log/part1.py 이외 **101개 hash 일치**, HW1·baseline·설정·핵심 physics 보존. 기존 로그 최초 25,266 byte prefix와 이후 append prefix 보존. KST 시간 순서·정정 이후 정상 UTF-8/필수 section·PLAN 8개 section 확인, `git diff --check` 통과.
- 남은 한계: Double 수치 안정성 미해결, mesh convergence 미검증, 조교 모델·실측 일치 미확인, ideal bottom body와 surface p+ tap 차이 및 상수 mobility/Boltzmann/SRH 등 기존 모델 가정. **현 결과를 제출용 물리 정확성의 최종 증명으로 확대하지 않는다.**
- 이번 작업의 일부 옛 추가 기록은 인코딩으로 손상됐지만 append-only 규칙대로 보존하고 14:11:54 KST에 정정했다. 선택적 그림은 matplotlib 미설치로 생략했으며 새 의존성·복잡한 자동화·multi-agent는 도입하지 않았다.

### 다음 작업

- **현재 요청은 완료됐으며 사용자 검토와 다음 요청을 기다린다.** 추가 설계 실험·step 9 보고서·제출 준비는 자동으로 진행하지 않는다.
- 후속 작업을 요청할 경우 double 안정성·모델 일치·mesh 검증의 필요성을 이 기록과 실제 실패 로그를 근거로 판단한다. 이번 10회 결과와 선정 후보를 보존한다.

## 2026-10-04 14:35:31 KST

### 수행한 작업

- **Project 1 폴더 정리 M1 완료**: 실제 import/입출력 경로, HW1 복사본, Git 상태와 복구 가능성을 조사했다.
- 새 요청에 맞게 PLAN을 갱신하고 visible 파일 289개 hash·기존 로그·원래 YAML snapshot을 확보했다.

### 현재 상태

- project1 최상위 파일 26개 중 미사용 17개를 삭제 대상으로 확정했다. 비교 스크립트 2개·실행 예제 1개·STEP2 배치 3개·옛 CSV 5개·HTML 6개이며 약 27.85 MiB다.
- 현재 simulator/package·Part 1 도구·tests·PDF·결과 이력은 보존한다. 이전 미커밋 구현·10회 실험 결과도 그대로 유지한다.
- 이전 설계의 extended 검증 통과와 double 전체 검증 실패 상태는 이번 폴더 정리로 달라지지 않는다.

### 발견 / 이슈

- 대상 17개는 모두 tracked이며 staged/unstaged diff가 없다. Git 이력으로 복구 가능하고 HW1의 reference 예제도 남는다.
- compare_models는 옛 step1 경로를 기대하는 예제다. 일반 CLI와 Part 1은 해당 비교 모듈이나 최상위의 옛 결과 파일을 읽지 않는다.
- 실제 load_config는 device/sweeps만 반환한다. 삭제 예정 compare_tcad 전용 compare YAML과 stale 설명은 정리하되 실제 device/sweep 값은 보존한다.
- 이번 요청은 기존 10회 탐색 이후 **파일 정리로 목표가 바뀐 것**이다. PLAN을 교체했으며 이전 실험 이력과 실패 증거를 삭제하지 않는다.

### 다음 작업

- 확정한 17개 파일을 project1 내부 경로 확인 후 삭제하고 README/AGENTS에 남은 구조·실행 방법을 안내한다.
- 설정 의미 동일성·imports/help·20개 tests·기존 CLI 3종을 검증한 뒤 전체 diff와 원본 보호를 확인한다.

## 2026-10-04 14:39:46 KST

### 수행한 작업

- **Project 1 폴더 정리 완료**: 실제 Part 1 개발·검증 경로에서 사용하지 않는 HW1 복사본과 옛 출력 파일 **17개를 삭제**했다.
- 삭제된 비교 예제 전용 `config.yaml`의 compare 블록과 `mosfet.py` docstring/config.py 주석의 stale 참조를 정리했다. 장치·sweep 값과 계산 코드는 그대로다.
- `project1/README.md`를 추가해 남은 파일 역할·실행 명령·결과 위치·현재 수치 검증 한계를 안내했다. AGENTS의 구조와 launcher 안내, PLAN의 최종 상태도 갱신했다.

### 현재 상태

- **project1 바로 아래 파일은 26개에서 README를 포함한 10개로 줄었다.** 폴더는 mosfet_tool/tests/results/tmp이며, 주요 개발 코드를 쉽게 찾도록 역할을 README에 정리했다.

| 구분 | 삭제한 파일 | 수 |
|---|---|---:|
| HW1 예제 | compare_models.py, compare_tcad.py, run_example.py | 3 |
| HW1 배치 실행 | STEP2_COMPARE.bat, STEP2_COMPARE_MODELS.bat, STEP2_RUN.bat | 3 |
| 옛 CSV 출력 | compare_models.csv, compare_tcad.csv, cv.csv, idvd.csv, idvg.csv | 5 |
| 옛 HTML 출력 | compare_gate_length.html, compare_gate_length_log.html, compare_models.html, compare_models_log.html, cv.html, idvd.html | 6 |

- 남은 최상위 파일: README.md, Project1_Assignment_0927.pdf, mosfet.py, config.yaml, part1.py, part1_baseline.yaml, PART1_BASELINE.md, part1_experiment.py, validate_part1.py, check_structure_file.py.
- `hw1/`, 과제 PDF, 실제 simulator/package, tests, baseline, 10회 설계 탐색 결과, raw CSV·진단 구조·검증/실패 로그와 기존 미커밋 구현은 보존했다.
- 기존 설계 후보의 extended 검증 통과와 double 전체 검증 실패는 그대로다. **파일 정리를 마친 것이며 double 문제를 해결한 것은 아니다.**

### 발견 / 이슈

- 삭제 대상 17개는 staged/unstaged 수정이 없는 tracked 파일이며 Git으로 복구 가능하다. 약 27.85 MiB의 working-tree 파일을 정리했다. 원본 학습 예제와 reference는 HW1에 남는다.
- 실제 loader 반환 Device/sweeps 및 YAML device/sweeps는 작업 전과 동일하다. config.py의 AST 전체와 mosfet.py의 docstring 제외 AST도 기존 코드와 같다.
- **20개 unittest 통과**, exit 0. 명령: `.conda\python.exe -B -m unittest discover -s project1/tests -v`.
- **기존 CLI 3종 통과**, idvg/idvd/cv 모두 exit 0. 별도 scratch에서 `mosfet.py <mode> --config <absolute project1/config.yaml>` 실행. 21/21/31점·열·bias·유한값 일치. I–V 최대 차이는 1.8635e-20/2.7105e-20 A/µm로 기존 rtol=1e-9/atol=1e-17 기준 안이며, 이번 C–V는 기준 CSV와 bit-exact 일치했다.
- 현재 5개 entrypoint import와 4개 CLI help 통과. README의 실제 링크·활성 코드/설정의 삭제 파일 참조·Python 구문·PLAN 8개 section 확인.
- 전체 diff를 검토했고 YAML 마지막 빈 줄을 제거한 뒤 **git diff --check exit 0**. 계산 구현이 바뀌지 않아 10회 탐색·fine/precision probe 전체를 다시 실행하지 않았다.
- 시작 snapshot 289개 중 삭제 17개와 의도한 기존 파일 수정 6개를 제외한 **266개 파일의 hash가 모두 일치**한다. HW1·results·이전 미커밋 source/tests 보존을 포함한다. 이전 PROGRESS_LOG byte prefix와 이번 append prefix, KST 시간 순서·정상 UTF-8·필수 section을 확인했다.
- 검증 자료는 `project1/tmp/cleanup_20261004/`의 `start_snapshot.json`, `tests.log`, `cli/`, `cli_comparison.json`, `cleanup_validation.json`에 있다. 과거 실험의 당시 source hash와 실패 판정을 덮어쓰지 않았다.
- 추가 이슈 없음. 남은 수치 문제는 이전 기록의 double 수렴·전류 보존 실패 및 물리/mesh 검증 한계다. 새 의존성·복잡한 시스템·feature·commit/push는 추가하지 않았다.

### 다음 작업

- **현재 폴더 정리 요청은 완료됐으며 다음 요청을 기다린다.** 이후 개발에서는 project1 README의 진입점과 results의 기존 증거를 사용한다.
- 수치 안정성 조사나 추가 설계 실험은 해당 요청을 받은 뒤 진행한다.

## 2026-10-04 15:24:31 KST

### 수행한 작업

- [공식 Q&A 대조] 사용자 첨부 전문과 현재 source·tests·실험 결과를 읽고 최신 PDF의 Part 1/2·제출 관련 7개 physical page를 직접 렌더링해 확인했다.
- PLAN을 이번 조사·문서 작업으로 갱신하고 `project1/OFFICIAL_QA.md`를 작성했다. AGENTS에 공식 조건을 추가하고 project1 README의 double 판정 설명을 정정했다. 구현 코드는 수정하지 않았다.

### 현재 상태

- Part 1 동일 구조 8개 측정·10회 탐색·후보 #10/#8의 기존 8 PASS/extended PASS 증거는 보존되어 있다. 공식 모델에서의 재측정은 아직 하지 않았다.
- Part 2는 checker naming 검사만 있으며 구조·CSTORE·READ·retention 구현은 없다.
- 사용자 첨부 §7의 계획 확인 후 구현 지시를 따른다. 문서·파일 보호 최종 검증이 남았다.

### 발견 / 이슈

- 공식 채점은 extended 128비트·ramp 0.1 V다. 이전 14:20:18 탐색 종료 및 14:39:46 정리 종료 기록의 double 전체 실패는 실제 진단 결과로 유지하되, **double 실패만으로 채점 탈락이라고 해석하지 않도록 정정**한다. 기존 validator는 extended와 double을 AND하므로 전체 false는 유지된다.
- 현재 고온 mobility는 400/200 고정인데 공식값은 398 K 약 202.970/107.388 cm²/(V·s)다. Gate 기준은 기존 χ+Vt ln(Nc/ni)와 공식 χ+Eg(T)/2가 다르다. Algebra 비교에서 공식 offset−기존 offset은 300 K +0.8615 mV, 398 K +1.1430 mV다. 전류 영향은 새 simulation 없이 추정하지 않는다.
- Eg/ni/SRH 구현은 공지 식·anchor와 부합한다. 별도 p+ body tap은 없으며 PDF 그림과 차이를 검토할 필요가 있다. Q&A는 tap을 허용하며 예제 농도를 의무값으로 지정하지 않는다.
- **계획 변경 이유:** 채점 정밀도 공식 확인과 물리 식 차이 발견으로 첫 우선순위를 double 통과 강제/추가 탐색에서 물리 정합화→기존 소자 재측정으로 바꿨다.
- Part 2는 최신 Lg=0.3 µm·tox≥5 nm·READ 0.5 ns/60 mV·retention BL 2/0 V를 사용한다. 기존 Part 1 후보를 그대로 적용할 수 없고 임의 Vcell failure threshold도 사용할 수 없다.
- 새 TCAD·tests는 실행하지 않았다. 기존 PASS를 공식 채점 모델의 PASS로 재명명하지 않았다. PDF SHA256과 원 공지 SHA256은 `project1/tmp/qa_review_20261004/start_snapshot.json`에 보존했다.

### 다음 작업

- 문서 diff·링크·공식 수치·source/results/HW1 보호 hash·append-only prefix를 최종 검증하고 조사 결과와 Part 1→Part 2 계획을 보고한다. 구현은 사용자 계획 확인 후 별도 범위에서 시작한다.

## 2026-10-04 15:25:39 KST

### 수행한 작업

- [공식 Q&A 대조 — 종료] 최신 PDF·공식 공지·현재 source/결과의 대조와 Part 1→Part 2 단계별 제안을 완료했다.
- 변경 파일: `AGENTS.md`, `PLAN.md`, `PROGRESS_LOG.md`, `project1/README.md`. 공식 조건·구현 대조 자료 `project1/OFFICIAL_QA.md` 한 개를 추가했다. 설계 parameter·source·tests·기존 결과는 변경하지 않았다.

### 현재 상태

- 이번 조사·문서 요청은 완료됐다. 첫 구현 제안은 T 의존 mobility·gate offset 정합화와 독립 test이며 사용자 계획 확인을 기다린다.
- 기존 후보 #10/#8의 당시 8 PASS와 extended PASS, double 전체 실패는 실제 기록 그대로다. **공식 모델에서의 spec 재측정은 미실행이며 제출 확정 상태가 아니다.**
- Part 2 전용 구조·CSTORE·READ·retention은 미구현이다. 최신 fixed Lg/tox와 READ·retention 조건을 향후 계획에 반영했다.

### 발견 / 이슈

- 새 공지로 double 실패가 곧 채점 탈락이라는 해석을 정정했다. 공식 128비트·ramp 0.1 V 기준으로 검증하되 전류 보존·해상도·구조 재로딩 검증은 유지하도록 제안했다. 기존 FAIL이나 JSON은 덮어쓰지 않았다.
- 실제 validation: `git diff --check` exit 0. 문서 링크·Markdown 표·PLAN 필수 8개 section·전체 diff·공식 수치를 확인했다. 시작 snapshot 중 의도한 문서 수정 4개 외 **기존 269개 파일 hash 모두 일치**하며 HW1·source/tests·results·과제 PDF 보존을 포함한다. 원 첨부·PDF hash도 일치한다.
- 이전 PROGRESS_LOG 57,635 byte prefix 및 이번 milestone까지의 prefix가 보존됐고 새 기록은 실제 UTC를 KST로 변환한 timestamp로 append했다. PLAN과 최종 로그의 완료 범위·남은 작업이 일치한다.
- 검증 자료: `project1/tmp/qa_review_20261004/start_snapshot.json`, `documentation_validation.json`, `pdf_pages/`. TCAD·GUI·unittest는 문서 작업이므로 새로 실행하지 않았다. 식의 수치 비교는 algebra validation이며 물리 simulation 통과 증거가 아니다.
- 남은 한계: 공식 모델 재측정, mesh 검증, 실제 채점기 세부 오차·설정, body tap 요구 해석, 실제 학번, 향후 추가 탐색 예산. 새 blocker나 문서 검증 실패는 없다.

### 다음 작업

- 첨부 §7의 “계획을 확인한 뒤 작업”에 따라 사용자 확인을 기다린다. 승인 후 먼저 공식 physics 정합화·독립 test를 수행하고 별도 실행 경로에서 기존 baseline·후보를 재검증한다. 추가 설계 탐색과 Part 2 전체 구현을 이번 요청으로 자동 착수하지 않는다.

## 2026-10-04 16:00:34 KST

### 수행한 작업

- [기존 후보 보존·공식 물리 정합화] 사용자 재개 승인으로 두 물리 계산을 최소 수정했다. Varshni 경로 μ(T)와 χ+Eg(T)/2 gate 기준을 적용했으며 legacy의 상수 μ·기존 gate 기준은 유지했다.
- physics.py·simulator.py·config.py의 anchor 설명·part1.py의 model ID/실제 μ metadata·독립/native test를 갱신했다. Validator는 필수 extended 판정과 선택적 double 진단을 분리했다.

### 현재 상태

- `.conda/python.exe -B -m unittest discover -s project1/tests -v`: 21 tests PASS, exit 0. 공식 300/398 K numeric anchor·legacy·실제 native parameter·flatband·기존 측정/구조/실험 보호를 포함한다.
- 후보 #10/#8의 기존 입력 YAML로 coarse0.02/fine0.01 V 재측정을 순차 시작했다. 결과는 새 official run 경로에 저장한다. 도핑·치수·mesh·gate 재료·solver·tolerance를 변경하지 않았다.
- PLAN은 세 묶음 A(Part1 정합화/재검증), B(Part2 구현/검증), C(보고서/최종검증)로 갱신했다.

### 발견 / 이슈

- 과거 10회 탐색·raw·FAIL·source hashes와 HW1은 보존한다. 기존 후보가 새 모델에서 통과한다고 아직 판단하지 않는다.
- Double 미실행은 None으로 표시하며 PASS로 만들지 않는다. 기존 all_checks_pass 의미도 유지하고 공식 조건의 별도 필드를 추가했다. 옛 JSON은 수정하지 않는다.
- 학번·추가 설계 탐색 예산 답변은 미확인이다. 기존 후보 재측정부터 진행하고 임의로 대규모 탐색을 재개하지 않는다.

### 다음 작업

- 기존 후보·baseline 재측정과 legacy CLI 회귀, extended 수치 validation. Part2는 공유 simulator를 활용하며 결과에 근거해 다음 결정을 기록한다.

## 2026-10-04 16:23:05 KST

### 수행한 작업

- [공식 재검증·Part2 구현] 후보 #10 coarse/fine의 8개 spec PASS를 확인했고 fresh numerical probe를 실행 중이다. 후보 #8·baseline 및 Lg/NA one-knob ablation도 진행한다. 기존 10회 탐색을 재실행하지 않았다.
- Legacy idvg/idvd/cv 실제 회귀는 21/21/31점·열·bias·유한값·기존 수치 기준 PASS. Current 최대 차이 8.89385e-21 A/µm, idvd/cv는 bit-exact다.
- CellSimulator는 기존 TR physics/transport를 상속한다. Source 위 ideal metal stem과 ZrO2 두 slab, storage/plate contact를 추가하고 실제 plate dQ/dV를 구현했다. Signed two-terminal READ·body charge·폭0.1µm·adaptive retention을 구현했다.

### 현재 상태

- 전체 29개 tests PASS, 실제 native individual/joint maximum0.1V ramp current 비교 포함(115.636s). 중간 indentation 오류는 test import에서 발견해 수정했고 실패 로그도 보존했다.
- Part2 첫 구조의 10ps READ0=128.264 mV, READ1=84.102 mV로 두 초기 READ는 PASS다. Joint bias optimization 후 READ0 전체 VBL/Vcell trace는 원 진단과 bit-exact다. 아직 retention 전체 PASS는 확인하지 않았다.
- 추가 탐색 예산·학번 답변은 미확인이다. 기존 후보 유지와 현재 첫 cell 검증을 우선한다.

### 발견 / 이슈

- 순차 set_bias가 같은 bias에도 solve해 매 READ step 최대4회 DC를 수행했다. 최종 DC 조건과 접점당 최대0.1V를 유지한 공동 갱신은 결과가 일치했다. Native tolerance는 변경하지 않았다.
- Retention에서 3mV accepted step마다 0.5ns READ를 반복하면 시간이 매우 길다. **계획 수정:** 누설 적분 ΔV≤3mV는 유지하되 30mV/8ms checkpoint 및 64ms 끝점에서 READ, 첫 sampled failure 구간은 재적분+READ bisection으로 시간1% bracket까지 좁힌다. Checkpoint 사이 단일 failure crossing 가정과 시간 불확실성을 숨기지 않는다.
- 초기/중복 계산 진단은 incomplete로 구분하고 원 READ·log를 보존했다. 시작 manifest가 종료 시에만 저장되는 약점을 확인해 새 Part2 run에서는 input/cap/READ/retention별 checkpoint JSON을 즉시 저장한다.
- 구조 checker OK는 electrical PASS와 별개다. CSTORE의 independent parallel-plate/native extraction 및 전계 검증은 통과했지만 전체 Part2 결과는 새 final metrics를 기다린다.

### 다음 작업

- 기존 후보 numerical validation·ablation 완료, Part2 checkpoint/refinement 검증과 64ms 판정. 실제 결과에 근거해 필요한 최소 재설계를 판단하고 보고서 초안과 최종 review를 진행한다.

## 2026-10-04 16:45:18 KST

### 수행한 작업

- 묶음 A 완료: 공식 mobility·gate 기준 최소 수정 후 baseline와 기존 #10/#8 재측정, 두 후보 coarse/fine·extended 검증, 최종 후보 one-knob ablation을 완료했다.

### 현재 상태

- Part 1 최종 후보 #10 유지. fine 8/8 PASS: Vth 0.484848 V, Ion 516.138 µA/µm, Ioff 0.012637 pA/µm, SS 66.222 mV/dec, 고온 Ioff 10.376 pA/µm, DIBL 13.042 mV/V, body effect 0.026622 V, Eox 4.211 MV/cm.
- #8도 8/8 및 필수 수치 검증 PASS. Part 2 CSTORE·READ0/1은 PASS이며 retention은 진행 중이다. 전체 완료로 판단하지 않는다.

### 발견 / 이슈

- `validate_part1.py`를 각 후보 coarse/fine 결과에 실행해 공식 extended 3종·ramp 0.1 V, 전류 보존, 간격 비교, raw 재추출, fresh 구조 replay를 통과했다. Double는 선택 진단으로 미실행이며 과거 double FAIL은 그대로 보존한다.
- Legacy CLI idvg/idvd/cv 회귀 21/21/31점 PASS. 29 tests PASS 후 retention checkpoint·실패 bracket 로직을 수정하고 Part 2 8 tests를 다시 통과했다.
- #10의 최악 정규화 여유 0.11704가 #8의 0.11111보다 커 기존 선택을 유지했다. Lg만 늘리면 Ion 감소, NA만 늘리면 coarse Vth 0.500344 V로 상한 경계에 걸린다. 후자는 fine 경계 검증을 완료한 것으로 주장하지 않는다.
- 기존 10회 탐색 및 과거 결과는 변경하지 않았다. 이번 결과는 `project1/results/official_20261004_155839/part1/`에 별도로 저장했다.

### 다음 작업

- 진행 중인 Part 2 degraded READ 기반 retention을 완료하고 실제 실패가 확인될 경우에만 필요한 설계를 조정한다. 이후 최종 구조 재검증·보고서·전체 review를 진행한다.

## 2026-10-04 16:48:21 KST

### 수행한 작업

- 사용자의 “일단 part1까지만 하자” 지시에 따라 작업 범위를 Part 1 최종 정리로 변경하고 Part 2 native 계산에 Ctrl+C를 전달해 종료했다.

### 현재 상태

- Part 1 후보 #10/#8 공식 재측정·필수 수치 검증 완료, 최종 #10 유지. Part 1 보고서 초안과 최종 review만 정리한다.
- Part 2 중간 코드·raw·checkpoint·log를 보존한다. 추가 실행·탐색은 중단하며 전체 PASS 또는 완료로 표시하지 않는다.

### 발견 / 이슈

- Part 2 data0는 64 ms에서 degraded READ margin 102.578 mV를 확인했다. Data1은 마지막 완료된 READ checkpoint Vcell=1.967 V / margin=82.516 mV이며 retention 미완료다. 실행 session 87704는 중단 후 exit 1을 반환했다.
- 계획 변경 이유는 최신 사용자 범위 지시다. Part 2의 실패 판정이나 설계 변경을 근거로 한 중단이 아니다.
- 실제 학번은 미확인이다. Part 1 결과를 진단 구조·보고서 초안으로 보존하며 제출 이름을 추측하지 않는다.

### 다음 작업

- Part 1만 최종 결과·검증·한계·재현 명령으로 정리하고 diff 및 기존 파일/log 보존을 검토한다. Part 2 재개는 별도 사용자 지시를 기다린다.

## 2026-10-04 16:53:54 KST

### 수행한 작업

- Part 1 공식 재검증·최종 review·결과 정리를 완료했다. 기존 10회 탐색과 후보 #10/#8을 재사용했고 최종 #10을 유지했다.
- `project1/results/official_20261004_155839/part1/selected/`에 재현 config·최종 진단 구조·fresh checker·결과 요약을 저장했다. `output/pdf/part1_report_draft.pdf` 7쪽 초안을 생성해 렌더링·검토했다.

### 현재 상태

**Part 1은 공식 모델에서 8/8 PASS이며 필수 수치 검증도 PASS다.** 최종 소자는 gate W, Lg 0.6 µm, tox 4.75 nm, NA 2e16 / ND 1e19 cm⁻³다. 같은 저장 구조로 아래 항목을 평가했다.

| 항목 | 최종 fine 결과 | 요구 기준 | 판정 |
|---|---:|---:|---|
| Vth | 0.484848 V | 0.40…0.50 V | PASS |
| Ion | 516.138 µA/µm | ≥450 | PASS |
| Ioff | 0.012637 pA/µm | ≤1 | PASS |
| SS | 66.222 mV/dec | ≤75 | PASS |
| 고온 Ioff (398 K) | 10.376 pA/µm | ≤100 | PASS |
| DIBL | 13.042 mV/V | ≤30 | PASS |
| Body effect | 0.026622 V | ≤0.08 | PASS |
| Eox | 4.211 MV/cm | ≤5 | PASS |

- 관련 테스트 21개·기존 3 CLI 회귀·fresh 구조 checker도 PASS. Part 2는 사용자 지시에 따라 중단·미완료 상태로 보존했다. 전체 과제 제출 준비가 끝났다는 뜻은 아니다.

### 발견 / 이슈

- 최종 테스트 명령: `.conda/python.exe -B -m unittest discover -s project1/tests -p "test_part1*.py" -v` — 21 tests PASS(2.294 s).
- 수치 검증은 두 후보의 coarse 0.02 / fine 0.01 V, extended 3종·ramp 0.1 V에서 간격·raw 재추출·전류 보존·새 프로세스 live/reload critical bias를 통과했다. `grading_condition_checks_pass=true`; double는 이번 필수 검사에서 미실행이며 과거 FAIL을 보존한다.
- `check_structure_file.py`로 selected 최종 구조를 새 프로세스에서 검사해 OK. 실제 저장 geometry는 Lg 0.6 µm / tox 4.75 nm, 단일 device, physics equation 없는 structure-only임을 확인했다. `git diff --check` PASS.
- 원 파일 274개 중 의도한 source/docs 12개 외 262개 hash 일치; HW1·기존 결과 및 이전 PROGRESS_LOG byte prefix 보존. 보고서의 긴 숫자 표시·그림 label·기준표를 review에서 개선했다.
- Fine raw 폴더의 원 YAML은 0.02 V지만 실제 실행은 `--step-v 0.01` override였다. 원본은 보존하고 selected 재현 config만 실제 fine 간격으로 맞췄다.
- 남은 한계: 실제 조교 시뮬레이터 전체 실행·완전한 mesh convergence 미검증, NA 경계 ablation은 coarse만 측정. 실제 학번·제출 이름·UI OK 화면이 미확정이므로 보고서는 초안이다.

### 다음 작업

- 현재 Part 1 정리 요청 완료·사용자 검토 및 다음 요청 대기. 학번이 확인되면 제출용 이름과 해당 OK 화면을 확정할 수 있다. Part 2는 별도 재개 지시 전까지 실행하지 않는다.

## 2026-10-04 17:03:59 KST

### 수행한 작업

- 사용자의 “Part 1 확실히 마무리한 뒤에 넘어가자” 요청에 따라 최신 PDF·공식 Q&A·실제 결과를 다시 대조하고 제출 준비 점검을 시작했다.

### 현재 상태

- 전기적 8개 spec·설계 범위·필수 수치 검증은 충족한다. 제출용 학번과 해당 OK 화면은 미확정이므로 Part 1의 모든 제출 조건이 완료됐다고 판단하지 않는다.
- Part 2는 계속 중단하며 소자 추가 최적화도 수행하지 않는다.

### 발견 / 이슈

- 앞선 완료 기록은 계산·검증·초안 정리의 완료였다. 전체 제출 준비까지 완료로 읽힐 수 있어 이번 계획에서 구분했다.
- 보고서 (a)의 HW1 대비/필요성, (b)의 초기 설계와 판단, (c)의 실제 영향 설명을 보강한다. 결과값을 바꾸는 작업이 아니다.
- 제출 파일 이름과 보고서에 사용할 실제 학번을 비동기로 질문했다. 답변 전 독립적으로 가능한 대조·문서 보강을 진행한다.

### 다음 작업

- 요구사항 근거표·보고서 설명·실제 OK 화면을 준비하고, 학번 확인 후 제출 이름·checker를 확정한다. 검증되지 않은 항목은 미완료로 남긴다.

## 2026-10-04 17:24:23 KST

### 수행한 작업

- Part 1 과제 요구사항을 최신 PDF와 실제 산출물로 재대조했다. `part1/PART1_REQUIREMENTS_AUDIT.md`와 `submission_audit.json`에 조건별 근거 및 완료/미완료를 기록했다.
- 보고서 (a)의 HW1 대비 물리 필요성·구현 식, (b)의 초기 소자와 시도→지표→판단, (c)의 실제 8개 ablation metric과 물리 trade-off를 보강했다. 최종 그림의 Lg/tox/xj 표시도 추가했다.

### 현재 상태

- 전기적 8 spec·설계 범위·동일 소자·공식 물리/수치 조건·구조 저장 규약 충족. 최종 후보 #10과 raw·진단 구조·소스는 그대로다.
- 보고서 7쪽 보강 및 전 페이지 렌더 검토 완료. **전체 Part 1 제출 준비는 아직 미완료**이며 실제 학번의 제출 파일과 해당 self-check OK 화면이 남아 있다.
- Part 2는 계속 중단했다. 추가 시뮬레이션·최적화·feature 구현은 하지 않았다.

### 발견 / 이슈

- 앞선 “완료”는 계산·검증·초안 정리를 뜻했다. 이번에는 제출 이름/OK 화면까지 충족했는지 분리해 `part1_submission_ready=false`를 유지한다.
- 검증: 8개 과제 threshold·공식 numerical PASS·구조 hash 일치, tox/Lg/NA 비교에서 실제 하나의 field만 변경 및 같은 sweep 확인, 문서 링크·HW1/기존 결과 hash·원 로그 prefix PASS. `git diff --check` PASS. 소자/source 변경이 없어 기존 21 tests·legacy 3 CLI 증거를 사용하고 전체 TCAD를 반복하지 않았다.
- 실제 화면 캡처 준비 중 computer-use `sky.launch_app`가 `Computer Use app approval timed out`을 반환해 UI 캡처를 완료하지 못했다. 검사 로그를 화면 캡처로 가장하지 않았다.
- 학번을 비동기로 질문했으나 현재 답변은 미확인이다. 실제 채점기 전체 실행·완전한 mesh convergence는 여전히 미검증이며 공개된 공식 조건의 만족을 채점 통과 보장으로 표현하지 않는다.

### 다음 작업

- 실제 학번과 OK 화면 확보 후 제출 이름·fresh checker·보고서 화면을 확정한다. 현재 턴의 독립 점검/보강은 완료했으며 필수 입력·화면 확보를 기다린다. Part 1 제출 준비 확정 전 Part 2로 넘어가지 않는다.
