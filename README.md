# Flappy Bird AI: Genetic Algorithm
Application of the Genetic Algorithm to the game Flappy Bird.

## Configuration

### What the Bird can see:
- Distance to the front of the next pipe.
- Own vertical velocity.
- Vertical distance to the end of the top and bottom pipes (2 values).

### What the Bird can do:
Every frame the bird can either jump or not jump.

### Neural Network Structure:
There are 4 input nodes, 1 output node with sigmoid activation (activation > 0.5 => jump, otherwise don't jump) and no hidden layers.

### Fitness Function:
The number of frames the bird has been alive for.

### Results:
Ultimately Flappy Bird is a very simple game and is easily beaten by the Genetic Algorithm. Here is a group created in generation 5 passing the 1000 mark:

![Birds passing 1000](https://i.imgur.com/KgvvAJR.gif)

Seeing as the game does not increase in difficulty as score increases, they would keep going on forever if you let them.

## If you want to run it yourself

### Basic Requirements:
1. [Python](https://www.python.org/downloads/).
2. [Poetry](https://python-poetry.org/docs/) for ease of installing the dependencies.

### Getting Started:
1. Clone or download the repo `git clone https://github.com/RJW20/flappy_bird_ai_genetic_algorithm.git`.
2. Download the submodules `git submodule update --init`.
3. Set up the virtual environment `poetry install`.
4. Enter the virtual environment `poetry shell`.

### Running the Algorithm:
1. Change any settings you want in `flappy_bird_ai/settings.py`. For more information on what they control see [here](https://github.com/RJW20/genetic_algorithm_template/blob/main/README.md). 
2. Run the algorithm `poetry run main`.
3. View the playback of saved history with `poetry run playback`. You can change the generation shown with the left/right arrow keys and increase or slow-down the playback speed with the k/j keys respectively.
