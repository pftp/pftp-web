from application_config import app, db
from flask.ext.security import RoleMixin, UserMixin, SQLAlchemyUserDatastore

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer(), primary_key=True)
  email = db.Column(db.String(120), index = True, unique = True, nullable = False)
  firstname = db.Column(db.String(30), index = True, nullable = False)
  lastname = db.Column(db.String(30), index = True, nullable = False)
  password = db.Column(db.String(255), nullable = False)
  active = db.Column(db.Boolean())
  website = db.Column(db.String(120))
  confirmed_at = db.Column(db.DateTime())
  roles = db.relationship('Role', secondary=roles_users,
      backref=db.backref('user', lazy='dynamic'))
  grades = db.relationship('Grade', lazy='dynamic', backref='user')
  programs = db.relationship('Program', lazy='dynamic', backref='user')
  code_revisions = db.relationship('CodeRevision', lazy='dynamic', backref='user')
  submissions = db.relationship('Submission', lazy='dynamic', backref='user')

  def is_admin(self):
    return self.has_role("admin")

  def add_grade(self, assignment, score):
    grade = Grade(score=score)
    self.grades.append(grade)
    assignment.grades.append(grade)
    db.session.add(grade)
    db.session.commit()

  def get_grade(self, assignment):
    grades = self.grades.filter_by(assignment_id=assignment.id).all()
    if len(grades) == 0:
      grade = self.grades.filter_by(assignment_id=assignment.id).all()[0]
      return grade
    else:
      return None

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
