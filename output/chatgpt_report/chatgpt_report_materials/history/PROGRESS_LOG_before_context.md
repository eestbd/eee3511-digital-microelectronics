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

## 2026-10-04 20:26:24 KST

### 수행한 작업

- 첨부한 약 60분 탐색 지침·추가 Q&A·baseline·한글을 확인하고 Part 2 실험을 시작했다. 최종 제출 학번 2022142233을 확인했다.

### 현재 상태

- W/TiN 게이트 단일 변수 screening을 독립 프로세스로 실행 중이다. 초기 READ/hard constraint를 먼저 확인하며 기존 Part 1/HW1/공용 physics·baseline은 보존한다.

### 발견 / 이슈

- 현재 한글 손상은 없다. 조기 제외/미측정과 전체 PASS를 구분하는 Part 2 전용 실험 경로를 준비했다. 기존 READ/retention·정밀도·ramp·물리 상수는 유지한다.
- 세션과 보호 snapshot을 새 결과 폴더에 기록했다. 약 21:07 KST부터 새 탐색보다 검증을 우선하며 21:22:48 KST까지 종료를 목표로 한다.

### 다음 작업

- gate/NA/xj 단일 변수 결과로 유망 조합을 고르고 data1 retention을 실제 측정한다. 최종 후보는 두 상태 전체 검증과 fresh 구조 checker를 수행한다.

## 2026-10-04 20:37:50 KST

### 수행한 작업

- W/TiN gate, NA=1e17, xj=0.03 µm의 네 단일 변수 READ/누설 screening을 완료했다. [후보 비교](project1/PART2_OPTIMIZATION_LOG.md)를 작성했다.

### 현재 상태

- 네 후보 초기 READ/용량/전계는 PASS다. W/TiN READ1=67.391/61.373 mV, 누설=0.106686/0.056593 pA로 감소했지만 전체 retention은 진행 중이다.

### 발견 / 이슈

- Gate의 누설 감소와 READ 저하가 함께 관측됐다. NA/xj 단일 변경의 누설은 0.632/1.725 pA라 gate/cap 및 공식 허용 비균일 채널 조합을 검토한다.
- 시간 절약용 64 ms 끝점 screening은 최초 failure time을 측정하지 않는다고 표시한다. 최종 후보는 기존 공식 retention 경로로 전체 재실행한다.
- Profile test 4개 PASS. #06은 입력 생성 오류로 native 측정 전 중단되어 실패 입력/log를 보존했고, 올바른 gate 값의 #07/#08을 새 경로에서 측정한다.

### 다음 작업

- 유망 조합의 실제 READ/누설·64 ms 끝점과 유지시간을 비교하고, 가장 좋은 후보를 선택해 전체 검증으로 전환한다.

## 2026-10-04 20:58:26 KST

### 수행한 작업

- 단일 gate·cap/도핑 조합을 비교해 #11(W, h0.96, p+ body tap1e19/0.05 µm)을 전체 재검증 대상으로 선택했다. 새 탐색을 중단하고 기본/미세 간격 측정으로 전환했다.

### 현재 상태

- #11 초기 READ0/1=127.320/67.301 mV, CSTORE=19.824 fF, 전계 PASS다. 64 ms data1 끝점 마진60.418 mV로 통과했지만 전체/수치 검증은 아직 진행 중이다.

### 발견 / 이슈

- W/TiN 단일 data1 유지시간은 약 40.3/20.8 ms로 FAIL이다. #05/#09/#10은 64 ms 끝점 FAIL이고 강한 저농도 #07/#08은 body 누설 증가로 제외했다.
- #11은 body 누설을 줄여 끝점을 통과했다. 공식 비대칭 ND 후보 #12는 READ1 67.914 mV/누설0.088449 pA이며 끝점을 비교한다. 기준/물리/solver/적분을 바꿔 PASS를 만들지 않는다.
- 전체 35 tests PASS. Profile 경계 test의 기대값 오류는 decimal 경계에 맞춰 수정해 fresh NetDoping 검증 PASS이며 원 실패 로그를 보존했다. 새 sourceND 범위 test는 후속 검사한다.

