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

task 2 :
FollowUserView:
Extends GenericAPIView
Overriding the post method:
The post method is overridden to handle the logic of following another user.
Retrieve the user to follow: user_to_follow = get_object_or_404(CustomUser, id=user_id) retrieves the user that the logged-in user wants to follow. If the user with the given user_id does not exist, a 404 Not Found error is raised.
Following the user: request.user.follow(user_to_follow) calls the follow helper method from the CustomUser model, adding the selected user to the following list of the logged-in user.
Creating a notification: After successfully following the user, i create a notification
Notification.objects.create(
    recipient=user_to_follow,  # The user who is followed
    actor=request.user,  # The user who is following
    verb='followed',  # The action performed
    target=user_to_follow  # The target of the action
)
Returning the response: You then return a success message indicating that the current user is now following the other user.
Similar Structure to FollowUserView:
The process is similar to the FollowUserView. The post method handles the logic for unfollowing a user.
Retrieve the user to unfollow: user_to_unfollow = get_object_or_404(CustomUser, id=user_id) fetches the user that the current user wants to unfollow.
Unfollowing the user: request.user.unfollow(user_to_unfollow) removes the selected user from the following list of the current user.
Creating a notification: After the unfollow action is completed, a notification is created with the verb 'unfollowed':
python
Copy code
Notification.objects.create(
    recipient=user_to_unfollow,  # The user who is being unfollowed
    actor=request.user,  # The user who is unfollowing
    verb='unfollowed',  # The action performed
    target=user_to_unfollow  # The target of the action
)
This notifies the unfollowed user of the action.
Returning the response: You return a success message indicating that the current user has unfollowed the user.

now for FeedVIew:
et_queryset(self): This method is overridden to customize the data that the view returns. Here's how it works:
user = self.request.user: It retrieves the currently authenticated user from the request.
following_users = user.following.all(): This fetches all users that the authenticated user is following
return Post.objects.filter(author__in=following_users).order_by('-created_at'): This query retrieves all Post objects whose
authors are in the list of followed users. The results are ordered by the created_at timestamp in descending order

Like and Unlike System
Like Model
The Like model tracks which users have liked which posts. It includes:

post: A foreign key to the Post model, representing the post that is liked.
user: A foreign key to the CustomUser model, representing the user who liked the post.
Unique Constraint: Users can only like a post once (unique_together = ('post', 'user')).
String Representation: The __str__ method returns a string showing which user liked which post.

LikePostView:
permission_classes = [permissions.IsAuthenticated]:
Ensures only authenticated users can like a post.
post(self, request, pk):
Retrieve Post: The post is retrieved using generics.get_object_or_404(Post, pk=pk). If the post with the given primary key (pk)
doesn’t exist, a 404 error is raised.
Create or Get Like: Like.objects.get_or_create(user=request.user, post=post) either creates a new Like object if it doesn’t
exist or retrieves an existing one.
Handling Duplicate Likes: If the like already exists (i.e., the user has already liked the post), the view returns an error
response: 'you have already liked this post'.

UnlikePostView:
permission_classes = [permissions.IsAuthenticated]:

Ensures only authenticated users can unlike a post.
post(self, request, pk):

Retrieve Post: The post is retrieved using generics.get_object_or_404(Post, pk=pk). If the post with the given primary key (pk)
doesn’t exist, a 404 error is raised.
Check If Liked: The view checks if the user has already liked the post by filtering for a Like object. If no like is found,
it returns an error: 'you have not liked this post'
Notification Model
. Recipient:
recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications'):
This represents the user who will receive the notification. It's a foreign key to the CustomUser model.
Actor:
actor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='actor_notifications'):
This represents the user who performed the action
Verb:
verb = models.CharField(max_length=150):
This is a string that describes the action that triggered the notification. For example, this could be 'liked', 'followed',
or 'commented on'

Target (Generic Foreign Key):
The target is the object that the action was performed on This uses Django’s Generic ForeignKey
mechanism to allow the notification to refer to any model.
target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True):
This is a foreign key to Django’s ContentType model, which allows the target to be any model
target_object_id = models.PositiveIntegerField(blank=True, null=True):
This is the primary key (id) of the object being referred to
target = GenericForeignKey('target_content_type', 'target_object_id'):
Generic ForeignKey: The combination of target_content_type and target_object_id creates a Generic ForeignKey, which allows
the Notification model to point to instances of any model. This is how the target can be any object, like a post or comment.