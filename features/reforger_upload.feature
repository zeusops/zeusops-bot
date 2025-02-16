Feature: Upload mission
  As a Zeus
  I need to upload new missions
  So that I can Zeus the next operation

Background:
  Given a discord channel to run commands in
  And a base config file to overwrite with new modlist/scenario

Scenario: Upload next mission
  Given a Zeusops mission locally ready
  When Zeus calls "/zeus-upload"
  And Zeus specifies <modlist.json>, <scenarioId>, <filename>
  Then a new server config file is created

Scenario: Load mission from previous upload
  Given a Zeusops mission was uploaded already under <filename>
  When Zeus calls "/zeus-set-mission" with <filename>
  Then a symbolic link is created from "current-config.json" to <filename>

Scenario: Restart server
  When Zeus calls "/zeus-restart-server"
  Then reforger server restarts
