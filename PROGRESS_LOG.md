# PROGRESS_LOG.md

중요 결정·결과·문제·남은 작업만 시간순으로 기록한다. 현재 계획은 `PLAN.md`, 작업 규칙은 `AGENTS.md`를 참조한다. 시간대는 Asia/Seoul(KST, UTC+9)다.

사용자의 2026-10-04 정리 요청에 따라 과거 기록을 요약했다. 아래 과거 표제는 원래 기록 시각이며 본문은 요약이다. 중복 검증·사소한 진행·인코딩 손상 후 정정된 중복 내용은 생략했다. 원본은 로컬 [백업](project1/tmp/git_log_cleanup_20261004_174102/PROGRESS_LOG.md)에 보관하며 Git에는 포함하지 않는다. 이후 중요한 사건만 간결하게 append한다.

## 2026-10-04 00:55:04 KST

### 수행한 작업

- 단일 agent Level 1 workflow와 AGENTS/PLAN/PROGRESS_LOG 운영·문서 검증을 완료했다.

### 현재 상태

- PLAN은 현재 계획·상태, 로그는 시간순 이력을 관리한다. 기능·HW1은 변경하지 않았다.

### 발견 / 이슈

- 문서 검증 PASS. 구현 전 조사·계획, milestone별 검증, 원인 조사, 최종 review를 기본 작업 방식으로 설정했다.

### 다음 작업

- 다음 요청에서 과제 요구사항을 먼저 조사하고 승인된 범위만 진행한다.

## 2026-10-04 02:02:40 KST

### 수행한 작업

- Part 1 step 1~5: 제출 구조·물리 보완·8개 spec 측정·초기 소자 baseline 검증을 완료했다.

### 현재 상태

- 당시 모델 baseline은 6/8 PASS, Vth=0.5503 V와 Ion=142.05 µA/µm는 FAIL이다. 결과는 [baseline](project1/results/part1_baseline/primary/metrics.json)에 있다.

### 발견 / 이슈

- 14 tests·기존 CLI·coarse/fine·extended live/reload PASS. Double 고전압 ramp 수렴 실패로 당시 전체 validation은 PASS가 아니다.
- Fine 실행 source hash 시점 차이는 [출처 보완](project1/results/part1_baseline/provenance_review.json)에 기록했다. 원본 결과를 덮어쓰지 않았다.

### 다음 작업

- 사용자 확인 후 변수 탐색을 진행한다. 구조 checker OK와 전기적 spec 충족은 구분한다.

## 2026-10-04 14:20:18 KST

### 수행한 작업

- Step 6~8: 단일 변수 4회→조합 4회→주변 2회, 총 10회 탐색과 후보 2개 검증을 완료했다. 사용자 지시로 시간 제한을 해제했다.

### 현재 상태

- 당시 모델에서 #7~#10은 8/8 PASS, 최종 #10·차선 #8을 선정했다. [10회 표](project1/results/part1_search_20261004/summary.csv)와 [선정·검증 요약](project1/results/part1_search_20261004/final_summary.json)을 보존한다.

### 발견 / 이슈

- 두 후보의 fine·전류 보존·extended 재현성은 PASS지만 double은 수렴 ERROR 5개/비교·보존 FAIL 1개로 전체 검증 FAIL이다. 실패 JSON과 로컬 상세 로그를 보존한다.
- 기존 C–V의 3 ULP strict 비교 실패는 원본 반복에서도 2 ULP 변동이 있었고 재실행은 일치했다. [조사 결과](project1/results/part1_search_20261004/legacy_regression_review.json)를 보존하며 solver·허용 오차로 실패를 숨기지 않았다.

### 다음 작업

- 추가 탐색 없이 공식 모델·수치 조건을 확인한다. 이 시점 결과를 최종 채점 통과로 확대하지 않는다.

## 2026-10-04 14:39:46 KST

### 수행한 작업

- Project 1에서 사용하지 않는 HW1 복사 예제·launcher·옛 출력 17개를 삭제하고 README를 정리했다.

### 현재 상태

- HW1 원본·실제 simulator·tests·과제·baseline·10회 결과는 보존했다.

