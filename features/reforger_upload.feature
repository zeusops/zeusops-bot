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
  And the version numbers are removed from the mods.

Scenario: Upload next mission with versions retained
  Given a Zeusops mission locally ready
  When Zeus calls "/zeus-upload" with "keep_versions=True"
  Then a new server config file is created
  And the config file is patched with <modlist.json> and <scenarioId>
  And the version numbers are kept as-is.

Scenario: Upload next mission and activate
  Given a Zeusops mission locally ready
  When Zeus calls "/zeus-upload" with the activate flag
  Then the server config file is set as the active mission

Scenario: Upload next mission without modlist
  Given a Zeusops mission locally ready
  When Zeus calls "/zeus-upload"
  And Zeus specifies <scenarioId>, <filename>
  Then a new server config file is created
  And the config file is patched with just <scenarioId>
