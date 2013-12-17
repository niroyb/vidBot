# vidBot

## What is vidBot?
This is the source code for a Reddit bot that adds information to video links.

## But why?
Often video links are used with little context and may result in a risky click.  
Users can decide if the video is worth watching based on the added information.

## How does it work?
- vidBot searches for comments containing his name and a links.
- If no url is found, he will try to use the submission link.
- He will then answer with the formatted video information.

## Requisites
* [Python 2.7](http://www.python.org/download/)
* The latest version of praw (available via pip)
* youtube-dl (available via pip)

## Configuration
- Copy the file `config_sample.cfg` to `config_real.cfg`.
- Follow the directions within the config to setup the new bot.

## License
The bot is licensed under GPL v3 with the following stipulations. Please view the license file in docs/LICENSE

## Acknowledgments
Based on the work of [JiffyBot](https://github.com/l1am9111/JiffyBot), by Nathan Hakkakzadeh and John O'Reilly