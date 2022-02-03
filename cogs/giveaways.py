from discord.ext import commands
import json
import pathlib
import time


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.write_count = 0
        with open("giveaways.json", 'r') as giveaway_config_file:
            self.config = json.load(giveaway_config_file)
            self.giveaway_channel = self.config["Discord"]["Channels"]["GIVEAWAY"]
            self.giveaway_role = self.config["Discord"]["Roles"]["GIVEAWAY"]
            self.booster_role = self.config["Discord"]["Roles"]["BOOSTER"]
            self.patron_role = self.config["Discord"]["Roles"]["PATRON"]
            self.writes_per_flush = self.config["Giveaway"]["writes_per_flush"]
            self.giveaway_csv = self.config["Giveaway"]["csv"]
        
        with open("config.json", 'r') as config_file:
            config = json.load(config_file)
            self.admin_role = config["Discord"]["Roles"]["ADMIN"]
        
        if not pathlib.Path(self.giveaway_csv).is_file():
            self.make_new_csv()
        self.output_file = open(self.giveaway_csv, 'a')
    
    def cog_unload(self):
        self.output_file.close()
        
    def has_admin_role(self, member):
        return self.admin_role in [r.id for r in member.roles]
    
    def has_giveaway_role(self, member):
        return self.giveaway_role in [r.id for r in member.roles]

    def has_booster_role(self, member):
        return self.booster_role in [r.id for r in member.roles]

    def has_patron_role(self, member):
        return self.patron_role in [r.id for r in member.roles]

    def make_new_csv(self):
        """Generate CSV with header"""
        with open(self.giveaway_csv, 'w') as csv_file:
            csv_file.write("Unix Timestamp,Username,User ID,Has Role?,Booster,Patron")
            csv_file.write("\n")
    
    @commands.Cog.listener(name="on_message")
    async def log_activity(self, msg):
        """Log messages in the giveaway channel"""
        if msg.author == self.bot.user:
            return
        if msg.channel.id == self.giveaway_channel:
            # log user activity to csv if in giveaway channel
            has_role = int(self.has_giveaway_role(msg.author))
            booster = int(self.has_booster_role(msg.author))
            patron = int(self.has_patron_role(msg.author))
            line = f"{int(time.time())},{msg.author.name},{msg.author.id},{has_role},{booster},{patron}"
            #print("Activity:", line)
            self.output_file.write(line)
            self.output_file.write("\n")
            self.write_count += 1
            if self.write_count >= self.writes_per_flush:
                self.output_file.flush()  # force write to disk
                self.write_count = 0
    
    @commands.command(name="csv-cleargiveaway")
    async def giveup(self, msg):
        """Clear and restart the giveaway CSV file"""
        if not self.has_admin_role(msg.author):
            await msg.channel.send("I don't trust you")
            return
        self.output_file.close()
        self.make_new_csv()
        self.output_file = open(self.giveaway_csv, 'a')
        await msg.channel.send(f"Truncated `{self.giveaway_csv}` successfully")


def setup(bot):
    bot.add_cog(Giveaway(bot))
