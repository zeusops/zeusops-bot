Feature: Show currently active mission
  As a Zeus
  I need to know the currently active mission config
  So that I can know which mission the server is running

Background:
  Given a discord channel to run commands in

Scenario: Show currently active mission
  Given file "mission1.json" exists in the mission directory
  And "mission1.json" is set as the active mission
  When Zeus calls "/current-mission"
  Then "mission1" is displayed