### 발견 / 이슈

- 20 tests·CLI 3종 PASS. 설정 값·계산 동작은 동일하며 double 문제를 해결한 작업은 아니다.

### 다음 작업

- 공식 공지와 현재 구현의 차이를 확인한다.

## 2026-10-04 15:25:39 KST

### 수행한 작업

- 최신 과제/공식 Q&A를 대조하고 [공식 조건](project1/OFFICIAL_QA.md)을 정리했다.

### 현재 상태

- 공식 채점은 extended 128비트·ramp 0.1 V다. Double 실패 자체가 채점 탈락을 뜻하지 않는다. 과거 FAIL 판정은 유지한다.

### 발견 / 이슈

- 공식 μn=400(T/300)^−2.4, μp=200(T/300)^−2.2 및 gate 기준 χ+Eg(T)/2와 기존 구현의 차이를 발견했다. 공식 모델 재측정 전에는 제출 소자를 확정하지 않는다.

### 다음 작업

- 승인 후 물리식을 맞추고 기존 baseline/#10/#8을 새 run에서 재검증한다. 기존 10회 탐색은 다시 시작하지 않는다.

## 2026-10-04 16:48:21 KST

### 수행한 작업

- 사용자 “Part 1까지만” 지시로 Part 2 계산을 중단하고 계획 범위를 축소했다.

### 현재 상태

- Part 2 코드·raw·checkpoint는 보존했으며 전체 완료/PASS가 아니다. Data0 retention 64 ms는 확인했지만 data1 retention은 미완료다.

### 발견 / 이슈

- Data0 READ margin=102.578 mV, data1 마지막 checkpoint Vcell=1.967 V/margin=82.516 mV다. 중단은 사용자 범위 변경에 따른 것이며 process exit 1을 기록했다.

### 다음 작업

- Part 1만 최종 정리한다. Part 2는 별도 재개 지시 전까지 실행하지 않는다.

## 2026-10-04 16:53:54 KST

### 수행한 작업

- 공식 μ(T)/gate 기준 적용 후 기존 후보를 재검증했다. #10 유지, [최종 소자·결과·재현 명령](project1/results/official_20261004_155839/part1/selected/README.md)과 7쪽 보고서 초안을 정리했다.

### 현재 상태

- 최종 #10: W, Lg=0.6 µm, tox=4.75 nm, xj=0.1 µm, tSi=0.5 µm, S/D 각각 0.5 µm, NA=2e16/ND=1e19 cm⁻³. 같은 소자로 공식 8/8 PASS다.
- Fine 결과: Vth 0.484848 V, Ion 516.138 µA/µm, Ioff 0.012637 pA/µm, SS 66.222 mV/dec, 398 K Ioff 10.376 pA/µm, DIBL 13.042 mV/V, body effect 0.026622 V, Eox 4.211 MV/cm.

### 발견 / 이슈

- 21 Part 1 tests·기존 CLI 3종·구조 checker·공식 extended 3종/ramp 0.1·coarse/fine·전류 보존·raw 재추출·fresh live/reload PASS. [수치 검증](project1/results/official_20261004_155839/part1/candidate_10/numerical_validation.json)을 보존한다. Double는 이번에 미실행이며 과거 FAIL은 남긴다.
- Fine 원 YAML의 0.02 V는 CLI에서 0.01 V로 override했다. Selected config는 실제 간격으로 맞췄다. 실제 채점기 전체·완전한 mesh convergence·NA 경계 fine 검증은 미완료다.

### 다음 작업

- Part 1 과제/보고서/제출 조건을 마지막으로 대조한다. 추가 최적화나 Part 2는 진행하지 않는다.

## 2026-10-04 17:24:23 KST

### 수행한 작업

- [요구사항 대조표](project1/results/official_20261004_155839/part1/PART1_REQUIREMENTS_AUDIT.md)·[제출 점검](project1/results/official_20261004_155839/part1/submission_audit.json)을 작성하고 보고서 (a)/(b)/(c)를 보강·전 페이지 렌더 검토했다.

### 현재 상태

