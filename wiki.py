from application_config import app, db
from common_models import User

class School(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)

class Topic(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    topic_name = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    def __unicode__(self):
        return self.topic_name

#put an index on date_time and topic -- make it a b tree index
class DiscussionPost(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text(), nullable = False)
    user = db.Column(db.Integer(), db.ForeignKey('user.id'))
    date_time = db.Column(db.DateTime(), nullable = False)
    topic = db.Column(db.Integer(), db.ForeignKey('topic.id'))
    ups = db.Column(db.Integer(), nullable = False, default = 0)
    downs = db.Column(db.Integer(), nullable = False, default = 0)
    deleted = db.Column(db.Boolean(), nullable=False, default = False)
    def __unicode__(self):
        return unicode(self.user) + " posted " + unicode(self.text) + " to " + unicode(self.topic)

#put an index on discussion post and date_time
class DiscussionResponse(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text(), nullable = False)
    user = db.Column(db.Integer(), db.ForeignKey('user.id'))
    date_time = db.Column(db.DateTime(), nullable = False)
    topic = db.Column(db.Integer(), db.ForeignKey('topic.id'))
    ups = db.Column(db.Integer(), nullable = False, default = 0)
    downs = db.Column(db.Integer(), nullable = False, default = 0)
    deleted = db.Column(db.Boolean(), nullable=False, default = False)
    discussion_post = db.Column(db.Integer(), db.ForeignKey('discussion_post.id'))
    def __unicode__(self):
        return unicode(self.user) + " posted " + unicode(self.text) + " in response to " + unicode(self.discussion_post.text)


#handles the shits for getting feedback
class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    comment = db.Column(db.Text(), nullable = False)
    date_time = db.Column(db.DateTime(), nullable = False)
    ip = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    def __unicode__(self):
        if self.email:
            return self.email + ' sent ' + self.comment
        else:
            return self.comment

class Subject(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    def __unicode__(self):
        return self.name

class Course(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    subject = db.Column(db.Integer(), db.ForeignKey('subject.id'))
    number = db.Column(db.String(60), nullable=False)
    school = db.Column(db.Integer(), db.ForeignKey('school.id'))
    def __unicode__(self):
        return unicode(self.subject) + " " + self.number

#first level topics to subject
class TopicToSubject(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    topic = db.Column(db.Integer(), db.ForeignKey('topic.id'))
    subject = db.Column(db.Integer(), db.ForeignKey('subject.id'))
    def __unicode__(self):
        return unicode(self.subject) + "'s " + unicode(self.topic)


class TopicTree(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    subject = db.Column(db.Integer(), db.ForeignKey('subject.id'))
    #represents the json tree representation {'parent_topic' : {'child_topic' : {'grandchild_topic' : None, 'grandchild_topic2' : None}}}
    tree_representation = db.Column(db.String(1000), nullable=False)
    def __unicode__(self):
        return self.tree_representation

class ContentToTopic(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.Text(), nullable = False)
    links = db.Column(db.Text(), nullable = False, default = '')
    topic = db.Column(db.Integer(), db.ForeignKey('topic.id'))
    version_number = db.Column(db.Integer(), nullable = False)
    def __unicode__(self):
        return unicode(self.topic) + "'s content"

#store everything so that we can easily mix and match topics to put inside of a class and mask certain topics out of a specific course
class TopicToCourse(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    topic = db.Column(db.Integer(), db.ForeignKey('topic.id'))
    course = db.Column(db.Integer(), db.ForeignKey('course.id'))
    def __unicode__(self):
        return unicode(self.course) + " has this topic: " + unicode(self.topic)
