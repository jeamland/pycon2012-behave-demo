Feature: Add entries to page
    As a PyCon attendee
    In order to meet up with other attendees
    I want to tell people which flight I'm on

    Scenario: Add person to flight
        Given I am at the PyCon AU meetup page
        When I select "DJ 1320" as my flight
        And I select "Friday" as my arrival day
        And I enter "Benno Rice" as my name
        And I click "Add me!"
        Then my flight should appear in the flights table
        And my name should appear next to my flight
