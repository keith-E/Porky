# Porky: The Real-Time Object Detecting Robot
The goal of this project is to demonstrate how to create a real-time object detection autonomous robot with relatively inexpensive components. By training your own Machine Learning model and pairing Intel's Neural Compute Stick 2 with a Raspberry Pi 3 B+, you'll be able jumpstart your next real-time object detection project! 

TODO: pictures and gif of robot in action

## Table of Contents
* [Project Overview](#project-overview)
* [Update History](#update-history)
* [Hardware List](#hardware-list)
  * [Required Hardware](#required-hardware)
  * [Optional Hardware](#optional-hardware)
* [Hardware Configuration](#hardware-configuration)
  * [Image Capturing Setup](#image-capturing-setup)
  * [Tweak and Test Setup](#tweak-and-test-setup)
  * [Live Deployment Setup](#live-deployment-setup)
* [Train Object Detection Model with TensorFlow](#train-object-detection-model-with-tensorflow)
* [Optimize Model for Intel Neural Compute Stick 2](#optimize-model-for-intel-neural-compute-stick-2)
  * [Install OpenVINO on Dev PC](#install-openvino-on-dev-pc)
* [Deploy the Optimized Model](#deploy-the-optimized-model)
  * [Install Raspberian on Raspberry Pi](#install-raspberian-on-raspberry-pi)
  * [Install OpenVINO on Raspberry Pi](#install-openvino-on-raspberry-pi)
  * [Clone this Repository](#clone-this-repository)
* [Testing](#testing)
* [Deploy the Robot](#deploy-the-robot)
* [Feedback Statement](#feedback-statement)
* [References and Acknowledgements](#references-and-acknowledgements)

## Update History
**2019/05/09:** Initial Release

## Project Overview
This guide will teach you how to: 
* Train your own model in TensorFlow using a Transfer Learning technique to save time and money 
* Optimize the resulting TensorFlow model to be utilized with Intel's Inference Engine
* Implement the optimized model into a Python script
* Deploy the program with real-time performance and feedback loops

## Hardware List
While some of the hardware in this section is described as 'Required' or 'Optional', this is only if you want to follow this guide step-by-step. This does not mean you are restricted to these components if you want to swap, subtract, or add components. However, for the best initial results (if your intention is to follow this guide), I highly suggest acquiring the components within the 'Required Hardware' section at the very least. This will enable you to train a Machine Learning model and perform Real-Time Object Detection. My personal favorite sites for finding components for robotic projects are [Adafruit](https://www.adafruit.com/), [RobotShop](https://www.robotshop.com/), and [eBay](https://www.ebay.com/) (useful for scoring great deals on used parts). The possibilities are endless!

#### Required Hardware
* **Raspberry Pi 3 B+** w/ MicroSD Card and a way to power the device (battery or AC wall adapter)
* **Intel Neural Compute Stick 2 (NCS2)**
* **USB or Pi Camera** This project uses the [PS3 Eye Camera](https://en.wikipedia.org/wiki/PlayStation_Eye) which can be found on eBay for about $6 USD each.

#### Optional Hardware
TODO: clean and add links
* **Robot Chassis Kit w/ Motors** This project uses the [Lynxmotion 4WD1 Rover Kit](http://www.lynxmotion.com/c-111-a4wd1-no-electronics.aspx). You can purchase this kit directly from [RobotShop](https://www.robotshop.com) or find a used kit on eBay.
* **Servos x2 w/ Mounting Hardware** This project uses the [Lynxmotion Pan and Tilt Kit](https://www.robotshop.com/en/lynxmotion-pan-and-tilt-kit-aluminium2.html).
* **PWM Controller**
* **Mounting Hardware** Please refer to the [Optional Hardware](#optional-hardware) section for the list of mounting hardware this project uses.
* **Assorted Electrical Components (switches, buttons, wires, etc)** Check out [Adafruit](https://www.adafruit.com/) for great deals and tutorials on anything electrical.
* **Power Delivery Devices (Batteries/AC Adapters)** Please refer to the [Optional Hardware](#optional-hardware) section for the list of power delivery devices this project uses.
* **Development PC (Linux, Windows, MacOS)** Development for this project was performed on a Windows 10 platform.
* **Display Monitor w/ HDMI Output** Helpful for debugging and testing within Raspberry Pi environment.
* **Arduino Uno3**
* **Electrical Tape**
* **Small Rig Mounting Arm** TODO: Needs link
* **iFixit Toolkit** TODO: Needs link
* **Velcro Tape (for modular prototype mounting)** TODO: Needs link
* **Breadboards for Prototyping**

## Hardware Configuration
The wiring diagrams contained within this section were created with [Fritzing](http://fritzing.org/home/), a fantastic open-source tool.

#### Image Capturing Setup
To train your own Machine Learning model, you will need to gather the data to train and validate your model on. The idea for this project was to train the model based on images captured with an identical camera that was eventually going to be deployed live.

This setup consists of:
* **Raspberry Pi 3 B+** w/ MicroSD Card and a way to power the device (battery or AC wall adapter)
* **PS3 Eye USB Camera** TODO: provide a link to ebay search
* **Portable Powerbank** TODO: update this name and link
* **Mini Button** TODO: provide a link to adafruit buttons
* **Breadboard** TODO: provide a link to adafruit breadboards
* **2 Female to Male Wires** TODO: provide a link to adafruit wires

Please see the [Capture Images with the Image Capturing Setup](#capture-images-with-the-capturing-setup) section to capture your own images for your dataset using this hardware configuration.

#### Tweak and Test Setup
This hardware configuration serves the purpose for testing your hardware components (motors, servos, etc) and software integrations (debugging, testing, sandbox). This setup is geared towards using AC wall adapters to save batteries and keeping moving components as stationary as possible. Having a proper testing setup can potentially save lots of frustration and money. It is strongly suggested to test your own project before deploying it into the wild.

#### Live Deployment Setup
After performing adequate hardware and software tests, you'll be ready to release your autonomous robot without its leash. This section will show you how to configure your robot to be deployed live. 

## Train Object Detection Model with TensorFlow
The goal of this section is to use TensorFlow to train your custom model using Transfer Learning. While creating your own Machine Learning model can be extremely rewarding, that process typically involves much configuration, troubleshooting, and training/validating time. A very costly process. However, with Transfer Learning, you can minimize all three fronts by choosing an already proven model to customize with your own dataset.

#### Create Your Dataset

###### Capture Images with the [Image Capturing Setup](#image-capturing-setup)

###### Label the Captured Images with LabelIMG

#### Install the TensorFlow Framework onto Dev PC

#### Convert the Images and Annotations into TFRecord Format

#### Pick an Already Trained Model and Use Transfer Learning

#### Deploy the TensorFlow Training Session

##### Using Google Cloud for Machine Learning

#### Extract the Trained Model

## Optimize Model for Intel Neural Compute Stick 2

#### Install OpenVINO on Dev PC

## Deploy the Optimized Model

#### Install Raspberian on Raspberry Pi

#### Install OpenVINO on Raspberry Pi

#### Clone this Repository

## Testing
During the lifecycle of your robot project, it's a good idea to develop and maintain some sort of testing strategy. In this section, I will break down how to use the provided testing scripts and their purpose.
#### Hardware Specific Tests
###### Test the Camera
###### Test the Motors
###### Test the Servos

#### Unit Tests
###### Test the ML Model
###### Test the Camera Process
###### Test the Detection Process

#### Integration Tests
###### Test Detection with Pan and Tilt
###### Test Detection with Pan and Follow

## Deploy the Robot

## Feedback Statement
I tried my best to detail all of the processes I used to get this project off the ground, but I may have missed some key steps along the way or you may have experienced some frustrations trying to follow along. With that being said, please don't hesitate to drop me any comments, questions or concerns. I promise to do my best to address your issues.

TODO: add contact links

## References and Acknowledgements
**[leswright1977/Rpi3_NCS2](https://github.com/leswright1977/RPi3_NCS2):** leswright1977's bottle-chasing robot introduced me to the Intel NCS2 and its ability to integrate machine learning models for real-time applications.

**[PINTO0309](https://github.com/PINTO0309):** PINTO0309's [MobileNet-SSD-RealSense](https://github.com/PINTO0309/MobileNet-SSD-RealSense) project provided a ton of inspiration for this project especially for the use of hardware choices and multiprocessing in Python to optimize performance.

**[OpenCV Docs](https://docs.opencv.org/):** The official documentation for OpenCV. Necessary for gaining a strong foundation of using OpenCV to build your application.

**[Adafruit Pixy Pet Robot](https://learn.adafruit.com/pixy-pet-robot-color-vision-follower-using-pixycam/overview):** Adafruit's guide on creating color vision following robot using a Pixy CMUCam-5 vision system and Zumo robot platform. This guide was very helpful for learning how to integrate a PID (Proportional-Integral-Deravitive) control feedback loop for the motion mechanisms.
