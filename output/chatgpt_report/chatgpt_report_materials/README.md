# ChatGPT 보고서 자료 사용 안내

1. `REPORT_CONTEXT.md`가 전체 구현·설계 과정과 현재 최종 결과를 정리한 주 문서다.
2. `project1/CHATGPT_REPORT_PROMPT.md`의 본문을 ChatGPT에 붙이고 이 자료를 함께 첨부한다.
3. 과제 원본은 `project1/Project1_Assignment_0927.pdf`, 공식 답변은 `project1/OFFICIAL_QA.md`다.
4. `report_facts.json`은 기존 metrics/config를 복사해 종합한 기계 판독 자료다. 새 실험 결과가 아니다. `manifest.json`의 repository_source/SHA256으로 원본과 대조할 수 있다.

최종 수치는 Part1 official candidate_10/fine, Part2 robust19이다. 이전10회 Part1은 공식 모델 반영 전 탐색 이력이며, 첫 Part2 winner11은 역사적 비교 대상이다. README/audit/PDF 초안의 과거 학번 미확인·Part2 중단 상태는 현재 상태가 아니다.

최종 그래프 데이터는 컨텍스트9절에 있다. `verify0/verify1/fine0/fine1`의 initial_read.csv는10 ps이고 initial_read_5ps.csv는 별도 민감도 검사다. Fine0/1은 미세 retention 의미다. Null current/margin은 미측정으로 두며, degraded_read 파일은 metrics의 metadata로 hold 시각을 찾는다. 64 ms 적분과 이후 continuation을 합칠 때 중복64 ms 행을 정리하고 refinement의 실패 양끝을 별도 표시한다.

`history/PLAN_before_context.md`, `history/PROGRESS_LOG_before_context.md`는 이 문서 작업 직전의 계획·이력이다. 당시 상태를 보존했으며 최신 문서 생성 상태는 archive의 진행 이력에 소급하지 않는다.

포함된 HTML 그래프는 초기TaN baseline과 이전#11의 그래프다. 현재#19의 새 그래프는 CSV에서 작성해야 한다. 두 실제 checker OK 화면은 아직 미확보이므로 이 자료 묶음에도 없다. Checker 텍스트/JSON을 실제 화면처럼 꾸미지 않는다.

현재 Part1과 현재추천Part2 구조 파일도 포함했다. 새 Part2는 robust run/selected 경로이며 루트의 이전Part2파일은 혼동을 피하기 위해 이 묶음에 넣지 않았다. 보고서95.2 ms와 제출 구조가 일치해야 한다.

원본 CSV/JSON의 내부 경로는 원 실행 호스트·repository 경로일 수 있다. 압축을 푼 자료에서 같은 상대 경로를 찾되, 원본의 출처 문자열을 임의로 갱신하거나 raw를 덮어쓰지 않는다. 프로젝트 environment/cache/tmp전체/native solver log는 포함하지 않았다. 보고서 제작에 필요한 작은 reference code와 실제 구조·결과를 선별했다.

본 자료는 보고서 작성 지원이다. 조교 재평가 통과·독립 mesh 수렴·실험 소자 정확성을 증명하지 않는다. 보고서 PDF와 OK 화면 캡처·LearnUs 제출은 별도 작업이다.
