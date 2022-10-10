from django.urls import path

from brewwerconnections.views import(
    send_friend_request,
    friend_requests,
    accept_friend_request,
    remove_friend,
    decline_friend_request,
    cancel_friend_request,
    friends_list_view,
)


urlpatterns = [
    path('list/<user_id>', friends_list_view, name='list'),

    path ('friend_remove/',remove_friend,name="remove-friend"),
    path ('friend_request/',send_friend_request,name="friend-request"),
    path ('friend_request/<user_id>',friend_requests,name="friend-requests"),
    path ('accept_friend_request/<friend_request_id>',accept_friend_request ,name="friend-requests-accept"),
    path('friend_request_decline/<friend_request_id>/', decline_friend_request, name='friend-request-decline'),
    path('friend_request_cancel/', cancel_friend_request, name='friend-request-cancel'),


]