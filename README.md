# trAIn

![](https://cdn.discordapp.com/attachments/1010348308587348088/1010759644274237511/unknown.png)

## TLDR;

Train is a simple mobile application that acts as an extension for your treadmill. It uses AI and pose detection to enhance your form and make you a better runner by providing real time feedback.


## Inspiration

I want to start with a personal story that become an inspiration for this project. Now, LOVE TO RUN. I put on my running shoes every day and head out the front door no matter the weather. But things were not always this way. In the beginning, running was supremely tough for me, and the reason for that comes down to one word, “form”. I was not running properly. I had the wrong posture, poor form and a lot of other small but important bad running habits. So, I had to face injuries, muscle pains and many other unpleasant phenomenon. Soon I realized that I am not the only one who faces this problem. There are over 50 million treadmill runners in the United States alone! But there are less than 5 thousand certified coaches across the whole country! That is one coach for every 12,500 runners! Although there were many apps that told me how far I should run each day, no app had the functionality to fix my poor running form. And proper form, is arguably the most important part of a successful run. This is where trAIn comes in! 

##  Introduction

Train is a simple mobile application that acts as an extension for your treadmill. It uses AI and pose detection to enhance your form and make you a better runner by providing real time feedback. (The capitalized “AI” in the logo actually stands for Artificial Intelligence). trAIn attaches to the handle of your treadmill and monitors your form in real-time. It uses pose detection to keep track of your movements and makes sure they are in-line with professionally set guidelines for better running form. It uses a voice coach to alert the user whenever his/her running form falters, this allows the users to receive instantaneous hands-free feedback and ensures that their running form is fixed immediately before it leads to further complications.

## Building Process

When I first built a prototype of the application, I saw very promising results as I imitated good and bad running postures in my bedroom. But that was not enough to quench my thirst. I wanted to test it in real world scenarios! So, I packed my laptop and headed out to the local gym. Now we got kicked out of the gym, because some noble soul called the security because we were filming. But, we didn't give up. We snuck in again and captured some rough but important footage of the early models performance. The data we got from doing the real-world tests further solidified my trust in the system. 

The voice coach worked well, and the lag was very low. But after making some additional tweaks to our model and rewriting a lot of code, we were able to make our package small enough to run on a modern smartphone without any hiccups! This means that trAIn can be converted into a mobile app which can be distributed very easily. Now, I didn't stop there. I worked through the night and further streamlined the model. 

I would also like to talk about the analysis section which is currently under development. Users can see pictures of their past mistakes and reflect on their running. This makes them less prone to making those same mistakes again.

## Under the Hood

Now that we have seen a demo, lets see what is under the hood. The pose detection is powered by mediapipe’s blazepoze model. I chose Mediapipe because it supports both integrated GPU and WebGL rendering. This makes it much faster than its fellow open source competitors. The frontend is powered by streamlit who relays the webcam feed via a very clever library called streamlit_webrtc. In the back, we use OpenCV for image processing and numpy for all the stuff involving math. Additional libraries like Pytorch and Matplotlib were used occasionally during prototyping. I mainly used functional programming to keep my project manageable and tried to use docstrings, comments and proper variable names to write quality code.

## Future Improvements

Moving on, lets talk about the improvements that can be made. First, there are some minor glitches involving managing threads between rendering and outputting the audio. Fixing this should reduce the jitter you see on screen and make the system a lot smoother. Secondly, we can measure the users breath rate remotely using only the camera! I came across [this](https://arxiv.org/pdf/2106.02669.pdf) paper, and it provides a really elegant way of accurately getting respiration rates using just a video feed. We can change our monitoring system based on level of fatigue detected and tell the user to decrease and increase pace as needed. And lastly, almost all exercises are built on the basis of repetitive movements with proper form. trAIn can easily be extended to account for various different activities to further increase its scope.

## Monetization

I’ll also talk briefly about monetization. We will have two main channels of generating revenue in the future. We will monetize trAIn by selling subscriptions to individual customers and we will sell bundled plans to gyms. Selling plans directly to gyms will allow us to reach a large audience by focusing on a few large businesses.

## Conclusion

To conclude, trAIn can revolutionize the way runners around the world train. It is a way to improve your running form in real time with a very small investment. It can expand in the future to incorporate other exercises as well. It has the ability to shake the 200-billion-dollar fitness industry. I believe that trAIn has immense potential and will be a successful product if it is further developed.


