from datetime import datetime

from sqlalchemy import select

from src.articles.models import Article
from tests.conftest import ArticleFactory


def test_create_article(client, user, token):
    date = datetime.now().isoformat()
    response = client.post(
        '/articles/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'this is a article',
            'content': 'str',
            'tags': 'str',
            'date': date,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'title': 'this is a article',
        'content': 'str',
        'tags': 'str',
        'user_id': user.id,
        'date': date,
    }


def test_get_articles(session, client, user):
    session.bulk_save_objects(ArticleFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get('/articles/')

    assert len(response.json()) == 5


def test_get_articles_pagination(session, client, user):
    session.bulk_save_objects(ArticleFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get('/articles/?skip=1&limit=2')

    assert len(response.json()) == 2


def test_get_article_filter_by_title(session, client, user):
    session.bulk_save_objects(
        ArticleFactory.create_batch(5, title='article 1', user_id=user.id)
    )
    session.commit()

    response = client.get('/articles/?title=article 1')

    assert len(response.json()) == 5


def test_get_article_filter_by_user_id(session, client, user):
    session.bulk_save_objects(ArticleFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(f'/articles/?user_id={user.id}')

    assert len(response.json()) == 5


def test_get_article_filter_by_content(session, client, user):
    session.bulk_save_objects(
        ArticleFactory.create_batch(5, content='content', user_id=user.id)
    )
    session.commit()

    response = client.get('/articles/?content=content')

    assert len(response.json()) == 5


def test_get_article_filter_by_tags(session, client, user):
    session.bulk_save_objects(
        ArticleFactory.create_batch(5, tags='tag', user_id=user.id)
    )
    session.commit()

    response = client.get('/articles/?tags=tag')

    assert len(response.json()) == 5


def test_get_article_all_filters(session, client, user):
    session.bulk_save_objects(
        ArticleFactory.create_batch(
            5,
            title='article all filters',
            content='content all filters',
            tags='tag',
            user_id=user.id,
        )
    )
    session.commit()

    response = client.get(
        f'/articles/?title=article all filters&content=all&tags=tag&user_id={user.id}'
    )

    assert len(response.json()) == 5


def test_update_article(session, client, token, user):
    session.bulk_save_objects(ArticleFactory.create_batch(5, user_id=user.id))
    session.commit()

    article_date = datetime.now().isoformat()

    response = client.put(
        '/articles/1',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'new title', 'date': article_date},
    )

    article_in_db = session.scalars(
        select(Article).filter(Article.id == 1)
    ).first()

    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'title': 'new title',
        'content': article_in_db.content,
        'tags': article_in_db.tags,
        'user_id': user.id,
        'date': article_date,
    }


def test_update_article_not_found(session, client, token, user):
    session.bulk_save_objects(ArticleFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.put(
        '/articles/100',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'new title'},
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Article not found'}


def test_delete_article(session, client, admin_token, user):
    session.bulk_save_objects(ArticleFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.delete(
        '/articles/1',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == 200
    assert response.json() == {'detail': 'Article deleted'}


def test_delete_article_not_found(session, client, admin_token, user):
    session.bulk_save_objects(ArticleFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.delete(
        '/articles/100',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Article not found'}


def test_delete_article_non_admin(session, client, token, user):
    session.bulk_save_objects(ArticleFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.delete(
        '/articles/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 403
    assert response.json() == {'detail': 'Not enough permissions'}
