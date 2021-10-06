from models import db, connect_db, User, Post, Tag, PostTag
from app import app

db.drop_all()
db.create_all()

#tags

tag1 = Tag(name="food")
tag2 = Tag(name="meet")
tag3 = Tag(name="greet")
tag4 = Tag(name="new")
tag5 = Tag(name="nature")
tag6 = Tag(name="hunting")
tag7 = Tag(name="dog")
tag8 = Tag(name="treat")

db.session.add_all([tag1,tag2,tag3,tag4,tag5,tag6,tag7,tag8])

db.session.commit()

#users

k = User(first_name="Kratai", last_name="Gordon")
j = User(first_name="Josiah", last_name="Gordon")
e = User(first_name="Evie Marie", last_name="Gordon")

db.session.add_all([k, j, e])

db.session.commit()

#post

post1 = Post(title="Foods", content="I love food so much", userid=1)
post2 = Post(title="Hello, doggo fellas", content="What are the good treats do you all recommend?", userid=3)
post3 = Post(title="Elk Hunting Season", content="The season is near and I cannot wait", userid=2)

db.session.add_all([post1,post2,post3])

db.session.commit()

#post_tags

post_tag1 = PostTag(post_id=1, tag_id=1)
post_tag2 = PostTag(post_id=1, tag_id=2)
post_tag3 = PostTag(post_id=1, tag_id=3)
post_tag4 = PostTag(post_id=1, tag_id=4)
post_tag5 = PostTag(post_id=2, tag_id=7)
post_tag6 = PostTag(post_id=2, tag_id=8)
post_tag7 = PostTag(post_id=3, tag_id=5)
post_tag8 = PostTag(post_id=3, tag_id=6)

db.session.add_all([post_tag1,post_tag2,post_tag3, post_tag4, post_tag5, post_tag6, post_tag7, post_tag8])

db.session.commit()
