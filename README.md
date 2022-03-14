# jiro-the-sushi-bot
A virtual assistant that recommends sushi to the user.

Introduction

Sushi is perhaps the most famous Japanese food in the world. It can be a flavorful, delightful experience. But if you have not had much sushi in your life, you may not be aware of dishes or styles that exist that you may wish to try. Or maybe you may have questions about why or how that tuna you are eating is able to maintain its bright red color or whether there are any vegetarian/vegan alternatives available. 

Goal

The focus for this report was to create a dialog system that can answer common questions about sushi as well as provide sushi recommendations based on descriptions provided by the user with a chatbot dialog system using a BestMatch logic adapter and a recommendation system using content-based, collaborative, and popularity filtering. 

Dataset

The data set by Kamishima, https://www.kamishima.net/sushi/is a survey of 100 types of sushi answered by 50000 people who ranked their 10 favorite types of sushi. 

Implementation

The sushi bot is composed of two py files: The Recommender_Core and Jiro_Bot.

A. Recommender_Core:

The recommender_core was created by first importing Pandas, Surprise, and Sklearn. Matplotlib was also imported to conserve processing speed of numerical data.
Next, the preprocessed data was imported. The data consisted of a survey of 100 types of sushi answered by 50000 people ranking their 10 favorite sushi types. The data was preprocessed by first reorganizing the data so that it reflected an order from most liked to 10th in rank. User IDs were then added for those who participated in the survey. The user IDs were arbitrarily large numbers so that they were not a risk of interfering with the data. 
It was decided that the sushi data be kept as numerical data instead of abstract data to save on processing speed.
A file was added where the data is organized the by user ranking where each user put their sushi rankings one after the other. This is also done in later algorithms (Hug, N., “Surprise Documentation”, https://surprise.readthedocs.io/en/stable/getting_started.html.
Excel was used to count the total instances of each sushi appearing in the top 10 and put it into a column. 

B. Jiro_Bot

The Jiro_Bot was created by first installing Chatterbot, then importing Chatbot. An SQL storage adapter was implemented to allow the chat bot to connect to SQL databases.
Logic adapters were then added. The adapters used in this project were MathematicalEvaluation and BestFit. A while loop was made to illicit a response from the chatbot.

Chatterbot comes with its own training regimen accessed through the ChatterbotCorpusTrainer module. With this module, we can “teach” our chatbot how to respond to different prompts based on logic adapters and filters. The two corpuses used sushi.yml and sushi_descriptions.yml. To train the chatbot you need to create the words where you will store the pattern words that share characteristics from the lemmatized words. There is a base word that represents all the other related words in the bag. Every word is compared to the bag with the base word, and if it matches it will be added to the pattern. From those bags, you create a training array that can be used to make a model.
A command of good will prompt a command for a sushi name if the sushi is in the list, then the second functionality of the core will activate.
A command of like will bring our SVD recommender and predict sushi likes [6]. Ideally this would run an analysis on all the user’s previous sushi preferences and recommend a new sushi based on the community profile. For now, we run the prediction on a single sushi for new user. For the future, this function would look at the estimated score and respond appropriately with “I think you’ll like this”, or “I don’t think you’ll like this” when asked about a specific sushi, eg: 

User: Would I like the egg sushi?

Jiro: No, I do not think you will.

Jiro_Bot is a simple virtual assistant with a rudimentary ai based on if/then statements. Jiro_Bot’s main purpose is to vocalize the information from the previous two modules. However, Jiro_Bot can be modified to include or exclude more functionality. Currently Jiro bot can google search and search on Youtube. Jiro_ Bot functions using the speech recognition and gTTS (google text-to-speech) Python libraries included by default.
