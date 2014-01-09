Feature: Book App :: Generate book prc

	Scenario: Create book prc
		Given a book exist
		And some chapter was posted
		And after period of time
		Then a prc file was generated for this book
		And the prc file was listed in the list of attachments


	Scenario: Manually generate prc file
		Given I was a logged-in super user
		When I read a book
		And I press generate prc button
		Then I see the generate prc process was shown
		When the process is done
		Then a prc file was generated for this book
		And the prc file was listed in the list of attachments