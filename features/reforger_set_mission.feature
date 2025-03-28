Feature: Loading a mission to run it now
  As a Zeus
  I need to activate an uploaded mission
  So that I can run the mission on server now

Scenario: Load mission from previous upload
  Given a Zeusops mission was uploaded already under <filename>
  When Zeus calls "/zeus-set-mission" with <filename>
  Then a symbolic link is created from "current-config.json" to <filename>

Scenario: Load two missions back to back
  Given a Zeusops mission was uploaded already under <filename>
  And another Zeusops mission was uploaded already under <filename2>
  And Zeus has already called "/zeus-set-mission" with <filename>
  When Zeus calls "/zeus-set-mission" with <filename2>
  Then a symbolic link is created from "current-config.json" to <filename2>

# Consider moving this to separate feature?
Scenario: Restart server
  When Zeus calls "/zeus-restart-server"
  Then reforger server restarts
