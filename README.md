Discord bot for Steam Deck Discord specific use.

>reload cogs.<cogname> (i.e; >reload cogs.helper_role)
Allows users with enough permissions to reload certain cogs for live testing/debug

>sitdown @user1 @user2 etc
Adds users to the sit-down role

>sitdownrelease @user1 @user2 etc
Removes users from the sit-down role

>scoopnotification
Allows users with enough permissions to notify News Junkies in the scoop channel.

  
>NOTE config.json
A config.json file is required for the bot to run. It looks like this;
  {
    "Discord": {
        "API_KEY": "token key here",
        "COMMAND_PREFIX" : ">",
        
        "Roles": {
            "BOT_DEV" : 865684680195964998,
            "HELPER": 866128683809767474,
            "RESEARCHER": 867125502833852426,
            "NEWSJUNKIE": 865654074274873374,
            "SITDOWN": 866796838098042880
        },
        
        "Channels" : {
            "RESEARCH" : 867125657737232395,
            "SCOOP" : 865802501470683186
        }
    }
}
