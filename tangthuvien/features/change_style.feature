Feature: Tangthuvien :: Change style
    As a user
    I want to change the website style as I want

    Scenario: User change style
        Given I was a logged-in user
        When I visit the homepage
        And I change the style of website
        Then I see the style of website was changed
        When I reload the page
        Then I still see the style of website was keep as I changed