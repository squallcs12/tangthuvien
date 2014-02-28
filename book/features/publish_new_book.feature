Feature: Book App :: Publish new book

    Scenario: User publish new book
        Given I was a logged-in user
        When I visit book index page
        And I click on "New book"
        Then I see the new book form
        When I fill in book title "New book title"
        And I fill in book description
        And I select image for book cover
        And I select book author
        And I select book categories
        And I select languages
        And I submit the publish form
        Then I see a book was published
        And I see the post new chapter form
        And the book was not listed yet
        When I post a new chapter for this book
        Then I see that book "New book title" was listed
