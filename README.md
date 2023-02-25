# Find Your Furmily - Paw Match

Access deployed app from here: **[Paw Match](https://paw-match.herokuapp.com/)**

#### 1. Goal

This website will give a series of questions to narrow down the search for a potential pet from rescue organizations.

#### 2. Type of users 

Anyone who is looking to adopt a pet. It is important to make this website easy to navigate so anyone can find their future pet easily.

#### 3. API 

**[Petfinder API](https://www.petfinder.com/developers/v2/docs/)**
This API will provide detailed pet and organization information.


#### 4. Database schema

- User table -user’s information with password
- User’s preference table - store user’s pet preferences
- User comments table -store users comment on pets and organizations
- Favorite pet table - store user’s favorite pets
- Maybe pet table - store user’s second choice pets
- Favorite organization table -store user’s favorite organization


#### 5. Possible Issues with API 

API could be unavailable	

#### 6. Sensitive information that needs to be secured

Password, username, and email.

#### 7. Functionality

- Ask a series of questions to find out the user's preference for a pet.
- Rather than a showing list of pets, this website will show a randomly chosen pet one by one up to 10 animals.
- A User will choose yes, no, maybe on the pet shown. 
- Website will create a list of animals with “yes” and “maybe”. -Users can edit the lists and add comments to each pet. 


#### 8. User flow 

1. Show questions for a user to answer to find an ideal pet
2. Shows first matched pet information -> user will choose “yes”, “no”, “maybe”. Depending on a user’s answer, the pet will be added to “yes” list and “maybe” list. A user will repeat this 10 times.
3. Last page will show “Yes List”, “Maybe List” (potentially show the map of pets locations)
4. Inside those lists, a user can click on each pet to find more details and leave any thoughts or comments.
	
#### 9. What features make my site more than CRUD? Stretch goals?

More than CRUD : having a logic behind to choose random 10 pets for users
Stretch goal: potentially show the map of pets or shelter locations

