import openai

with open('secret.key', 'r') as f:
    key = f.read().replace('\n', '')

openai.api_key = key

class ChatBot:
    def __init__(self, engine="text-davinci-003", max_tokens=500):
        self.engine = engine
        self.max_tokens = max_tokens
        self.prompts = []
        self._responses = []
        self.replies = []

    def say(self, something):
        self.prompts.append(something)
        self._responses.append(
                response := openai.Completion.create(
                    engine=self.engine,
                    prompt=something,
                    max_tokens=self.max_tokens
                    )
                )
        self.replies.append(reply:=response.choices[0].text)
        return reply

class AutoBlogger:
    def __init__(self, subject='hobbies', engine="text-davinci-003", max_tokens=2500):
        self.chatbot = ChatBot(engine=engine, max_tokens=max_tokens)
        self.subject = subject
        self.ideas = []
        self.posts = {}

    @staticmethod
    def start_blog(subject='coding in Python'):
        return f"""
            I am starting a blog. Give me blog ideas on the subject of {subject}.
            """

    @staticmethod
    def write_post_about(idea):
        return f"Write a 500 word blog post with the title {idea}."


    def get_ideas(self):
        self.ideas = self.ideas + self.chatbot.say(
                self.start_blog(self.subject)).split('\n')
        print(self.ideas)

    def write_post(self, idea):
        if not idea in self.posts.keys():
            self.posts[idea] = self.chatbot.say(
                    self.write_post_about(idea))
        print(self.posts[idea])

    def save_posts(self, save_dir):
        pass

def autoblog(subject='whatever'):
    blogger = AutoBlogger(subject=subject)

    blogger.get_ideas()

    [blogger.write_post(idea) for idea in blogger.ideas if idea]


    return blogger


autoblog('Mastering the Linux Command Line')
