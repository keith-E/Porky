# Porky: The Real-Time Object Detecting Robot
The goal of this project is to demonstrate how to create a real-time object detection autonomous robot with relatively inexpensive components. By training your own Machine Learning model and pairing Intel's Neural Compute Stick 2 with a Raspberry Pi 3 B+, you'll be able jumpstart your next real-time object detection project! 

TODO: pictures and gif of robot in action

## Table of Contents
* [Project Overview](#project-overview)
* [Hardware List](#hardware-list)
  * [Required Hardware](#required-hardware)
  * [Optional Hardware](#optional-hardware)
* [Hardware Configuration](#hardware-configuration)
  * [Image Capturing Setup](#image-capturing-setup)
  * [Tweak and Test Setup](#tweak-and-test-setup)
  * [Live Deployment Setup](#live-deployment-setup)
* [Train ML Model with TensorFlow](#train-object-detection-model-with-tensorflow)
* [Optimize Model for Intel Neural Compute Stick 2](#optimize-model-for-intel-neural-compute-stick-2)
  * [Install OpenVINO on Dev PC](#install-openvino-on-dev-pc)
* [Deploy the Optimized Model](#deploy-the-optimized-model)
  * [Install Raspberian on Raspberry Pi](#install-raspberian-on-raspberry-pi)
  * [Install OpenVINO on Raspberry Pi](#install-openvino-on-raspberry-pi)
  * [Clone this Repository](#clone-this-repository)
* [Testing](#testing)
* [Deploy the Robot](#deploy-the-robot)
* [References and Acknowledgements](#references-and-acknowledgements)

## Project Overview
This guide will teach you how to: 
* Train your own model in TensorFlow using a Transfer Learning technique to save time and money 
* Optimize the resulting TensorFlow model to be utilized with Intel's Inference Engine
* Implement the optimized model into a Python script
* Deploy the program with real-time performance and feedback loops

## Hardware List
While some of the hardware in this section is described as 'Required' or 'Optional', this is only if you want to follow this guide step-by-step. This does not mean you are restricted to these components if you want to swap, subtract, or add components. However, for the best initial results (if your intention is to follow this guide), I highly suggest acquiring the components within the 'Required Hardware' section at the very least. This will enable you to train a Machine Learning model and perform Real-Time Object Detection. My personal favorite sites for finding components for robotic projects are [Adafruit](https://www.adafruit.com/), [RobotShop](https://www.robotshop.com/), and [eBay](https://www.ebay.com/) (useful for scoring great deals on used parts). The possibilities are endless!

#### Required Hardware
* **Raspberry Pi 3 B+**
* **MicroSD Card for Raspberry Pi**
* **Intel Neural Compute Stick 2 (NCS2)**
* **USB or Pi Camera** This project uses the [PS3 Eye Camera](https://en.wikipedia.org/wiki/PlayStation_Eye) which can be found on eBay for about $6 USD each.
* **Robot Chassis Kit w/ Motors** This project uses the [Lynxmotion 4WD1 Rover Kit](http://www.lynxmotion.com/c-111-a4wd1-no-electronics.aspx). You can purchase this kit directly from [RobotShop](https://www.robotshop.com) or find a used kit on eBay.
* **Servos x2 w/ Mounting Hardware** This project uses the [Lynxmotion Pan and Tilt Kit](https://www.robotshop.com/en/lynxmotion-pan-and-tilt-kit-aluminium2.html).
* **PWM Controller**
* **Mounting Hardware** Please refer to the [Optional Hardware](#optional-hardware) section for the list of mounting hardware this project uses.
* **Assorted Electrical Components (switches, buttons, wires, etc)** Check out [Adafruit](https://www.adafruit.com/) for great deals and tutorials on anything electrical.
* **Power Delivery Devices (Batteries/AC Adapters)** Please refer to the [Optional Hardware](#optional-hardware) section for the list of power delivery devices this project uses.

#### Optional Hardware
TODO: clean and add links
* **Development PC (Linux, Windows, MacOS)** Development for this project was performed on a Windows 10 platform.
* **Display Monitor w/ HDMI Output** Helpful for debugging and testing within Raspberry Pi environment.
* **Arduino Uno3**
* **Electrical Tape**
* **Small Rig Mounting Arm** TODO: Needs link
* **iFixit Toolkit** TODO: Needs link
* **Velcro Tape (for modular prototype mounting)** TODO: Needs link
* **Breadboards for Prototyping**

## Hardware Configuration

#### Image Capturing Setup

#### Tweak and Test Setup

#### Live Deployment Setup

## Train Object Detection Model with TensorFlow

#### Install the TensorFlow Framework onto Dev PC

#### Label the Captured Images with LabelIMG

#### Convert the Images and Annotations into TFRecord Format

#### Pick an Already Trained Model to Perform Transfer Learning On

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

## References and Acknowledgements
