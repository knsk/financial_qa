import logging
from settings import DATABASE
from datetime import datetime
from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker, relationship
from sqlalchemy.types import Integer, Unicode, DateTime, Text, LargeBinary

engine = create_engine(URL(**DATABASE), pool_recycle=30, pool_pre_ping=True, echo=False)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

class Base(DeclarativeBase):
  pass


class TimestampMixin(object):
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Article(TimestampMixin, Base):
  __tablename__ = "articles"
  id = Column(Integer, primary_key = True)
  title = Column(Unicode(255))
  url = Column(Unicode(255))
  text = Column(Text)
  published_at = Column(DateTime)
  article_images = relationship("ArticleImage")

  @classmethod
  def get_or_create(cls, title: str, url: str, text: str, published_at: datetime):
    article = session.query(Article).filter(cls.url==url).first()
    if not article:
      article = Article(title=title, url=url, text=text, published_at=published_at)
      session.add(article)
      session.commit()
    return article

  @classmethod
  def update_or_create(cls, title: str, url: str, text: str, published_at: datetime):
    article = cls.get_or_create(title=title, url=url, text=text, published_at=published_at)
    article.title = title
    article.text = text
    article.published_at = published_at
    session.add(article)
    session.commit()
    return article




class ArticleImage(TimestampMixin, Base):
  __tablename__ = "article_images"
  id = Column(Integer, primary_key=True)
  article_id = Column(Integer, ForeignKey(Article.id))
  url = Column(Unicode(255))
  image = Column(LargeBinary)