### 다음 작업

- #11 두 상태 전체/미세 검증, #12 끝점, 제출 구조 fresh 검사와 보호/diff/한글 검증을 완료하고 약 60분 예산 안에 보고한다.

## 2026-10-04 21:04:04 KST

### 수행한 작업

- #12 비대칭 S/D 후보의 64 ms 끝점을 확인하고 #11 선택을 유지했다. #11 data0 전체 실행과 동일 구조의 data1 retention 기본/미세 실행을 병행한다.

### 현재 상태

- #12 끝점 마진59.145 mV로 FAIL. #11의 READ10/5 ps 검증은 완료됐고 두 상태 retention 검증은 진행 중이다. 최종 profile 7 tests PASS.

### 발견 / 이슈

- 전체 순차 실행 시간이 남은 예산보다 길 수 있어 상태별 검증을 병행하도록 계획을 조정했다. 기존 cell.retention의 적분/READ checkpoint/판정 조건은 동일하며 실제 완료 결과만 provenance와 함께 종합한다. 원 미완료 로그와 상태를 보존한다.

### 다음 작업

- 동일 구조·source·입력과 raw 데이터를 대조해 실제 측정 완료 여부를 판단하고 최종 구조/표/검증 결과를 정리한다.

## 2026-10-04 21:12:32 KST

### 수행한 작업

- 선택 #11의 초기 READ10/5 ps·data0 retention 기본/미세 검사와 학번 구조 fresh 검사를 완료했다.

### 현재 상태

- Data0 두 간격 모두≥64 ms PASS. 기본/미세 끝점 READ 마진117.214/117.304 mV. Data1 전체 검증은 진행 중이다.

### 발견 / 이슈

- 초기 READ 간격 차이0.439/0.092 mV, data0 끝점 전압/마진 차이0.636/0.090 mV다. 정한 수치 민감도 범위 안이다.
- part2_2022142233.devsim fresh checker OK, 실제 NetDoping2,142 nodes PASS. 보호 파일402개·기존 log prefix·staged 상태·실제 한글 검증 PASS. 원 순차 실행은 data0 checkpoint를 보존한 뒤 중복 data1 계산을 종료했고 동일 조건 독립 data1 실행을 사용한다.

### 다음 작업

- Data1 완료 후 provenance를 대조해 종합하고 raw/최종 문서 검증을 마친다. 약60분 예산은 유지한다.

## 2026-10-04 21:19:19 KST

### 수행한 작업

- 약56분 동안 Part 2 새 물리 후보11개를 측정하고 #11을 선택했다. 두 상태 전체 측정·기본/미세 간격·raw·학번 구조 검증과 최종 review를 완료했다.

### 현재 상태

- Local 전체 spec/validation PASS. W/h0.96/p+tap1e19·0.05 µm, CSTORE19.824 fF, gate/cap 전계5/3.333 MV/cm, 초기 READ0/1=127.320/67.301 mV. 양 상태 retention≥64 ms.
- Data1 64 ms 기본/미세 마진60.417968/60.420969 mV. 두 간격 끝점 전압/마진 차이0.072691/0.003000 mV. Fresh part2_2022142233.devsim checker OK 및 NetDoping2,142 nodes 검사 PASS.

### 발견 / 이슈

- 초기 READ10/5 ps·전류/전하·Euler update·retention3/1.5 mV·선택/출력 구조 hash·보호 파일402개·staged/log prefix·실제 한글 검증 PASS. 전체 tests35개와 후속 profile7개 PASS(중복 포함).
- 종합 결과는 같은 source/config/구조/조건의 상태별 완료 측정이다. 원 순차 실행은 data0 checkpoint 뒤 중복 계산을 종료했으며 미완료 기록과 원 로그를 보존했다. #06 입력 오류와 audit UTF-16 reader 오류도 원 로그를 남기고 원인을 바로잡았다.
- 남은 한계: data1 마진이 기준60 mV에 가깝고 전계/용량도 상한에 가깝다. ≥64 ms는 관측 하한이며 mesh 민감도/조교 전체 evaluator는 미검증이다.

