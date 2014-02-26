Feature: Book App :: Publish new book
    
    Scenario: User publish new book
        Given I was a logged-in user
        When I go to book index page
        And I click publish new book
        And I fill in book title
        And I fill in book description
        And I select image for book cover
        And I select book author
        And I create new author of this book
        And I select book categories
        And I select languages
        And I submit the publish form
        Then I see a book was published
        And I was on the post new chapter page
        And the book was not listed yet
        When I post a new chapter for this book
        Then I see that book was listed
