# 📠 Paragraph 1.1 - Django texting.
> Simplified texting and media sharing app built with django

---

[Website](https://myparagraph.space)
<br>
[Android App](https://github.com/coleblvck/paragraph-for-android)
<br>
[Web App](https://web.myparagraph.space)

---

# Features:

- Texting (Live or not, you can implement this however you like)
- Search and view profiles, add friends, unfriend and block (You can only text friends)
- Get a list of friend requests, sent requests and blocked users
- No history texting (Previous message is deleted as new one is sent)
- Note keeping and sharing in a status-like manner
- Media sharing in the same manner as the texting (one file at a time)
- Manually notify your friend if you wish to get their attention
- Live mode


# 📓 Some Important Notes:

- This is not a representation of Django best practices, as it was written for prototyping purposes.
- I have tried implementing subscriptions on this project with little to no success, (with the little succes, it was not reliable for my use case so I stuck with querying in a specific interval for this purpose. So, suggestions are very welcome).
- Currently making major refactoring changes in order to federate this app, so future updates may be in a completely different repo.


# Deployment:

You can deploy this app with various options such as: UVICORN with GUNICORN(For asgi deployment especially if you choose to implement subscriptions) or UWSGI.
