# AIChat
simple ai bot for Discord. 

## Instructions (for Render hosting)

1. Fork this repo
2. Go to the Discord Developer Portal for making bots (https://discord.com/developers/applications)
3. Click on "New app"
4. Click on "Bot" in the sidebar
5. Enable All gateway intents
6. Scroll down to "Bot permissions"
7. Click the following bot permissions: Send messages, Incorporate links, Attach files and Read chat history.
8. Go to the OAuth section in the sidebar
9. Scroll to "OAuth URL generator"
10. Check "bot"
11. Check all bot permission in 7
12. go to dashboard.render.com
13. Click "New"
14. Click "Web Service"
15. select the AIChat repo
16. configure (Build command: ./ $ pip install -r requirements.txt, Start command: leave blank)
17. scroll to "Enviorment Variables"
18. Add these ENVs: GEMINI_API_KEY, DISCORD_TOKEN
19. Click "Deploy Web service"
20. go back to Discord Dev Dashboard
21. Go to the link generator at the bottom
22. Copy it and paste it in a web browser
23. Link the app to your discord account and choose a server
24. Done!

Known issues:
incompatible with IBM PC's


