import requests, json, argparse
import dateutil.relativedelta
from datetime import date, timedelta
from textblob import TextBlob
from random import sample

class Util():

    def arg_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-cfg', '--config', default='config.json', help='Path to config file'
        )

        return parser

    @classmethod
    def convert_json_to_dict(self, json_str: str):
        dictionary = json.loads(json_str)
        return dictionary

class MadlibGame(Util):
    """
    A Madlib game that seaches the internet for recent news stories, selects one, then replaces random words with a user input, prompting the user for the part of speech of the word he or she is to replace. 
    """
    def __init__(self, args):
        self.config = args.config
        
    def query_articles(self, args, from_date: date, to_date: date):
        """
        Make a query to newsdata.io and returns the query

        ARGS:
        from_date: The date from which we are searching
        to_date: The date to which we are searching
        """
        url = (f'https://newsdata.io/api/1/news?apikey={args.config["token"]}&'
            f'qInTitle={args.config["query"]}&'
            f'language=en&'
            f'from_date={from_date}&'
            f'to_date={to_date}&'
    )
        
        response = requests.get(url)
        json_string = response.json()
        return json_string['results']

    def get_datetime(self) -> (date, date):
        """
        Returns today's date and 29 days earlier
        """
        d = date.today() - timedelta(days=1)
        d2 = d - dateutil.relativedelta.relativedelta(days=29)\
        
        return d, d2

    def select_an_article(self, query_results) -> dict:
        """
        Returns the first non-None article from a returned article query. Returns an empty dict if no article is found.

        ARGS:
        query_result: A returned result from query_articles()
        """
        selected_article = {}
        for query_result in query_results:
            if ('title' in query_result and
                'content' in query_result and
                query_result['title'] is not None and 
                query_result['content'] is not None and
                query_result['title'] != "" and
                query_result['content'] != ""):
                selected_article['title'] = query_result['title']
                selected_article['content'] = query_result['content']
                continue
            else:
                pass
        
        return selected_article

    def get_user_input(self, args, word: dict) -> str:
        """
        Prompt the user for the part of speech of a given word and return the result

        ARGS:
        word: A dictionary containing the word, its part of speech, and the index in the sentence where it came from
        """
        part_of_speech_list = args.config['eligable_parts_of_speech']
        part_of_speech = part_of_speech_list[word['part_of_speech']]

        user_input = input(f'Type a {part_of_speech} >> ')
        return f'_{user_input}_'

    def process_sentence(self, args, sentence: TextBlob) -> str:
        """
        Selects a single random word from a sentence and replaces it with a user input
        
        ARGS:
        sentence: The TextBlob sentence to process
        """
        words_eligable_to_replace = []
        for index, word in enumerate(sentence.tags):
            for eligable_part_of_speech in args.config['eligable_parts_of_speech']:
                if word[1] == eligable_part_of_speech:
                    words_eligable_to_replace.append(
                        {'word': word[0],
                        'index': index,
                        'part_of_speech': word[1]})
        # Select a random word from the sentence
        if words_eligable_to_replace != []:
            selected_word = sample(words_eligable_to_replace,  1)   # Pick a random item from the list
            selected_word = selected_word[0] # Normalize the selected_word
            user_input = self.get_user_input(args, selected_word)
            sentence.words[selected_word['index']] = user_input
        else:
            pass
        
        sentence_to_return = ' '.join(sentence.words)

        return sentence_to_return


    def process_article(self, text: str):
        """
        Parses the article in to sentences and processes each sentence. Returns the article with the user inputs.

        ARGS:
        text: The string to process
        """

        textblob_string = TextBlob(text)
        list_article_with_user_inputs = []
        for sentence in textblob_string.sentences:
            sentence_with_replaced_word = self.process_sentence(args, sentence)
            list_article_with_user_inputs.append(sentence_with_replaced_word)
        
        article_with_user_inputs = '. '.join(list_article_with_user_inputs)
        
        return article_with_user_inputs

    def run(self, args):
        to_date, from_date = self.get_datetime()
        query_results = self.query_articles(args, from_date, to_date)
        selected_article = self.select_an_article(query_results)
        if selected_article != {}:
            final_text = self.process_article(selected_article['content'])
        else:
            raise Exception('Looks like I could not find any articles.  Please try modifying the query field in config.json' )

        return selected_article['title'], final_text


if __name__ == '__main__':
    parser = MadlibGame.arg_parser()
    args = parser.parse_args()

    args.config = MadlibGame.convert_json_to_dict(open(args.config).read())
    game = MadlibGame(args)
    title, content = game.run(args)
    print()
    print(title)
    print()
    print(content)