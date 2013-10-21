Feature: Book App :: Publish new book
    
    Scenario: User publish new book
        Given I was a logged-in user
        When I publish a new book
        Then I a book was published
        And I was on the post new chapter page
        And the book was not listed yet
        When I post a new chapter for this book
        Then I see that book was listed

    Scenario: Listing book by category
        Given I publish a number of books
        When I visit those book categories
        Then I see the book was listed there