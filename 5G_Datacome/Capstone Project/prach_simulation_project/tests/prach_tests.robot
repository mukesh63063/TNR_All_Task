*** Settings ***
#Library    prach_simulation.PrachSimulation    WITH NAME    PrachSim
Library    Collections
Library    OperatingSystem

*** Variables ***
@{LOADS}    10    100    500

*** Test Cases ***
Run PRACH Simulation
    [Documentation]    Run PRACH simulation for different loads and save results
    ${results}=    Run Test Cases    ${LOADS}
    ${module}=    Evaluate    prach_simulation    prach_simulation
    Call Method    ${module}    save_results    ${results}    output/prach_results.json
    Call Method    ${module}    generate_graphical_report    ${results}
    Validate Low Load Success    ${results}

*** Keywords ***
Run Test Cases
    [Arguments]    ${loads}
    ${results}=    Create List
    FOR    ${load}    IN    @{loads}
        ${sim}=    Evaluate    prach_simulation.PrachSimulation(${load})    prach_simulation
        ${result}=    Call Method    ${sim}    simulate_cfbra
        Append To List    ${results}    ${result}
    END
    [Return]    ${results}

Validate Low Load Success
    [Arguments]    ${results}
    ${low_load_result}=    Get From List    ${results}    0
    Should Be Equal As Numbers    ${low_load_result["successRate"]}    1.0    Low load should have 100% success