Feature: Book App :: Generate book prc

	Scenario: Create book prc
		Given a book exist
		And some chapter was posted
		And after period of time
		Then a prc file was generated for this book
		And the prc file was listed in the list of attachments