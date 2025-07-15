import tornado.ioloop
import tornado.web
import db  # keep this if you're using db.py
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html")

class ArticleListHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")

    def get(self):
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, content FROM articles ORDER BY id DESC;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        articles = [{"id": r[0], "title": r[1], "content": r[2]} for r in rows]
        self.write(json.dumps(articles))

class ArticleCreateHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")

    def post(self):
        try:
            title = self.get_argument("title")
            content = self.get_argument("content")

            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO articles (title, content) VALUES (%s, %s)", (title, content))
            conn.commit()
            cur.close()
            conn.close()

            self.write({"status": "success"})
        except Exception as e:
            self.set_status(500)
            self.write({"status": "error", "message": str(e)})
 
class ArticleEditHandler(tornado.web.RequestHandler):
    def post(self, article_id):
        try:
            title = self.get_argument("title")
            content = self.get_argument("content")

            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(
                "UPDATE articles SET title = %s, content = %s WHERE id = %s",
                (title, content, article_id)
            )
            conn.commit()
            cur.close()
            conn.close()

            self.write({"status": "updated"})
        except Exception as e:
            self.set_status(500)
            self.write({"status": "error", "message": str(e)})


class ArticleDeleteHandler(tornado.web.RequestHandler):
    def post(self, article_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM articles WHERE id = %s", (article_id,))
            conn.commit()
            cur.close()
            conn.close()

            self.write({"status": "deleted"})
        except Exception as e:
            self.set_status(500)
            self.write({"status": "error", "message": str(e)})


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/articles", ArticleListHandler),
        (r"/articles/create", ArticleCreateHandler),
        (r"/articles/edit/([0-9]+)", ArticleEditHandler),
        (r"/articles/delete/([0-9]+)", ArticleDeleteHandler),
    ],
    static_path="static",
    debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server running at http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
