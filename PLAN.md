# PLAN.md

현재 작업: Project 1 구조 저장·학번 파일 준비·자가검사.
상태: 두 학번 파일 준비·fresh checker·structure-only 검사 완료. 실제 OK 화면 캡처와 보고서 삽입은 사용자 terminal에서 진행한다.

## Goal

사용자가 제시한 저장/자가검사 절차를 기존 최종 설계에 적용해 두 학번 구조 파일을 준비하고 실제 checker 결과를 확인한다. 보고서용 실제 OK 화면을 얻는 실행 방법을 안내한다.

## Current State

- simulator.py의 build는 mesh→doping→write_devices→physics 순서로 이미 저장한다. 재구현·HW1 수정·전체 시뮬레이션 재실행은 필요 없다.
- Part 1 최종 #10 diagnostic SHA256은41c6f8f6ff5782c8ec3ecbc98d39bd264149ec076630f8bad0c9c98d6f06d07c, Part 2 최종 #11 학번 구조는f2442ee257af6dfcb610db5928d0ff5d3b8e5bce1d2423d72e00c7fb099fe62e다.
- 이전 review에서 두 선택 구조의 singleton·physics equation 부재·실제 NetDoping 및 로컬 성능 PASS를 확인했다. Part 1 학번 파일 준비는 마지막에 하도록 유보됐으며 이번 요청에서 진행한다.
- 최종 보고서 및 두 실제 OK 화면의 보고서 삽입은 아직 남아 있다.
- project1/part1_2022142233.devsim을 최종 diagnostic과 byte 동일 복사했고 Part 2 파일은 그대로 보존했다. 두 파일의 fresh checker exit0/OK 및 singleton/equation 부재 PASS. 새 증거는 project1/results/submission_check_20261004_231707/validation.json이다.

## Requirements

- 학번2022142233으로 project1/part1_2022142233.devsim, part2_2022142233.devsim을 준비한다.
- 원 최종 구조를 byte 동일하게 보존한다. Part 1은 기존 structure-only diagnostic을 복사하며 원본을 이동·재저장하지 않는다.
- 기존 destination이 다른 내용이면 덮어쓰지 않는다. 각 파일을 fresh Python에서 checker 및 singleton/equation 검증한다.
- 사용자 terminal에서 두 검사 결과를 직접 표시하고 실제 OK 화면을 캡처할 수 있는 PowerShell 명령을 제공한다.
- 코드/physics/parameter/raw/HW1·기존 보고서는 보존한다. 최종 보고서 작성·제출·commit/push는 이번 범위에 포함하지 않는다.

## Assumptions

- 이미 physics 전에 저장했고 검증된 byte 동일 파일을 학번명으로 복사하는 것은 소자 재설계가 아니다. 동일 hash라면 기존 전기적 검증과 연결된다.
- 현재 연결에는 Windows native terminal 화면 제어가 없으므로 실제 화면 캡처는 사용자의 VSCode terminal에서 검사 실행 후 수행한다. Text log를 실제 캡처로 표시하지 않는다.

## Plan

- [x] 최신 PLAN/log와 build 저장 위치, 최종 파일/hash 확인.
- [x] 보호 snapshot 후 Part 1 학번명 파일을 byte 동일 복사하고 Part 2 hash 대조.
- [x] 두 실제 학번 파일의 fresh checker·singleton/equation 검사 및 결과 보존.
- [x] PLAN/log 최종 갱신, 보호/UTF-8/diff 확인, 사용자 화면 캡처 명령 정리.

## Validation

- .conda/python.exe를 사용하고 .conda/Library/bin DLL PATH, PYTHONIOENCODING=utf-8을 준비한다.
- 각 구조의 hash를 과거 최종 metrics와 대조하고 fresh process에서 check_structure_file.py의 exit0 및 OK를 확인한다.
- 별도 fresh read에서 exactly one device·모든 region equation 부재를 확인한다. 물리 재등록이나 측정 결과 저장을 하지 않는다.
- 기존 파일 hash·staged 상태·기존 log byte prefix·한글·git diff --check를 확인한다. 의미 있는 종료 기록은 현재 UTC→KST 시각으로 append한다.
- 실제 실행: .conda/python.exe -B project1/tmp/submission_preparation_20261004_231707/prepare.py PASS. 기존 최종 측정 hash와 두 제출명 파일이 일치하고 새 프로세스마다 checker exit0/OK, singleton/equation 부재를 확인했다. Text log는 실제 UI 화면 캡처로 표시하지 않았다.

사용자 화면 캡처용: 저장소 루트 VSCode PowerShell terminal에서 실행한다. Last4는 실제 checker 출력의 OK/재료/접점/계면 줄만 표시한다.

```powershell
$repoRoot = (Get-Location).Path
$env:PATH = "$repoRoot\.conda\Library\bin;$repoRoot\.conda;$env:PATH"
$env:PYTHONIOENCODING = 'utf-8'
& .\.conda\python.exe -B .\project1\check_structure_file.py .\project1\part1_2022142233.devsim | Select-Object -Last 4
& .\.conda\python.exe -B .\project1\check_structure_file.py .\project1\part2_2022142233.devsim | Select-Object -Last 4
```

두 OK와 파일명/재료/접점/계면이 보이도록 terminal을 넓히고 Win+Shift+S로 실제 화면을 캡처한다. 이 화면을 최종 보고서에 넣는다.

## Progress / Discoveries

- 저장 코드는 project1/mosfet_tool/simulator.py build에서 doping 직후 physics 직전에 구현돼 있다. Part 2도 상속한 build를 사용한다.
- 새로 만들 것은 Part 1 제출명 파일과 두 실제 학번 파일의 검사 증거다. 실험이나 code patch는 필요 없다.
- 새 학번 파일은 최종 측정 당시 structure-only 파일과 같은 hash다. 저장 코드 수정이나 물리 등록 이후 재저장을 하지 않았다. 기존 소자·raw·code·PDF를 유지했다.

## Final Review

- 저장 절차 설명·두 제출명 파일 준비·두 fresh checker 및 structure-only 검증 완료. 코드/parameter/원본 구조·과거 결과·PDF를 변경하지 않았다. 재실험·commit/push·업로드는 수행하지 않았다.
- 두 실제 UI OK 화면 캡처·최종 보고서 삽입/완성은 남은 항목이며 명령으로 안내한다. Checker 결과를 전기적 spec 새 측정으로 주장하지 않는다.
- 최종 기존 파일 hash·staged 상태·log byte prefix·실제 UTF-8 한글·diff check PASS. 2026-10-04 23:19:02 KST 최종 기록을 append했다. 파일 준비/자가검사 요청 완료다.
