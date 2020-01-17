Feature: RM produces all initial contact print files within a time window

  Scenario: Sample load through to initial contact print file production
    Given the sample file has been loaded
    And the sample has been fully ingested into action scheduler database
    When all initial contact action rules are scheduled for now
    Then all the initial contact print files are produced on the SFTP
    And they all have the correct line count
    And they are produced within the configured time limit

  @skip
  Scenario: 3.5 Million Sample load through to initial contact print file production
    Given the sample file "3_5_million_sample.csv" has been loaded from the bucket "census-rm-performance-test-files"
    And the sample has been fully ingested into action scheduler database
    When all initial contact action rules are scheduled for now
    Then all the initial contact print files are produced on the SFTP
    And they all have the correct line count
    And they are produced within the time limit 100 minutes