- Part 1 전기적·설계·구조 조건 충족. **제출 준비는 미완료**: 실제 학번의 `part1_[학번].devsim`과 해당 self-check OK 화면이 남았다. [보고서](output/pdf/part1_report_draft.pdf)는 초안이다.

### 발견 / 이슈

- 실제 학번은 미확인이고 UI 앱 접근 승인 시간 초과로 OK 화면을 확보하지 못했다. 공개된 공식 조건 만족을 실제 채점 보장으로 표현하지 않는다.

### 다음 작업

- 학번·실제 OK 화면 확보 후 제출 이름과 보고서를 확정한다. Part 2는 중단 상태로 유지한다.

## 2026-10-04 17:44:26 KST

### 수행한 작업

- GitHub 제외 대상을 정리하고 사용자 요청에 따라 과거 로그 38건/1,057줄을 핵심 8건/153줄로 요약했다. AGENTS에 짧은 기록과 사용자 요청 시 원본 백업 후 정리 규칙을 반영했다.

### 현재 상태

- 상세 실행 로그 81개(약 53 MB)를 Git index에서만 제외했다. 로컬 파일과 설정·raw CSV·검증 JSON·소자·checker·PDF·HW1은 보존했다.
- 원본 로그는 위 백업 경로에 보관했다. Part 1은 공식 8/8 PASS지만 제출 이름/OK 화면이 남았고 Part 2는 중단·미완료다.

### 발견 / 이슈

- 제외/유지 26개 사례·기존 파일 418개 hash·원본 백업·날짜/링크·문서 및 diff 검증 PASS. [검증 근거](project1/tmp/git_log_cleanup_20261004_174102/validation.json)를 남겼다. 코드 변경이 없어 TCAD/test는 재실행하지 않았다.

### 다음 작업

- 현재 정리 요청 완료·다음 요청 대기. 이후에는 중요한 결과·문제·계획 변경·종료만 총 4~8개 bullet로 기록한다.

## 2026-10-04 17:46:39 KST

### 수행한 작업

- Part 1 제출 점검과 Part 2 source/공식 조건/checkpoint를 대조하고 다음 순서를 PLAN에 정리했다. 구현·시뮬레이션은 실행하지 않았다.

### 현재 상태

- Part 1 공식 8/8 PASS, 학번 파일/OK 화면은 미완료다. Part 2 기존 CSTORE 18.585 fF·READ 0/1 128.264/84.102 mV와 data0 ≥64 ms를 확인했지만 data1 retention은 중단·미완료다.

### 발견 / 이슈

- 기존 Part 2를 재사용하여 전체 baseline→수치 검증→필요 시 재설계→최종 제출 순으로 진행한다. 현재 CLI에 checkpoint 자동 resume는 없고 Part 1의 탐색 예산을 Part 2에 자동 적용하지 않는다.

### 다음 작업

- 이번 순서 정리 완료·후속 요청 대기. Part 1 제출 준비 확정 후 Part 2 실행 요청에 따라 baseline 측정/검증 묶음부터 진행한다.

## 2026-10-04 17:56:25 KST

### 수행한 작업

- 최신 사용자 지시로 Part 1 제출 준비를 마지막으로 미루고 Part 2 점검·전체 baseline·수치 검증 묶음을 시작했다. 공식 PDF/source를 대조하고 기존 29 tests PASS를 확인했다.

### 현재 상태

- 기본 3 mV/미세 1.5 mV retention run을 새 결과 폴더에서 실행 중이다. 두 run의 초기 구조 checker·CSTORE 18.585 fF·전계 검사는 PASS이며 READ/retention 전체 판정은 아직 미완료다.

### 발견 / 이슈

- 기존 소자·물리·solver 조건은 유지했다. 시작 snapshot/비교 기준은 [session](project1/results/part2_baseline_20261004_175214/session.json)에 저장했다. 현재 새 수치 실패는 없으며 이전 data1 중단은 이번 전체 측정으로 확인한다.

### 다음 작업

- 두 상태 전체 측정, raw 재계산/간격 비교, 저장 구조 fresh replay를 완료하고 실제 결과로 보완 필요성을 정리한다.

## 2026-10-04 18:15:40 KST

### 수행한 작업

