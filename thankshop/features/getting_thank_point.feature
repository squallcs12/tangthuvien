Feature: As a user
	I can get thank points by login to the website daily
	And I can spend my thank points to thank other people
	
	Scenario: User get points by daily login
		Given I was a non-logged-in user
		When I log into the website for the first time in a day
		Then I receive a number of thank points
		When I re-login again
		Then I do not receive any thank points
		When I do not log into website in the next day
		Then I see my thank points was decreased
		
	Scenario: User give thank points to the poster
		Given I was a logged-in user
		When I thank a poster for a chapter
		Then I see my thank points was spent
		And poster thanked points was increased by half of those points
		When I use all my thank points
		Then I can not thank anylonger
		
	Scenario: Prevent auto thank
		Given I was a logged-in user
		When I thank a poster for a chapter
		Then I can not give any thank in a short time
		
	Scenario: Prevent get too many thank each days
		Given I was a logged-in user
		Then I can not receive more than a limited number of thank points for a chapter on a day
		
	Scenario: User buy thank points
		Given I was a logged-in user
		When I go to the buy thank points page
		Then I see a list of thank points packages
		When I buy a packages
		Then I receive an amount of thank points to spend