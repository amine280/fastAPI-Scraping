from fastapi import FastAPI
import uvicorn 
from facebook_scraper import get_posts
import sqlite3 as sl

app = FastAPI()

@app.get("/")
def read_root():
    return "Add /docs to the Adress Bar. to go to Swagger."

def delete_none(d):
    new_dict = dict()
    for k, v in d.items():
        if v:
            new_dict[k] = v
    new_dict["_id"] = new_dict["post_id"]
    return new_dict

con = sl.connect('database.db')
c = con.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS POSTS
		    	(id INTEGER NOT NULL PRIMARY KEY, page TEXT,contenu TEXT,likes INTEGER,comments INTEGER,shares INTEGER); ''')

@app.get("/scrap/{page_name}",summary="Insert the page name")
async def scrap_posts(page_name):
    posts = []
    try:
        posts = list(get_posts(page_name, pages=1))
        posts = [delete_none(post) for post in posts]
        insert_posts(posts)
        for post in posts:
            values=(post['post_id'], page_name, post['text'], post['likes'], post['comments'], post['shares'])
            c.execute('INSERT INTO POSTS (id, page, contenu, likes, comments, shares) values(?, ?, ?, ?, ?, ?)', values)
            con.commit()
    except:
        pass
    return posts

    
if __name__ == '__main__':
    uvicorn.run(app, port = 8000, host = "127.0.0.1")