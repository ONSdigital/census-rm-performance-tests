Feature: RM produces all initial contact print files within a time window

  Scenario: Sample load to print file production
    Given all initial contact action rules has been scheduled in the future
    And the sample file has been loaded
    And an time has passed to allow for full sample ingestion
    When all the initial contact print files have been produced within a window of time
    Then they all have the correct line count