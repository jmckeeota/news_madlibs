from news_madlibs import MadlibGame

payload = [{"title": "Bad_Title"}, 
           {"title": None, "content": "Bad_Content"},
           {"title": "Good_Title", "content": "Good_Content"},
           {"title": "Bad_Title"},
           {"title": None, "content": "Bad_Content"}]

def test_article_select():
    response = MadlibGame.select_an_article(self="test", query_results=payload)
    assert response == { "title": "Good_Title", "content": "Good_Content" }