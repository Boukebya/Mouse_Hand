# Mouse_Hand

Our project aims to learn how to create a computer vision model and train it on our own database to use a mouse with the webcam of a laptop.


We are using MediaPipe and MediaPipe-model-maker to use Google tools to create our model.
The project is working on Linux only due MediaPipe-model-maker not working on windows.
We train the model to recognize three hand gestures by creating a dataset of the gesture in differents light conditions and movement to use them to simulate right click, left click and mous movement.


Mouse movement : move your hand in front of the webcam.
Left click : index to thumb.
Right click : middle finger to thumb.
