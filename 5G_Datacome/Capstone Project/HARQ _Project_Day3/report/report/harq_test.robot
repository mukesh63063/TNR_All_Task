*** Settings ***
Library    OperatingSystem
Library    String

*** Test Cases ***
Run HARQ Simulation
    [Documentation]    Runs the HARQ simulation and checks if outputs are generated
    Execute HARQ Simulation
    Check Output Files Exist

Validate HARQ Success Rate
    [Documentation]    Validates that the HARQ success rate is reasonable
    ${report}=    Get File    output/summary_report.txt
    ${success_rate_line}=    Get Line    ${report}    1
    ${success_rate}=    Fetch From Right    ${success_rate_line}    :
    ${success_rate}=    Remove String    ${success_rate}    %    ms
    ${success_rate}=    Convert To Number    ${success_rate}
    Should Be True    ${success_rate} > 0    Success rate should be greater than 0%

Validate HARQ Latency
    [Documentation]    Validates that the average latency is reasonable
    ${report}=    Get File    output/summary_report.txt
    ${latency_line}=    Get Line    ${report}    2
    ${latency}=    Fetch From Right    ${latency_line}    :
    ${latency}=    Remove String    ${latency}    %    ms
    ${latency}=    Convert To Number    ${latency}
    Should Be True    ${latency} > 0    Latency should be greater than 0 ms

*** Keywords ***
Execute HARQ Simulation
    Run    python main.py

Check Output Files Exist
    File Should Exist    output/harq_logs.txt
    File Should Exist    output/harq_plot.png
    File Should Exist    output/summary_report.txt