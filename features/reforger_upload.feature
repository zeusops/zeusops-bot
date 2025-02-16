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
  And the config file is patched with <modlist.json> and <scenarioId>

Scenario: Upload next mission without modlist
  Given a Zeusops mission locally ready
  When Zeus calls "/zeus-upload"
  And Zeus specifies <scenarioId>, <filename>
  Then a new server config file is created
  And the config file is patched with just <scenarioId>
