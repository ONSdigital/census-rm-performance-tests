Feature: RM produces all initial contact print files within a time window

  Scenario: Sample load through to initial contact print file production
    Given the sample file has been loaded fully into the action db
    And all initial contact action rules have been scheduled for now
    Then all the initial contact print files are produced on the SFTP
    And they all have the correct line count
    And they are produced within the configured time limit