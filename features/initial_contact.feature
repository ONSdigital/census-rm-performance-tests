Feature: RM produces all initial contact print files within a time window

  Scenario: Sample load through to initial contact print file production
    Given all initial contact action rules have been scheduled in the future
    And the sample file has been loaded
    When the action rules trigger
    Then all the initial contact print files are produced on the SFTP
    And they all have the correct line count
    And they are produced within the configured time limit