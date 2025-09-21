# Agentic Travel Assistant [WIP]

Travel chatbot that leverages an agentic framework to answer questions about US attraction places and book flights in the US.

This is a "remake" project of a travel chatbot assistant I made early in my career where I leveraged rigid intents for routing chatbot conversations.

## Concept

- A digital assistant helping users answer questions about US tourism attractions
- Provide users on flight information and assist in flight ticket bookings.

## Scope

- Queries about tourist attractions and flights are limit in US locations.

## Data

- Kaggle: Global Tourist Hotspot: [Link](https://www.kaggle.com/datasets/maedemaftouni/global-tourist-hotspots-us-india-iran)
- Air flight API: TBD

## Agentic System
- Q&A agent - responsible for answer general questions on US tourist hotspot locations. 
- Flight agent - responsible for retrieving information on US flights via tool-call on flight API.
- Booking agent - responsible for adding/removing flight bookings.