- 두 실행의 초기 READ와 data0 retention 64 ms 측정을 완료했다. 같은 입력·구조·물리에서 retention 전압 간격만 3→1.5 mV로 비교했다.

### 현재 상태

- 초기 READ 0/1=128.264/84.102 mV PASS. Data0 64 ms 재READ 마진은 기본 102.578/미세 102.676 mV로 둘 다 PASS다. Data1과 fresh replay는 아직 진행/미검증이다.

### 발견 / 이슈

- READ 10/5 ps 차이 0.436/0.164 mV, data0 retention 끝점 Vcell/마진 차이 0.716/0.098 mV로 사전 기준 이내다. 수렴 오류는 없으며 전체 완료/PASS 판정은 두 상태 검증 후 내린다.

### 다음 작업

- 이전 중단 지점 이후 data1 retention을 완료하고 raw 독립 재계산·fresh 구조 replay·최종 판단 표를 정리한다.

## 2026-10-04 18:30:51 KST

### 수행한 작업

- 기본 data1 retention에서 60 mV 미만 재READ 마진을 관측하고 최초 실패 구간 refinement를 진행한다.

### 현재 상태

- Vcell=1.604 V에서 마진=59.095 mV다. Data0는 ≥64 ms PASS지만 data1 실패가 관측되어 전체 spec PASS로 처리할 수 없다. 정확한 failure time/fine/fresh 검증은 아직 미완료다.

### 발견 / 이슈

- Solver 오류 없이 저장 전압이 누설로 내려가며 READ 마진이 감소했다. 조건/오차를 바꿔 통과시키지 않고 사전 기준대로 미세 간격·전류/전하·재로딩을 대조한다.

### 다음 작업

- 최초 failure time과 재현성을 확정해 결과를 보고한다. 재설계는 사용자 검토 후 결정한다.

## 2026-10-04 19:47:57 KST

### 수행한 작업

- Part 2 단계 2~4 완료: 기존 구현 점검·전체 baseline·간격/전류/전하/저장 구조 검증을 묶어 실행하고 [결과 표](project1/results/part2_baseline_20261004_175214/README.md)와 곡선을 저장했다.

### 현재 상태

- CSTORE 18.585 fF, gate/cap 전계 5/3.333 MV/cm, 초기 READ 0/1 128.264/84.102 mV, data0 ≥64 ms는 PASS다. **Data1 retention 2.627~2.643 ms로 전체 spec FAIL**이다.
- 미세 간격에서도 data1 2.634~2.648 ms FAIL이다. 측정은 정상 완료했으며 소자·물리·solver·source·Part 1/HW1은 변경하지 않았다.

### 발견 / 이슈

- Data1 누설 약 2.99→2.46 pA로 저장 전압이 내려가 READ 기준 60 mV를 벗어났다. 실패 시각의 간격 민감도 0.215%로 사전 기준 1% 이내이며 재로딩에서도 재현됐다.
- [수치 검증](project1/results/part2_baseline_20261004_175214/validation.json) PASS: Conda unittest 29개, raw 독립 재계산, READ 10/5 ps·retention 3/1.5 mV 비교, fresh 9개 사례. 420개 기존 파일·staged 상태·이전 log prefix·diff·문서 링크/명령 검증 PASS다.
- YAML LF/CRLF로 인한 scratch 비교 오류와 결과 명령/그래프 표현을 수정했고 원 실패 로그/raw는 보존했다. Full mesh convergence·실제 조교 시뮬레이터·그래프 시각 검토는 미실행이다.

### 다음 작업

- 이번 묶음 완료·사용자 결과 검토 대기. 추가 설계 탐색은 수행하지 않았으며 data1 누설/retention 보완 여부는 다음 요청에 따른다. 학번 파일/OK 화면/최종 보고서 준비는 마지막에 한다.

## 2026-10-04 19:58:13 KST

### 수행한 작업

- Part 1 보존 조건에서 Part 2 수정 방향을 분석했다. 최신 PDF·Q&A·gate 재료 표와 baseline/fresh 전류 성분을 대조했다.

### 현재 상태

