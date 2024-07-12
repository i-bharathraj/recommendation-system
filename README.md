# Voice Assistant - MyJarvis
My kind of Voice Assistant leveraging Meta's LLaMA3 large language model (LLM)

**Overview**

This repository includes a complicated Python program that uses the Ollama Python Library and the Meta Llama 3 model to respond to user queries by turning text responses into audio. 

Trust me! This implementation has been tested and worked on WIndows 11. 

**GPU Compatibility**

Please check this list of supported graphics cards to make sure Ollama supports your GPU. A compute capability of five or more should be available on your GPU. An 8GB VRAM GPU is advised for best results with the 7B large language model.

**Installation Instructions 
**
**1. Ollama Installation
**
- Download and install the Ollama from the official website. 
- Download the Meta Llama3 model, you can use the following command to do that:

```ollama pull llama3```

**2. Running Ollama
**
- Once you download the package, start the Ollama service and then use the Llama 3 model in your own python program. 

```ollama serve```

- In case, if you wanna use a different Large Language Model like Llama2 or something else, you still can pull the similar one and then modify the code accordingly. 

**3. Python - Package Installation
**
- Before running this code, make sure that the python packages have been installed: 

```pip install ollama ```
```pip install speechrecognition gtts pyaudio pygame ```

- For Python 3.12 or any other newer versions, install the 'setuptools' package as well. 

```pip install setuptools ```

- You also may need to create a Python Virtual environment before installing all these packages. 

Once done, Enjoy!

Lol, you will now be able to deploy and then operate the Meta Llama3 based voice assistant however you need. 

