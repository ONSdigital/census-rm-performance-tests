Feature: RM produces all initial contact print files within a time window

  @three-hundred-and-fifty-thousand
  Scenario: 350,000 Sample load through to initial contact print file production
    Given the 350,000 unit sample file has been loaded
    And the sample has been fully ingested into action scheduler database
    When all initial contact action rules are scheduled for now
    Then all the initial contact print files are produced on the SFTP containing the correct total number of cases within 1 hour
    And they are produced within the time limit 30 minutes

  @three-and-a-half-million
  Scenario: 3.5 Million Sample load through to initial contact print file production
    Given the sample file "3_5_million_sample.csv" has been loaded from the bucket
    And the sample has been fully ingested into action scheduler database
    When all initial contact action rules are scheduled for now
    Then all the initial contact print files are produced on the SFTP containing the correct total number of cases within 2 hours
    And they are produced within the time limit 100 minutes

  @thirty-million
  Scenario: 30 Million Sample load through to initial contact print file production
    Given the sample file "30_million_household_sample.csv" has been loaded from the bucket
    And the sample has been fully ingested into action scheduler database
    When all initial contact action rules are scheduled for now
    Then all the initial contact print files are produced on the SFTP containing the correct total number of cases within 12 hours
    And they are produced within the time limit 720 minutes
