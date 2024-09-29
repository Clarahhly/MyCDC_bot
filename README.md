# CDC Bot for Booking Driving Lessons

A little project I did for fun. This project automates the process of booking practical driving lessons on the Singapore CDC (ComfortDelGro Driving Centre) website. The bot uses Selenium, solves CAPTCHA challenges, and selects available sessions based on user-defined preferences for time and day. <br>
The bot can only reserve the slot for you. Reserved slots will only be held for 30 minutes. So keep a look out! (or you can connect it to a telebot to inform you when a slot is reserved)


## Prerequisites
* Python 3.x <br>
* selenium and undetected-chromedriver libraries <br>
* pickle for cookie management <br>
* CAPTCHA-solving service <br>
* An authentication proxy <br>

## Things to configure
1. In "save_cookies.py", add in your username and password
2. In "proxy.py", add your path which is the path to the chromedriver.exe and your proxy details (host and port etc)
   I've used a paid proxy, but you can choose not to use a proxy at all because unpaid proxies are quite dangerous to use.
4. In "solveRecaptcha.py", add in your 2Captcha API key (This is a paid service, but it's relatively cheap)
5. In "main.py", add in you preferred date and time that you want to book your slot in.

sorry there's a lot to configure in different places because I'm lazy to use a yaml file.

*You have to run save_cookies once first before you run main.

## Disclaimer⚠️
Since I did this project for fun and it works on my end, I'm not planning to maintain it or fix anything if there is a bug.
