#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='siva')
        u.set_password('shambho')
        self.assertFalse(u.check_password('shivashambho'))
        self.assertTrue(u.check_password('shambho'))

    def test_avatar(self):
        u = User(username='visweswaraya', email='visweswaraya@kasi.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/9252e7996b37f296923820fbb5548345?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='siva', email='siva@kailash.com')
        u2 = User(username='visweswaraya', email='visweswaraya@kasi.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u2.follow(u1)
        db.session.commit()
        self.assertTrue(u2.is_following(u1))
        self.assertEqual(u2.followed.count(), 1)
        self.assertEqual(u2.followed.first().username, 'siva')
        self.assertEqual(u1.followers.count(), 1)
        self.assertEqual(u1.followers.first().username, 'visweswaraya')

        u2.unfollow(u1)
        db.session.commit()
        self.assertFalse(u2.is_following(u1))
        self.assertEqual(u2.followed.count(), 0)
        self.assertEqual(u1.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(username='visweswaraya', email='visweswaraya@kasi.com')
        u2 = User(username='mallikarjuna', email='mallikarjuna@srisailam.com')
        u3 = User(username='rameswaraya', email='rameswaraya@rameswaram.com')
        u4 = User(username='siva', email='siva@kailash.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="Om visweswaraya namaha", author=u1,
                    timestamp=now + timedelta(seconds=1))
        p2 = Post(body="Om Namah Shivaya", author=u2,
                    timestamp=now + timedelta(seconds=4))
        p3 = Post(body="Om rameswayaraya namaha", author=u3,
                    timestamp=now + timedelta(seconds=3))
        p4 = Post(body="Om kailasavaya namaha", author=u4,
                    timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        #setup the followers
        u1.follow(u4) # visweswaraya follows siva
        u1.follow(u2) # visweswaraya follows mallikarjuna
        u2.follow(u3) # mallikarjuna follows rameswaraya
        u3.follow(u4) # rameswaraya follows siva
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)
