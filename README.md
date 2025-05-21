# BUILDING AND SIMULATING FROM A COGNITIVE MODEL OF A PERSON USING PASSIVE BRAIN COMPUTER INTERFACES

What I am attempting here is to build a software system that can model what it is like to be a specific person interacting with a computer, or as ChatGPT put it, a subject-specific cognitive emulator. Given real-world data produced from passive BCI techniques that comprise of

•	Basic computer input streams 
  o	Keystrokes
  o	Cursor movements and clicks
•	visual representation of the user through the webcam
•	Screen Content
  o	Visual
  o	Auditory

all simultaneously captured, the ambitious me sets out two broad objectives for this project:

**A.	The learned moment-to-moment internal state of a user**

This project will be to construct a representation of the user’s state of mind over time. Broadly, the following characteristics will be computed.

1.	Working Memory
2.	Stress Level
3.	Attention
4.	Emotional State

A case can be made for fusing emotional state and stress level into a general affective state, but for now they will be kept distinct.
I believe it is possible to quantify each of the above characteristics, however, I am not sure as of yet what they will be. In any case, the reconstruction will then be cross-checked with the user’s own account of their state of mind over the same recorded period. Success will be measured in terms of how accurate the cognitive model developed is to the user’s own account, either mathematically or by qualitative judgement (it remains to be seen how exactly). Details on a precise metric will be determined later.

**B.	An artificial agent to simulate the user’s behavior from the user’s learned cognitive model**
Using existing automation and simulation tools, such as Selenium for browsers and AutoHotKey on Windows, the idea is to be able to use the cognitive model learned over the course of the user’s recorded sessions to simulate the user’s most likely actions and behaviors when performing any specific computer task. It is intended to be generalized and even transferable from one computer task to another.
This too can be represented in terms of some measured characteristics, like words per minute, cursor speed, temporal variation in actions, and more, which at this time is yet to be decided. Like objective A above, accuracy is ultimately determined if the simulations are believed to be accurate to the user’s recorded sessions.
We are in effect using a modified version of the Turing test as the metric for success of the cognitive modeling. It may be the case that we use statistical representations, human inquiry, or machine learning systems, or even a combination of any two or all of these to make a conclusive statement.
The guiding principle will be seeking results that are good enough, not necessarily perfect or even close to perfect. This consideration mainly stems from the reality that I will have limited computing resources to spare for this project, which quickly seems to be becoming computationally expensive.

**Requirements:**
* OBS - You MUST have OBS installed.
