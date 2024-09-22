Task 0: Custom User Model and Authentication System
Custom User Model (CustomUser)
Extends AbstractUser:

The CustomUser model uses the email field for authentication instead of the default username field (username = None).
USERNAME_FIELD = 'email' specifies that email is the primary field for user identification.
REQUIRED_FIELDS = [] ensures only email and password are required when creating a superuser.
Additional Fields:

bio: A text field with a max length of 250 characters to store user information.
profile_picture: An optional ImageField for user profile pictures.
followers: A ManyToManyField relating to itself, allowing users to follow and unfollow other users.
symmetrical=False ensures the following relationship is one-way

follow(self, user): Adds the specified user to the following list.
unfollow(self, user): Removes the specified user from the following list.
is_following(self, user): Returns True if the current user is following the specified user.
is_followed_by(self, user): Returns True if the specified user is following the current user.
User Manager:

UserManager handles creating users and superusers via the create_user and create_superuser methods.
create_user ensures email and password are set, while create_superuser enforces that is_staff and is_superuser are both True.


Serializers
RegisterSerializer:

Defines the password field as write_only=True to prevent it from being exposed in serialized responses.
Overrides the create method to:
Create a new user.
Automatically generate and associate a token for the user using Token.objects.create(user=user).
TokenSerializer:

Simple serializer for returning a token key in API responses.
ProfileSerializer:

Used for retrieving and updating the user's profile.
The email and followers fields are marked as read_only, ensuring they cannot be modified by the user.
Users can only update their bio, password, and profile_picture.

Views
RegisterView:

Subclasses CreateAPIView to handle user registration.
The create method is overridden to:
Serialize and validate the incoming data.
Save the user and automatically generate a token.
Return the serialized user data along with the token key upon successful registration.
LoginView:

Subclasses GenericAPIView to handle user login.
The post method retrieves the email and password, then authenticates the user using Django’s authenticate() method.
If authentication is successful, the token is either retrieved or created (if it doesn’t already exist), and the token key is returned.
If authentication fails, an error message is returned.
ProfileView:

Subclasses RetrieveUpdateAPIView to allow authenticated users to view and update their own profile.
Only the logged-in user can access or modify their profile data by overriding the get_object method to return self.request.user.


Task 1:

Post and Comment System:
PostSerializer:
The PostSerializer is used to serialize the Post model.

Author Field: The author field is set as a ReadOnlyField with the source set to author.email, which means the author's email
will be displayed, but it cannot be modified by the user.
Read-Only Fields: Both created_at and updated_at are also set as read-only fields, ensuring they cannot be manually modified,
and are automatically populated by the system.
Overriding the create method:
The create() method is overridden to automatically assign the logged-in user as the author of the post. This is achieved 
by retrieving the request object from the serializer's context.
The context contains additional information, such as the current request, and in this case, request.user is used to assign
the user creating the post as the author.
CommentSerializer:
The CommentSerializer is similar to the PostSerializer, with some key differences:
Post Field: The post field is represented using a SlugRelatedField, which displays the post title instead of the post ID. 
This makes the comment API more readable by allowing the title of the related post to be shown rather than its ID.
The rest of the fields (author, created_at, and updated_at) follow the same pattern as in PostSerializer.

Views for Posts and Comments:
PostViewSet and CommentViewSet:
Both PostViewSet and CommentViewSet inherit from ModelViewSet, which provides built-in functionality for listing, creating,
updating, and deleting posts and comments.

Querysets: Each view uses a queryset to retrieve all posts or comments from the database.
Serializer Class: Each view is tied to its respective serializer (PostSerializer or CommentSerializer).
Permissions: The IsAuthenticatedOrReadOnly permission ensures that authenticated users can create, update, or delete posts
and comments, while unauthenticated users can only read them (GET requests).
Filtering and Searching:
filterset_fields allows users to filter posts and comments by title and content.
search_fields provides the ability to search across titles and content, enabling more flexible querying of posts and comments.
Overriding get_object:

The get_object() method is overridden in both views to enforce that only the author of a post or comment can update or delete it.
If a user tries to modify or delete a post or comment they do not own, they will receive a PermissionDenied error, ensuring
only authors can manage their own content.