### 다음 작업

- 현재 요청 완료·다음 요청 대기. 최종 후보/parameter/기준별 표는 project1/PART2_OPTIMIZATION_SUMMARY.md, 후보 해석은 PART2_OPTIMIZATION_LOG.md, 원 데이터/검증은 results/part2_optimization_20261004_202430에 있다. Part 1/HW1은 보존했으며 commit/push는 하지 않았다.

## 2026-10-04 21:39:10 KST

### 수행한 작업

- Project 1 PDF·공식 Q&A·source·최종 raw/구조·보고서를 대조해 Part 1/2 완료 상태 검토를 마쳤다. 상세 표는 project1/PART1_PART2_COMPLETION_AUDIT.md에 작성했다.

### 현재 상태

- 핵심 구현·로컬 조건 PASS: Part 1 8/8, Part 2 양 상태 READ·retention≥64 ms·CSTORE19.824 fF·전계5/3.333 MV/cm. 제출 준비는 미완료다.
- 남은 필수 항목은 part1_2022142233.devsim 준비, Part 2 구조/I(t)/READ와 지정 section을 포함한 최종 PDF, 두 학번 파일의 실제 checker OK 화면이다. Part 2 학번 파일은 존재한다.

### 발견 / 이슈

- 새 verify_review.py/part1_geometry.py 검사 PASS: 두 fresh checker OK, raw 독립 재추출·전류/전하·적분·provenance/hash, NetDoping2,340/2,142노드·singleton·equation 부재 확인. 전체 TCAD는 실행 source/raw가 그대로여서 반복하지 않았다.
- Data1 64 ms 마진60.418 mV로 여유 약0.418 mV다. Retention은 관측 하한이며 최초 실패 시각·mesh 민감도·조교 전체 evaluator는 미검증이다. 기존587개 보호 파일 hash·staged 상태·log prefix 보존을 확인했다.

### 다음 작업

- 현재 검토 요청 완료·다음 요청 대기. 후속 제출 준비에서는 검증 구조를 보존해 두 학번 파일·최종 보고서·OK 화면을 완성한다. 이번에는 코드/소자/과거 결과/PDF 변경, 재최적화·commit/push·제출을 하지 않았다.

## 2026-10-04 23:19:02 KST

### 수행한 작업

- 요청한 소자 저장·자가검사 절차에 맞춰 Part 1 최종 diagnostic을 part1_2022142233.devsim으로 byte 동일 복사하고 두 실제 학번 파일을 fresh 검사했다.

### 현재 상태

- Part 1/2 학번 파일 모두 준비 완료. 최종 측정 hash 일치, checker exit0/OK, singleton 및 physics equation 부재 PASS. 증거는 project1/results/submission_check_20261004_231707/validation.json이다.

### 발견 / 이슈

- Mesh→doping→저장→physics 순서는 기존 simulator.build에 이미 구현돼 있어 코드 수정·재실험이 필요 없었다. 원본 구조/physics/config/raw/PDF와 staged 상태·기존 로그를 보존했다.
- 실제 Windows terminal OK 화면은 생성하지 않았다. Text log를 screenshot으로 대체하지 않으며 PLAN과 최종 안내의 명령을 사용자 terminal에서 실행해 캡처한다.

### 다음 작업

- 이번 파일 준비·자가검사 요청 완료. 사용자는 두 OK 화면을 캡처해 최종 보고서에 삽입한다. 통합 보고서 완성·최종 제출은 남아 있으며 이번에는 commit/push·업로드를 하지 않았다.

## 2026-10-05 11:26:06 KST

### 수행한 작업

- 최종 Part 2 구조의64 ms checkpoint를 재로딩하고 기본/미세3/1.5 mV로 누설 적분을 이어가 최초 sampled READ 실패를 확인했다.

### 현재 상태

- Data1 기본72.597648 ms/59.269445 mV, 미세72.119709 ms/59.338223 mV에서 실패. 64 ms는 양쪽 모두 이전 마진을 재현해 PASS이며 두 시각 사이의 실패 구간을 좁히는 중이다.

