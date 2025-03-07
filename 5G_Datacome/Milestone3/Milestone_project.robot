*** Settings ***
Documentation    Simple Google Search Test
Library          SeleniumLibrary

*** Variables ***
${BROWSER}       Chrome
${URL}           https://www.google.com
${SEARCH_TEXT}   selenium

*** Test Cases ***
Google Search Test
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    name:q    10s
    Input Text    name:q    ${SEARCH_TEXT}
    Press Keys    name:q    ENTER
    Wait Until Element Is Visible    xpath:(//h3)[1]    20s
    Click Element    xpath:(//h3)[1]
    Wait Until Page Contains    Selenium    15s
    Close Browser
