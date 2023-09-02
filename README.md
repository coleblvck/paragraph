# 📠 Paragraph 1.1 - Django texting.
> Simplified texting and media sharing app built with django

# Features

---

- Texting (Live or not, you can implement this however you like)
- Search and view profiles, add friends, unfriend and block (You can only text friends)
- Get a list of friend requests, sent requests and blocked users
- No history texting (Previous message is deleted as new one is sent)
- Note keeping and sharing in a status-like manner
- Media sharing in the same manner as the texting (one file at a time)
- Manually notify your friend if you wish to get their attention
- Live mode


# 📓 Some Important Notes:

---

- The frontend (web browser aspect) has been disconnected from the URLs in favour of GraphQL api
- This is not a representation of Django best practices, as it was written for prototyping purposes.
- If you'd wish to use this; You'd have to Iron out some implementations using your preferred methods for some features such as the live mode; as I built this with a corresponding mobile app which shares the user's now-playing audio with friends.
- GraphQL subscriptions can be implemented for live texting (I tried doing this, it was not reliable for my use case so I stuck with querying in a specific interval for this purpose)


# Deployment:

---

You can deploy this app with various options such as: UVICORN with GUNICORN(For asgi deployment especially if you choose to implement subscriptions) or UWSGI.
