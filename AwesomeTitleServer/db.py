from datetime import datetime

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .Achievements import *


admin = Admin()
db = SQLAlchemy()
migrate = Migrate()
N = 50


class User(db.Model):
    __tablename__ = "user"
    username = db.Column(db.String(N), primary_key=True)
    password_hash = db.Column(db.String(N + 10), nullable=False)
    realname = db.Column(db.String(N), nullable=False)
    student_number = db.Column(db.Integer, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)


class URL(db.Model):
    __tablename__ = "URL"
    link = db.Column(db.String(N), primary_key=True)
    username = db.Column(db.String(N))


class Nickname(db.Model):
    __tablename__ = "nickname"
    idx = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(N))
    nick = db.Column(db.String(N))
    recommender = db.Column(db.String(N))


class NickRecom(db.Model):
    __tablename__ = "nickrecom"
    idx = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(N))
    recommender = db.Column(db.String(N))
    username = db.Column(db.String(N))


class Photo(db.Model):
    __tablename__ = "photo"
    username = db.Column(db.String(N), primary_key=True)
    photo = db.Column(db.String(N + 10))


class Achievement(db.Model):
    """업적이 잠들어 있어요, zZZZ."""

    __tablename__ = "achievement"
    idx = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(N), unique=True)

    # TODO: logo_url = db.Column(db.String(N))
    #       XXX: 생각해보니까 Photo DB에 우리는 업적로고를 저장할 수 없어요.

    description = db.Column(db.String(2 * N))

    _categories = db.Column(db.String(N), default='[]')
    # XXX: 충분해? (now, N=50)
    #       0 ~ 18을 저장할 때 (19개) -> 48 bytes.
    #       10 ~ 26은 (두자릿수, 16개) -> 49 bytes.

    def addCategory(self, new_category_idx):
        """두둥! 우리는 어떻게 카테고리를 배열처럼 저장할 수 있을까요?

        우리의 One And The Only @Juice500ml 군의 힌트처럼,
        우리는 CSV(Comma-Seperated Value) 형식으로 (Issue #77 댓글)
        카테고리를 저장할 수 있습니다.

        리스트를 하나 만들고
        >>> c = []

        숫자를 추가합니다.
        >>> c.append(1)

        이건 이제 스트링으로 표현 가능 하죠?
        >>> str(c)
        '[1]'

        >>> c.append(2)
        >>> str(c)
        '[1,2]'

        파이썬에는 eval()라는 함수가 있어요.
        >>> d = eval(str(c))

        이를 통하면 스트링 형태의 파이선 코드를 실행할 수 있습니다.
        >>> d
        [1, 2]
        """

        currentCategories = self.getCategories()
        if new_category_idx in currentCategories:
            return False
        currentCategories.append(new_category_idx)
        currentCategories.sort()
        self._categories = repr(currentCategories)
        return True

    def delCategory(self, old_category_idx):
        currentCategories = self.getCategories()
        if old_category_idx not in currentCategories:
            return False
        currentCategories.remove(old_category_idx)
        self._categories = repr(currentCategories)
        return True

    def getCategories(self):
        """ eval(repr(A)) == A in PYTHONIC WORLD! """
        try:
            eval(self._categories)
        except SyntaxError:  # when `eval()` fail,
            self._categories = '[]'
        finally:
            return eval(self._categories)

    is_hidden = db.Column(db.Boolean, default=False)
    creators_issue_idx = db.Column(db.Integer, nullable=True)
    # XXX: 업적 제작자를 현명하게 저장하는 법을 찾아냈습니다!
    #      이것도 카테고리를 저장했던 것 처럼 한다면,
    #          무슨 문제가 발생할까요?
    #      우선 우리는 몇명의 제작자가 나올 지 몰라요.
    #      그리고 제작자의 사용자명이 얼마나 길지도 모릅니다.
    #
    #      그래서!,
    #       - 우리는 업적을 제작했다는 업적! 을 만들겁니다.
    #       - 그리고 그 업적은 is_hidden=True 로 숨기구요.
    #       - 그 업적을 획득한 사람은, 이 업적을 만든거에요!

    checker_func = db.Column(db.String(50), default=False)
    # XXX: 자동승인식 업적의 진행도를 확인해주는 함수거나,
    #      자신이 획득 가능한 업적인지 True/False로 알려주는 함수입니다.


class AchievementCategory(db.Model):
    """우리가 업적을 분류하는 방식."""

    __tablename__ = "achievementcategory"
    idx = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(N), unique=True)
    description = db.Column(db.String(N))


class AcquiredAchievement(db.Model):
    """아니 업적을 얻으셨다구요?"""

    __tablename__ = "acquiredachievement"
    idx = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(N))
    achievement_idx = db.Column(db.Integer)
    when = db.Column(db.DateTime, default=datetime.now)


class AchievementStatusForManualApproval(db.Model):
    """수동 승인식 업적을 신청하고 기다리는 사람들을 위한 DB."""

    __tablename__ = "achievementstatusformanualapproval"
    idx = db.Column(db.Integer, primary_key=True)
    achievement_idx = db.Column(db.Integer, nullable=False)
    waiting_username = db.Column(db.String(N), nullable=False)


class AchievementStatusForAutomaticApproval(db.Model):
    """자동 승인식 업적의 획득을 기다리는 사람들을 위한 DB."""

    __tablename__ = "achievementstatusforautomaticapproval"
    idx = db.Column(db.Integer, primary_key=True)
    achievement_idx = db.Column(db.Integer, nullable=False)
    target_username = db.Column(db.String(N), nullable=False)
    target_progress_percent = db.Column(db.Integer, default=0)
    target_status = db.Column(db.String(N), nullable=True)


class MyModelView(ModelView):
    column_display_pk = True


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(URL, db.session))
admin.add_view(MyModelView(Nickname, db.session))
admin.add_view(MyModelView(NickRecom, db.session))
admin.add_view(MyModelView(Photo, db.session))
admin.add_view(MyModelView(Achievement, db.session))
admin.add_view(MyModelView(AchievementCategory, db.session))
admin.add_view(MyModelView(AcquiredAchievement, db.session))
admin.add_view(MyModelView(AchievementStatusForManualApproval, db.session))
admin.add_view(MyModelView(AchievementStatusForAutomaticApproval, db.session))