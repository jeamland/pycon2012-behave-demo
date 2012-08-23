Feature: Main page
    As a PyCon attendee
    In order to meet up with other attendees
    I want to see a list of flights I can add myself to

    Scenario: Meetup form present
        When I fetch the meetup page
        Then I should see the meetup form

    Scenario: Flights table
        When I fetch the meetup page
        Then I should see the flights table
