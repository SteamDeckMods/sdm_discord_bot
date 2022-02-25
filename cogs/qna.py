from discord.ext import tasks, commands
import discord
import json


class QnAHelper(commands.Cog):
    """(Jankily) Manages all stuff associated with the Q&A Channel"""

    def __init__(self, bot):
        self.bot = bot
        with open("qna.json", 'r') as config_file:
            config = json.load(config_file)
            self.qna_channel = config["Discord"]["Channels"]["QNA"]
            self.qna_upvote = config["Discord"]["Emojis"]["UPVOTE"]
            self.html_out = config["Apache"]["site_root"] + "/" + config["Apache"]["filename"]
            self.truncate = int(config["Apache"]["truncate"])
            self.stylesheet_href = config["Apache"]["stylesheet"]
        self.questions = dict()
        #self.debug_questions.start()
        self.generate_html_output.start()

    def cog_unload(self):
        self.debug_questions.cancel()
        self.generate_html_output.cancel()

    async def cog_check(self, ctx):
        """
        Precheck that prevents anyone without an apropriate role
        from using any commands in this cog. This does not need to be called.
        """
        # note that this doesn't do anything atm because there are no commands
        return msg.channel.id == self.qna_channel

    @commands.Cog.listener(name="on_message")
    async def new_question(self, msg):
        if msg.channel.id != self.qna_channel:
            return
        self.questions[msg.id] = (msg.id, msg.content, 0, self.user_name(msg.author))

    @commands.Cog.listener(name="on_message_delete")
    async def question_removed(self, msg):
        if msg.channel.id != self.qna_channel:
            return
        if msg.id in self.questions:
            del(self.questions[msg.id])

    @commands.Cog.listener(name="on_message_edit")
    async def question_modified(self, msg_before, msg):
        if msg.channel.id != self.qna_channel:
            return
        if msg.content == "":
            await self.question_removed(msg)
        else:
            self.questions[msg.id] = (msg.id, msg.content, 0, self.user_name(msg.author))

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def question_vote_added(self, event):
        if event.channel_id != self.qna_channel:
            return
        if event.emoji.name != self.qna_upvote or event.message_id not in self.questions:
            return
        old_val = self.questions[event.message_id]
        self.questions[event.message_id] = (old_val[0], old_val[1], old_val[2]+1, old_val[3])

    @commands.Cog.listener(name="on_raw_reaction_remove")
    async def question_vote_removed(self, event):
        if event.channel_id != self.qna_channel:
            return
        if event.emoji.name != self.qna_upvote or event.message_id not in self.questions:
            return
        old_val = self.questions[event.message_id]
        self.questions[event.message_id] = (old_val[0], old_val[1], old_val[2]-1, old_val[3])

    @tasks.loop(seconds=5.0)
    async def debug_questions(self):
        print("----- new tally ----")
        sorted_questions = self.sort_questions()
        sorted_strs = list()
        for q in sorted_questions:
            sorted_strs.append(f"msg `{q[1]}` from {q[3]} has {q[2]} votes")
        print("\n".join(sorted_strs))

    @tasks.loop(seconds=5.0)
    async def generate_html_output(self):
        #print("Writing HTML out")
        sorted_questions = self.sort_questions()
        if self.truncate > 0:
            sorted_questions = sorted_questions[:self.truncate]
        sorted_strs = list()
        # generate some HTML the bad/stupid way
        for q in sorted_questions:
            sanitised = q[1].replace(">", "").replace("<", "")
            sorted_strs.append(f"<tr><td>{q[3]}</td><td>{sanitised}</td><td>{q[2]}</td></tr>")
        table_innards = "\n".join(sorted_strs)
        stylesheet = ""
        if self.stylesheet_href != "":
            stylesheet = f"<link rel=\"stylesheet\" type=\"text/css\" href=\"{self.stylesheet_href}\" media=\"screen\" />"
        table = "<table><tr><th>Author</th><th>Message</th><th>Votes</th></tr>" + table_innards + "</table>"
        page = "<head><title>Q&A Vote Tally</title><meta charset=\"utf-8\">" + stylesheet + "</head><body><h1 style=\"display: none;\">Questions, ordered by popularity as jankily judged by the SDM Discord Bot</h1>" + table + "</body>"
        with open(self.html_out, 'w') as html_file:
            html_file.write(page)

    def sort_questions(self):
        values = sorted(self.questions.values(), key = lambda item: item[2], reverse = True)
        return values

    def user_name(self, member):
        if member.nick is None:
            return member.name
        else:
            return member.nick



def setup(bot):
    bot.add_cog(QnAHelper(bot))