### 발견 / 이슈

- 독립 상수 누설 기대값3건·source/config/최종 구조 hash·CSTORE 및 seed READ 재현 PASS. 이 실패는64 ms 이후 보존 한계를 찾는 정상 측정이며 기존 최소조건 PASS를 취소하는 결과가 아니다.

### 다음 작업

- Data1 실패 구간폭≤0.1%를 측정하고 data0가 그 상단까지 유지되는지 확인한 뒤 원시 적분/READ·민감도·보호 검증과 최종 기록을 남긴다. 원 결과는 보존한다.

## 2026-10-05 11:39:08 KST

### 수행한 작업

- 최종 Part 2 구조를 유지한 채64 ms 이후 실제 누설 적분·재읽기·bisection을 기본/미세 간격으로 측정하고 data0 보존을 추가 확인했다.

### 현재 상태

- Cell retention estimate 약67.2 ms, 제한 상태data1. 미세 구간67.171761~67.235196 ms, 중간값67.203479 ms. Data0는72.5976 ms까지 실제 PASS, 그때 미세 READ 마진116.763318 mV다.
- 기존≥64 ms 최소조건 PASS는 유지된다. 상세 결과는 project1/PART2_RETENTION_ESTIMATE.md, raw/검증은 results/retention_estimate_20261005_111911에 보존했다.

### 발견 / 이슈

- Analytic continuation3건·64 ms fresh 재현·실제READ/전류/전하/Euler·failure bracket≤0.1%·source/구조/CSTORE·기본/미세 민감도 검사 PASS. 두 estimate 차이0.012945 ms(0.0193%). 기존592개 보호 파일·staged/log prefix도 보존했다.
- 유한 간격/모델에서의 추정값이며 수학적으로 정확한 시간은 아니다. Data0 단독 최대 retention·mesh 민감도·조교 evaluator는 미검증이다. 기존 코드/설계/과거 결과/PDF와 Part1/HW1은 변경하지 않았다.

### 다음 작업

- 이번 추가 측정 요청 완료·다음 요청 대기. 최종 제출 보고서에는 기존≥64 ms 확인과 새cell estimate를 구분해 반영할 수 있다. 이번에는 commit/push·업로드를 하지 않았다.

## 2026-10-05 12:07:10 KST

### 수행한 작업

- Part2 여유 개선: 최신 PDF50~57쪽·공식 Q&A·기존 측정 코드와 결과를 대조하고2시간 예산/633개 파일 보호 snapshot을 준비했다.

### 현재 상태

- 신규 run은 `project1/results/part2_robust_search_20261005_115807/`. 단일 변수 후보 측정 중이며 기존 Part1/HW1/최종 Part2·직전67.2 ms 결과는 보존했다.

### 발견 / 이슈

- Gate TaN/tap 유지 후보와 낮은 source-side NA 후보의 초기data1 READ는84.561/76.523 mV로 개선됐지만 저장 누설은2.878/0.227 pA로 기준0.069 pA보다 커졌다. 구조/C/초기READ 검증은 완료했으나 retention PASS로 해석하지 않는다.
- 초기READ만으로 선택하지 않고64 ms 열화 후 READ를 확인한다. Mobility/precision/ramp 등 공식 physics와 판정은 변경하지 않는다.

### 다음 작업

- Tap/NA/xj/tox/ND의 영향을 비교하고 유망 조합→endpoint→최종 두 상태·미세 간격 검증을 진행한다. 종료 시각13:58:07 KST를 지킨다.

## 2026-10-05 12:19:01 KST

### 수행한 작업

- Part2 단일 변수·초기 조합의 구조/plate C/READ/누설을 비교하고 유망 비균일 채널 후보의64 ms 실제 endpoint 검증을 시작했다.

### 현재 상태

- #10의 초기data1 READ71.951 mV·저장누설0.057507 pA로 기준67.301 mV·0.069343 pA보다 개선됐다. 용량·전계 여유를 더한 #19도 측정 중이며 아직 최종 PASS로 선언하지 않는다.

