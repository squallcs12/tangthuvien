Feature: Book App :: Publish new book
    
    Scenario: User publish new book
        Given I was a logged-in user
        When I publish a new book
        Then I see that book is listed
        
    Scenario: Listing book by category
        Given I publish a number of books
        When I visit those book categories
        Then I see the book was listed there