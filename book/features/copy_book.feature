Feature: Book App :: Copy book
    As user, I want to copy a book from live site to dev site
    So that I can read it on dev site

    Scenario: Copy book
        Given I was a logged-in user
        When I visit book index page
        And I press "Copy book"
        And I fill in book title
        And I fill in book description
        And I select image for book cover
        And I select book author
        And I create new author of this book
        And I select book categories
        And I select languages
        And I fill in book source thread page
        And I submit the publish form
        Then I see the copying was processed
        When the process is finished
        Then I see the whole book was copied
        And I can not copy this thread again
        When I visit the copied book
        Then I can sync the new posted chapter from main-site of this book
        When I sync the new posted chapter
        Then I see the copying was processed
        When the process is finished
        Then I see only new posted chapter was copied
        When I visit the redirect page for copied thread id
        Then I was redirected to the reading page of copied book
