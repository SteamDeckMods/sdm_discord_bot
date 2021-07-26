Discord bot for Steam Deck Discord specific use.

* `reload cogs.<cogname>` (i.e; >reload cogs.helper_role)
Allows users with enough permissions to reload certain cogs for live testing/debug

* `sitdown @user1 @user2 ...`
Adds users to the sit-down role

* `sitdownrelease @user1 @user2 ...`
Removes users from the sit-down role

* `scoopnotification`
Allows users with enough permissions to notify News Junkies in the scoop channel.


A config.json file is required for the bot to run. It looks like this;
```json
{
    "Discord": {
        "API_KEY": "Key-Goes-Here",
        "COMMAND_PREFIX" : ">",
        "Roles": {
            "BOT_DEV" : 212590471648772096,
            "HELPER": 205902469207687170,
            "RESEARCHER": 205902469207687170,
            "NEWS": 222054704471998465,
            "TIMEOUT": 206188934085083146
        },
        
        "Channels" : {
            "RESEARCH" : 205897207721754624,
            "NEWS" : 309846667597709324
        }
    }
}
```