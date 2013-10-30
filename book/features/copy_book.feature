Feature: Book App :: Copy book
    As user, I want to copy a book from live site to dev site
    So that I can read it on dev site

    Scenario: Copy book
        Given I was a logged-in user
        When I visit book index page
        And I press "Copy book"
        And I fill the book information page
        Then I see the copying was processed
        When the process is finished
        Then I see the whole book was copied
        