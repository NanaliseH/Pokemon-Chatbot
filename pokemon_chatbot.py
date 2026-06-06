# -*- coding: utf-8 -*-
"""
Created on April 27, 2026

@author: nan
"""

import re
import random

# Chatbot name
botID = "Pokémon Battle Bot: "

# Greeting and response messages
initialGreeting = (
    "Hello! I am a Pokémon Battle Bot. "
    "I can give information about Gen 1 Pokémon, including their type, strengths, and weaknesses. "
    "I can also compare two Pokémon and predict who would have the advantage. "
    "To ask about one Pokémon, type the name, like 'pikachu'. "
    "To compare two Pokémon, type them like 'pikachu vs squirtle'. "
    "Type 'quit' when you are done."
)

normalResponse = "Which Pokémon would you like to learn about or compare?"
confusedResponse = "I did not understand that Pokémon. Please try again."

greetings = ["hello", "hi", "hey", "greetings", "sup", "what's up", "howdy"]
greetingResponses = [
    "Hello Trainer! You can type a Pokémon name or compare two Pokémon using 'vs'.",
    "Hey there! Try something like 'pikachu' or 'charizard vs blastoise'.",
    "Hi! I can show Pokémon info or predict a battle winner."
]

thanks = ["thanks", "thank you", "cool", "awesome"]
welcomeResponse = "You are very welcome."

goodbyes = ["bye", "goodbye", "later", "cya", "quit", "exit"]
goodbyeResponse = "Goodbye Trainer! See you next battle!"

# Dictionary to store Pokémon data
pokemon_data = {}

# Read Pokémon data from file
with open("/Users/nan/Desktop/Spring 2026/Math4320/chatbot miniproject/pokemon_datafile.txt", "r", encoding="utf-8") as file:
    for line in file:
        if line.strip() == "":
            continue

        parts = line.strip().split(";")

        name = parts[0].strip().lower()
        poke_type = parts[1].strip()
        weaknesses = [w.strip() for w in parts[2].split(",")]
        strengths = [s.strip() for s in parts[3].split(",")]

        pokemon_data[name] = {
            "type": poke_type,
            "weaknesses": weaknesses,
            "strengths": strengths
        }


# Check for greeting
def greeting(sentence):
    for word in sentence.lower().split():
        if word in greetings:
            return random.choice(greetingResponses)


# Show Pokémon info
def pokemon_info(name):
    name = name.strip().lower()

    if name in pokemon_data:
        info = pokemon_data[name]

        return (
            f"Pokémon: {name.title()}\n"
            f"Type: {info['type']}\n"
            f"Weaknesses: {', '.join(info['weaknesses'])}\n"
            f"Strengths: {', '.join(info['strengths'])}"
        )
    else:
        return confusedResponse


# Predict battle winner
def battle(pokemon1, pokemon2):
    p1 = pokemon1.strip().lower()
    p2 = pokemon2.strip().lower()

    if p1 not in pokemon_data or p2 not in pokemon_data:
        return "One or both Pokémon were not found. Please check the spelling."

    p1_type = pokemon_data[p1]["type"].split("/")[0]
    p2_type = pokemon_data[p2]["type"].split("/")[0]

    p1_strengths = pokemon_data[p1]["strengths"]
    p2_strengths = pokemon_data[p2]["strengths"]

    if p2_type in p1_strengths:
        return (
            f"Battle: {p1.title()} vs {p2.title()}\n"
            f"Winner: {p1.title()}\n"
            f"Reason: {p1_type} is strong against {p2_type}."
        )

    elif p1_type in p2_strengths:
        return (
            f"Battle: {p1.title()} vs {p2.title()}\n"
            f"Winner: {p2.title()}\n"
            f"Reason: {p2_type} is strong against {p1_type}."
        )

    else:
        return (
            f"Battle: {p1.title()} vs {p2.title()}\n"
            f"Result: It is too close to call based on type advantage."
        )


# File input and output section
results = []

with open("/Users/nan/Desktop/Spring 2026/Math4320/chatbot miniproject/Pokemon_questions.txt", "r", encoding="utf-8") as file:
    questions = file.readlines()

for question in questions:
    question = question.strip()
    question = question.replace(">>>", "").replace("...", "").strip()

    if question == "":
        continue

    if "vs" in question.lower():
        pokemon1, pokemon2 = re.split(r"\s+vs\s+", question, flags=re.IGNORECASE)
        results.append(battle(pokemon1, pokemon2))
    else:
        results.append(pokemon_info(question))

with open("/Users/nan/Desktop/Spring 2026/Math4320/chatbot miniproject/pokemon_results.txt", "w", encoding="utf-8") as file:
    for result in results:
        file.write(result + "\n\n")


# Live chatbot section
flag = True

print("\n\n" + botID + initialGreeting)
print("\n" + botID + normalResponse)

while flag == True:
    user_response = input(">>> ").strip()

    cleaned_response = user_response.lower()

    if cleaned_response in goodbyes:
        flag = False
        print(botID + goodbyeResponse)

    elif cleaned_response in thanks:
        print(botID + welcomeResponse)

    elif greeting(user_response) is not None:
        print(botID + greeting(user_response))

    elif "vs" in cleaned_response:
        try:
            pokemon1, pokemon2 = re.split(r"\s+vs\s+", user_response, flags=re.IGNORECASE)
            print(botID + battle(pokemon1, pokemon2))
        except:
            print(botID + "Please compare Pokémon using this format: pikachu vs squirtle")

    else:
        print(botID + pokemon_info(user_response))