### 발견 / 이슈

- NA1e17·tox5.5 nm 단독 후보는 초기READ FAIL. TaN/높은 sourceND의 READ 이득에도 누설 증가가 있어 두 목적을 함께 봐야 한다. 상세 결과·미측정 구분은 새 run의 results_matrix.csv/JSON에 유지한다.
- 사용자가2시간을 채우거나 극한 최적화를 할 필요가 없다고 지시했다. 충분히 개선된 후보를 검증하면 조기 종료하도록 PLAN을 수정했다. 기본 목표는64 ms data1 마진≥64 mV·보존≥96 ms이며 과제 필수 조건과 구분한다.

### 다음 작업

- 유망 후보의 두 상태·READ5 ps·retention1.5 mV·fresh 구조/NetDoping을 검증하고 실제 연장 보존 결과 또는 하한을 보고한다. 검증된 충분한 후보가 나오면 추가 탐색을 멈춘다.

## 2026-10-05 12:25:10 KST

### 수행한 작업

- 12개 후보 screening와 #10/#19의64 ms data1 endpoint를 비교하고 #19를 최종 검증 후보로 선택했다. 사용자 지시에 따라 추가 parameter 탐색을 종료했다.

### 현재 상태

- #19: 초기data1 READ69.463 mV/64 ms63.557 mV, C19.281938 fF/Eox4.716981/Ecap2.5 MV/cm. Source-side NA1e15/drain-side NA1e17, sourceND1e20/drainND1e19, tox5.3 nm/cap4 nm·h1.245 µm다.

### 발견 / 이슈

- 기존64 ms 마진60.418 mV 대비 기준60 mV 초과분이 약8.5배로 늘고 용량·전계도 개선됐다. #10은65.280 mV지만 기존 C/Eox 경계값을 유지해 #19를 균형 후보로 골랐다.
- 초기≥75 mV/64 ms≥64 mV 희망 목표는 미충족이며 필수 기준과 구분한다. #19의 구조/NetDoping fresh 검증은 PASS, 두 상태·미세 간격·연장 retention은 진행 중이다. 기존 소자와 과거 결과는 보존한다.

### 다음 작업

- 두 상태의64 ms 및 최대128 ms 실제 READ 판정과 미세 간격을 검증한다. 충분히 개선되면 최초 failure를 더 찾지 않고 확인한 보존 하한을 명시해 종료한다.

## 2026-10-05 12:37:35 KST

### 수행한 작업

- 선택 #19의 저장 구조를 두 fresh process에서 재측정해 READ10/5 ps와64 ms adaptive retention·재읽기를 검증했다.

### 현재 상태

- 기본64 ms 두 상태 PASS: data0=112.955710 mV/data1=63.557209 mV. 초기READ5 ps 민감도·source/구조/C 일치·signed Euler·전류/전하 검증 PASS. 상세 raw는 신규 run의 experiments/19_balanced_ND20/verify0·verify1에 보존했다.

### 발견 / 이슈

- Data1은 endpoint 결과를 재현했고 기준60 mV 여유가 기존0.418→3.557 mV다. Data0도64 ms에서 충분한 마진을 유지했다. 연장 retention과 미세1.5 mV는 진행/대기 중이므로 최종 전체 검증 완료로 선언하지 않는다.

### 다음 작업

- 최초 READ 실패 구간 또는128 ms 실제 통과 하한을 확인하고 미세 간격·전체 raw audit 뒤 새 추천 구조와 간결한 비교 결과를 저장한다. 추가 후보 탐색은 종료한 상태다.

## 2026-10-05 12:47:46 KST

### 수행한 작업

- #19 기본3 mV 적분의64 ms 이후 실제 재READ·bisection을 완료하고 미세1.5 mV 두 상태 검증을 시작했다.

### 현재 상태

- Data1 bracket94.929035~95.451378 ms, midpoint95.190207 ms. Data0는128 ms/109.730137 mV PASS여서 셀 한계는data1이다. 두 상태의 기본64 ms 조건과 초기READ10/5 ps는 PASS다.

