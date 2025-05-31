from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SummaryDetails(db.Model):
    __tablename__ = 'summarydetails'

    summaryId = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    doc_path = db.Column(db.String(200), nullable=False)
    dt = db.Column(db.String(200), nullable=False)
    summary1 = db.Column(db.LargeBinary, nullable=True)
    summary2 = db.Column(db.LargeBinary, nullable=True)
    summary3 = db.Column(db.LargeBinary, nullable=True)

    def to_dict(self):
        return {
            "summaryId": self.summaryId,
            "userid": self.userid,
            "title": self.title,
            "doc_path": self.doc_path,
            "dt": self.dt
        }
