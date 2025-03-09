Feature: List uploaded mission configs
  As a Zeus
  I need to see a list of uploaded mission configs
  So that I can choose which mission to load

Background:
  Given a discord channel to run commands in

Scenario: List uploaded missions
  Given files "mission1.json" and "mission2.json" exist in the mission directory
  When Zeus calls "/zeus-list"
  Then a list of mission names is returned
