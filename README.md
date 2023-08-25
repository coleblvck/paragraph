# Paragraph
> Simplified texting and media sharing app built with django

## Features

- Texting (Live or not, you can implement this however you like)
- Search and view profiles, add friends, unfriend and block (You can only text friends)
- Get a list of friend requests, sent requests and blocked users
- No history texting (Previous message is deleted as new one is sent)
- Note keeping and sharing in a status-like manner
- Media sharing in the same manner as the texting (one file at a time)
- Manually notify your friend if you wish to get their attention
- Live mode

## Note:
- You'd have to figure out the implementations for some features in your own way such as the live mode; as I built this with a corresponding mobile app which shares the user's now-playing audio with friends.
- If you wish to run this for yourself, you an implement GraphQL subscriptions for live texting (I tried doing this, it was not reliable for my use case so I stuck with querying in a specific interval for this purpose)
