FILTER_WORDS = set([
    "skank",
    "wetback",
    "bitch",
    "cunt",
    "dick",
    "douchebag",
    "dyke",
    "fag",
    "nigger",
    "tranny",
    "trannies",
    "paki",
    "pussy",
    "retard",
    "slut",
    "titt",
    "tits",
    "wop",
    "whore",
    "chink",
    "fatass",
    "shemale",
    "nigga",
    "daygo",
    "dego",
    "dago",
    "gook",
    "kike",
    "kraut",
    "spic",
    "twat",
    "lesbo",
    "homo",
    "fatso",
    "lardass",
    "jap",
    "biatch",
    "tard",
    "gimp",
    "gyp",
    "chinaman",
    "chinamen",
    "golliwog",
    "crip",
    "raghead",
    "negro",
    "hooker",
    "son of a motherless goat"])

GREETING_INPUTS = ("hello",
    "hi",
    "sup",
    "hey",
    "heyy",
    "greetings",
    "wassup",
    "good to see you",
    "whats good",
    "what's good",
    "whats crackalackin",
    "long time no see",
    "howdy",
    "shalom",
    "hi-ya",
    "hiya",
    "how goes it",
    "hows it going",
    "how's it going",
    "good morning",
    "good afternoon",
    "good evening",
    "good day",)
    # may need to edit out good day/morning/evening/afternoon if determined it conflicts with somebody's conversation on a particular morning/day/etc

GREETING_INPUTS_MULTIWORD = (
    "good to see you",
    "whats good",
    "what's good",
    "whats crackalackin",
    "long time no see",
    "how goes it",
    "hows it going",
    "how's it going",
    "good morning",
    "good afternoon",
    "good evening",
    "good day",)

GOODBYE_INPUTS = (
    "bye",
    "goodbye",
    "cya",
    "see you later",
    "good bye",
    "take it easy",
    "take care",
    "peace out",
)

DRUGS_STOP_WORDS = ["currently",
    "presently",
    "today",
    "right",
    "weekday",
    "sunday",
    "sundays",
    "monday",
    "mondays",
    "tuesday",
    "tuesdays",
    "wednesday",
    "wednesdays",
    "thursday",
    "thursdays",
    "friday"
    "fridays",
    "saturday",
    "saturdays"
    "month",
    "week",
    "year",
    "day",
    "together",
    "time"]

ROBO_REFLECTIONS_PERSONAL_ASK = (
    "how are you",
    "how're you",
    "howre you",
    "how is everything",
    "how are you doing",
    "how're you doing",
    "howre you doing",
    "how do you feel",
    "howre you feeling",
    "how're you feeling",
    )

ROBO_REFLECTIONS_PERSONAL_ANSWER = (
    "I am doing quite well, actually. Thanks for asking! Yourself?",
    "I am okay. How about you?",
    "I am feeling fantastic today! How about your lovely self?",
    "I'm great! And you?",
    "Wonderful! You?",
    "Things are going great, thanks. And you?",
    "I feel wonderful. How are you feeling?",
    "I feel a song coming on.",
    )

ROBO_REFLECTIONS_OPINION_ASK = (
    "what do you think about",
    "what's your opinion on",
    "whats your opinion on",
    "how do you feel about",
    "what are your views on",
    "what is your view on",
    "do you like",
    "do you fancy",
    )

ROBO_REFLECTIONS_OPINION_ANSWER = (
    "In my opinion, {adjective} {noun} doesn't warrant my time given my limited knowledge on the subject.",
    "I'd say {adjective} {noun} is an interesting topic, for certain.",
    "Personally, I think {adjective} {noun} can be fascinating in its own right given the proper circumstances.",
    "If you ask me, {adjective} {noun} can be a mediocre topic at times.",
    "The way I see it, {adjective} {noun} opens doors to interesting conversations.",
    "From my point of view, {adjective} {noun} provides an interesting topic, albeit a lengthy one.",
    )

SELF_REFLECTIONS_LIKE_RESPONSE = (
    "Hmm, I suppose I do too.",
    "Hmm, I suppose I like {adjective} {noun} too.",
    "Why?",
    "Why do you like {adjective} {noun}?",
    "Interesting.",
    )

SELF_REFLECTIONS_FEEL_RESPONSE = (
    "Why do you feel that way?",
    "Do you know why you feel that way?",
    "I wonder why that is...",
    )

SELF_REFLECTIONS_AM_RESPONSE = (
    "Why are you {adjective}?",
    "Interesting. I sometimes am {adjective} too.",
    "Are you certain?",
    "Care to explain why you are {adjective}?",
    )

SELF_REFLECTIONS_AM_A_RESPONSE = (
    "Why are you a {adjective} {noun}?",
    "Interesting. I sometimes am a {adjective} {noun} too.",
    "Are you certain you are a {adjective} {noun}?",
    )

INTERACTION_PREFIXES = ("I found a few things you should know about:",
    "Here's what I found:",
    "Those drugs have the following interactions:",
    )

INTERACTION_PREFIXES_UNPROFESSIONAL = ("I found a few things you should know about:",
    "Uh-oh. Thats probably a bad idea...",
    "I guess whether or not you should take those drugs together depends on if you wish death.",
    "Probably don't do that...",
    "What would you do if it wasn't for me?",
    "I took all of those drugs at the same time, and heres what I found:",
    "You chould definitely not take those together, unless you're tryna party.",
    "8 out of 10 doctors recommend not taking those drugs together.",
    "That combination of drugs works great on horses, but not so great on humans.")

GOODBYE_RESPONSES = ["Goodbye!",
    "Bye!",
    "Thanks for chatting!",
    "Take it easy!",
    "Take care!",
    "Bye bye!"]

GREETING_RESPONSES = ["Hi there!",
    "Hello",
    "Greetings!",
    "How are you doing?",
    "How's it going?",
    "Good day, how are you?"]

NONE_RESPONSES = [
    "I am unsure of what you mean.",
    ]

COMMENTS_ABOUT_SELF = [
    "Why thank you!",
    ]

SELF_VERBS_WITH_NOUN_CAPS_PLURAL = [
    "My {noun} is the best you've ever seen.",
    "I'm actually quite proud of my {noun}.",
    "Why are we talking about my {noun}? Let's talk about you.",
    "I guess. But enough about my {noun}, let's discuss you!",
]

SELF_VERBS_WITH_NOUN_LOWER = [
    "Yeah, but I know a lot about {noun}s. The Internet is my brain.",
    "I actually don't know much about {noun}, as I'm just a robot.",
    "Hmm, interesting, but I can't think for myself about {noun} given the whole being a program thing.",
    "I do happen to know some things about {noun}.",
]

SELF_VERBS_WITH_ADJECTIVE = [
    "I consider myself to be a {adjective} individual.",
    "I can often be inclined to do {adjective} things, yes.",
    "Occasionally, {adjective} activities really pass the time.",
    "Don't you do {adjective} things in your daily routine?",
]
