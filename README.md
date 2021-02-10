# discordBot
a Bot for managing various discord tasks

Some required packages for this bot:
    Discord
    Discord-Anti-Spam

This bot has a recurring daily task set for the time between 0900 to 0959 checking for
a completed Daily Health Task that is localized to RIT. This is paired to the 
dailyHealthBot repo I also have on my account.

There are some cool functionalities of this bot. 
The default trigger command is '~'

Status Update:
    This app will update the status of the bot to a series of keywords that are
    determined by the day of the week

Help:
    Custom help message that is separated into tiers.

    Example:
    Usage:
    ~help [monke/joker/horny/todo]

    These help files are stored under help/ dir

    TODO HELP:
    Usage:
        ~todo [add/remove/clear/view] secondary argument <- Usually an int

Keyword Trigger:
    Bot is triggered automatically from a series of keywords.

Expanded:
    Horny:
    This function will send the 'go to horny jail' image when someone uses one of these words:
    Horny Keywords
        Boobs
        Butt
        Cum
        Cute
        Feet
        Gasm
        Horny
        Hot
        Sexy
        Tits
        Toes

    Joker:
	This function will send :FunnyMan: when someone uses one of these words:
	Joker Keywords
		A24
		Abuse
		Funny
		Joker
		Kino
		Misogyny
		Pedo
		Phile
		Prejudice
		Racism
		Racist
		Society
		Terrorism
		Terrorist

    Monkey:
	This function will send one of the following emotes when someone uses one of the keywords mentioned below:
		:monkey:
		:gorilla:
		:orangutan:
		:monkey_face:
		:squadW:
	Monkey Keywords:
		Ape
		Banana
		Chimp
		Gorilla
		Mongoloid
		Monke
		Orangutan
		Peanut
		Pimp
		Primate
		Train 
	
