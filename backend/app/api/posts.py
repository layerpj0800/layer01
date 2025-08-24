from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import require_role, require_subscriber
from app.core.database import get_session
from app.models.post import Post
from app.schemas.post import PostCreate, PostRead

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[PostRead])
async def list_posts(
    post_type: str | None = None,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_subscriber),
):
    query = select(Post)
    if post_type:
        query = query.where(Post.type == post_type)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("/", response_model=PostRead)
async def create_post(
    payload: PostCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_role("creator")),
):
    post = Post(**payload.dict(), author_id=user.id)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


@router.put("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: int,
    payload: PostCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_role("creator")),
):
    post = await session.get(Post, post_id)
    if post is None or post.author_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    for field, value in payload.dict().items():
        setattr(post, field, value)
    await session.commit()
    await session.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_role("creator")),
):
    post = await session.get(Post, post_id)
    if post is None or post.author_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    await session.delete(post)
    await session.commit()
