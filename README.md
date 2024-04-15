# Wikipedia Race Game with Claude-3 Haiku Agent System
This project utilizes a Claude-3 Haiku agent system to solve the Wikipedia race game. The Wikipedia race is a game where players start from a random Wikipedia page and navigate through the links to reach a predetermined target page. The objective is to reach the target page using the fewest number of links.

# Requirements
To run this project, you need an Anthropic API key and python >= 3.8.

Use this link to setup your Anthropic API key if you do not have one yet: https://console.anthropic.com/dashboard

You can install the required Python packages by running the following command:

```
pip install -r requirements.txt
```

# Setup
Clone this repository to your local machine.
Create a .env file in the project directory and add your Anthropic API key in the following format:

```
ANTHROPIC_API_KEY=your_api_key_here
```

Replace your_api_key_here with your actual Anthropic API key.

# Usage
To play the Wikipedia race game using the Claude-3 Haiku agent system, follow these steps:

- Open a terminal and navigate to the project directory.
- Run the Streamlit application by executing the following command:

```
streamlit run src/streamlit.py
```

The Streamlit application will open in your default web browser.
Follow the instructions provided in the Streamlit interface to play the game.

# Notebooks
This project includes two Jupyter notebooks that demonstrate the functionality of the Claude-3 Haiku agent system:

- easy_mode.ipynb: This notebook showcases the Wikipedia race game with a fixed target page, which is the "United States" page. It provides a step-by-step walkthrough of how the agent system navigates from a random starting page to the target page.
- hard_mode.ipynb: This notebook demonstrates a more challenging version of the Wikipedia race game, where both the starting page and the target page are randomly selected. It showcases the agent system's ability to navigate through Wikipedia links to reach the target page efficiently.

Feel free to explore these notebooks to gain a better understanding of how the Claude-3 Haiku agent system works and how it solves the Wikipedia race game.

# Contributing
If you would like to contribute to this project, please follow these steps:
- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and commit them with descriptive commit messages.
- Push your changes to your forked repository.
- Submit a pull request to the main repository, explaining your changes and their benefits.

# License
This project is licensed under the MIT License.

# Acknowledgments
- Claude-3 is developed by Anthropic.
- The Wikipedia race game concept is inspired by the popular online game.
