# Django Social Network

This is an educational **django v4**  project from Mongard course.
In this app you can register, login (by username or email)  and logout.
After login, you can see all post created by other users.In your profile, yourusername and your own posts are shown too.

## Some Implementation Details
After login you can see your profile as well as other users profiles in this social network.
For better implementation we use Class Based View.Admin pannel was costumized for showing posts.
Also frontend improved by **Bootstrap**
confirming pasword was done by overwriting clean() validator
using get_absolute_url instead of {%url%}template tag.