- 분석 완료; 새 후보 변경·시뮬레이션은 미실행이다. 기존 data1 retention 약 2.64 ms FAIL 상태를 유지하며 Part 1/HW1/공용 코드/기존 입력·결과는 보존했다.

### 발견 / 이슈

- Data1 초기 저장 전류 2.988 pA 중 반대 drain 성분 98.42%, body 성분 0.047 pA다. Gate TaN→W/TiN을 먼저 비교하고 READ 속도 저하를 함께 확인하는 방향을 권장한다.
- 필요한 유지시간 개선은 약 24.29배인데 CSTORE 증가 여유는 7.61%다. 유망 gate에 h=0.96 µm(기하 추정 19.824 fF)를 결합하되 실제 dQ/dV로 검사한다.
- 420개 기존 파일 hash·staged 상태·diff/문서 링크를 확인했다. 새 후보의 spec PASS는 미검증이며 접점 전류만으로 누설 메커니즘을 확정하지 않았다.

### 다음 작업

- 수정 방향 분석 요청 완료. 후속 설계는 gate 단일 변수→유망 gate+capacitor→필요 시 doping/junction→전체 READ/retention·수치 검증 순을 권장한다.

## 2026-10-04 20:06:40 KST

### 수행한 작업

- 추가 공식 Q&A 3항을 OFFICIAL_QA·AGENTS·PLAN에 반영했다. 문서 반영 요청을 완료했으며 실험/코드/입력 변경은 하지 않았다.

### 현재 상태

- Part 1 기존 PASS 설계를 보존하며 Part 2는 독립 pass transistor+capacitor 최적화로 취급한다. 기존 Part 2 data1 약 2.64 ms FAIL 판정은 그대로다.

### 발견 / 이슈

- Source contact 바로 위 capacitor 배치와 bulk-hk node 0개인 해당 구조가 허용됐다. Bare silicon 배치/contact 축소를 강제하지 않고 checker·naming·연결·plate dQ/dV를 확인한다.
- 허용 범위 내 비균일/비대칭 doping이 가능하다. 최종 spatial distribution은 NetDoping에 표현하고 미인식 LDDDoping/HaloDoping에 의존하지 않는다. 후속 후보 선택지가 넓어졌지만 아직 구현·측정하지 않았다.
- 문서 외 393개 보호 파일 hash·staged 상태·문서 링크·diff 검증 PASS. 기존 로그를 보존했다. 새 실험/test는 문서 범위에 필요 없어 미실행이다.

### 다음 작업

- 이번 반영 완료·실험 시작 요청 대기. 이후 Part 2 고유 조건으로 gate/cap 및 필요 시 비균일/비대칭 doping을 검토하고 저장 NetDoping·READ/retention을 실제 검증한다.

## 2026-10-04 20:13:39 KST

### 수행한 작업

- 사용자 요청에 따라 PLAN 전체와 2026-10-04 20:06:40 KST 로그 한 건의 손실된 한글을 확인 가능한 작성 원문으로 복원해 UTF-8로 저장했다.

### 현재 상태

- 문서 한글 복구 완료. 손상되지 않은 이전 로그와 원래 기록 시각을 보존했고 Part 1/HW1/Part 2 코드·입력·결과는 변경하지 않았다.

### 발견 / 이슈

- 이전 PowerShell→Python stdin 전달 중 한글이 ?로 치환됐다. 당시 UTF-8 decoding만 검사해 실제 문자 손상을 놓쳤다. AGENTS에 UTF-8 파일 직접 작성·실제 한글/물음표 확인 규칙을 추가했다.
- 손상본과 검증 snapshot은 ignored project1/tmp/encoding_repair_20261004_201208에 보존했다. 사용자 복구 요청에 따른 해당 기록의 본문 정정이며 과거 정상 이력은 그대로 유지했다.
- 실제 한글·strict UTF-8·문서 링크·diff·정상 로그 prefix·문서 외 394개 보호 파일 hash·Git staged 상태 검증 PASS. 문서 변경이므로 실험/TCAD/test는 미실행이다.

### 다음 작업

- 이번 복구 요청 완료. 다음 실험 요청을 기다리며 추가 공식 Q&A와 Part 1/2 독립 설계 기준을 유지한다.
