# Instructions

To start the training of the good-fake ml model you need to go through some steps.

## Setting up Keras
The Keras code is running Tensorflow as a backend. You need to fist setup tensorflow (preferably with the GPU support).

The information is here: https://www.tensorflow.org/install/

For GPU support you need a recent Nvida Graphics Card. The code in this repository was trained with a 1060GTX.

## Getting the data
Setup the data folder in the following way:
make a training and validation folder in the data folder.
Make a good, fake and normal folder in both the training and validation folder.

The trainer needs the images to be 455 width and 700 height. You can do this preprocessing with the img.py file. Make sure to adjust the folders in this code (line 6 and 7) to your own PC file structure. When you have done this you also need to adjust line 15 and 16 to the amount of images you put in total.

## Running the trainer
Run the train.py file. It should run for 70 epochs and get around 91% accuracy.
If you want Tensorboard support the logs are in the main folder.