### 발견 / 이슈

- 기존67.203479 ms 대비 약42% 증가했고64 ms 보존 여유는약3.2→31.2 ms로 커졌다. 96 ms 희망값은 약0.8% 미달이며64 ms 필수 조건과 구분한다. 64 ms 이후 실패 관측은 정상적인 한계 측정이며 과제 탈락을 뜻하지 않는다.
- Raw bracket 양끝 margin60.027768/59.964459 mV로 실제 통과·실패를 구분한다. 사용자가 극한 탐색을 원하지 않아 후보를 더 늘리지 않고 이 균형 설계를 검증한다.

### 다음 작업

- 미세 간격·raw 전류/전하/Euler·source/구조·보호 및 final review를 완료하고 새 추천 파일·간결한 비교 결과를 저장한다. 기존 파일은 보존한다.

## 2026-10-05 13:17:07 KST

### 수행한 작업

- Part2 여유 개선 완료:12개 후보 비교 후 #19의 두 상태·기본/미세·구조 및 전체 raw 검증을 마치고 새 추천 설정/학번 파일을 별도 저장했다. 탐색·수치 검증 약77분으로 조기 종료했다.

### 현재 상태

- Data1/cell estimate95.198837 ms(미세 bracket94.937594~95.460080 ms), 기존67.203479 ms 대비41.66% 개선. 64 ms data1 마진63.559235 mV, data0는128 ms/109.821026 mV까지 실제 PASS다.
- C19.281938 fF/Eox4.716981/Ecap2.5 MV/cm. 소자 필수 조건 로컬 PASS. 상세는 `project1/PART2_ROBUST_SEARCH.md`; 새 구조는run의 `selected/part2_2022142233.devsim`, 설정은 `project1/part2_robust.yaml`이다.

### 발견 / 이슈

- READ10/5 ps·retention3/1.5 mV·전류/전하/Euler·실패 양끝·fresh checker/NetDoping·범위·source/hash 검증 PASS. 두 estimate 차이0.008630 ms(0.009066%). 기존631개 파일·staged/log prefix를 보존했다.
- 희망75 mV/64 mV/96 ms 등은 일부 미달이지만 과제60 mV/64 ms와 구분했다. 독립 mesh·조교 evaluator/data0 최대 시간·제출 보고서/OK 화면은 남았다. Part1/HW1/core·기존 root Part2/과거 결과는 변경하지 않았다.

### 다음 작업

- 현재 최적화 요청 완료·다음 요청 대기. 새 추천은 별도 경로이며 재현은구조 reload를 사용한다. Commit/push·제출·추가 극한 탐색은 하지 않았다.

## 2026-10-05 14:29:19 KST

### 수행한 작업

- Part1·2 완료와 제출 준비를 PDF 제출 페이지·최종 metrics/validation·학번 파일 hash·현재 PDF 초안으로 재확인했다. 새 실험과 소자 변경은 하지 않았다.

### 현재 상태

- Part1 8/8 및 Part2 새 #19 필수 조건 로컬 PASS. Part1 학번 파일도 존재·기존 checker OK 구조와 동일하다. 구현·설계는 완료됐고 제출 준비는 미완료다.

### 발견 / 이슈

- 보고서 외 두 실제 OK 화면과 정확한 학번 파일 묶음이 필요하다. 루트 Part2는 이전 #11이며 새 #19는 robust run/selected에 있다. 7쪽 Part1 초안의 학번 미확인·Part2 미완료 문구는 최종 PDF에서 갱신해야 한다.
- 기존 검증과 실제 파일 hash 일치·8개 PASS/Part2 all_minimum_specs_pass 확인. 조교 evaluator·독립 mesh 검증은 미확인이며 채점 PASS를 보장하지 않는다.

### 다음 작업

- 현재 확인 요청 완료·다음 요청 대기. 남은 필수 준비는 통합 PDF·두 OK 화면·새 추천 파일을 포함한 제출 묶음이며, 추가 최적화는 필수로 편입하지 않는다.
