from src.common.database import Database
import uuid
import datetime


class Post(object):

    def __init__(self, blog_id, title, content, author, created_date=datetime.datetime.utcnow(), _id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date = created_date
        # unique post id
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='posts',
                        data=self.json())

    def json(self):
        return {
            "_id": self._id,
            "blog_id": self.blog_id,
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "created_date": self.created_date
        }

    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='posts', query={'_id': id})
        return cls(**post_data)

    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection='posts', query={'blog_id': id})]


if __name__ == '__main__':
    Database.initialize()
    post = Post(blog_id="00219e9981b24c37802ac31b6338aef0",
                title="test post",
                content="test content",
                author="test@email.com")
    post.save_to_mongo()
