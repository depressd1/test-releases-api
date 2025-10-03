from fastapi import APIRouter
from schemas.releases import ReleaseCreate, ReleaseUpdate
from services.github_client import github_client

router = APIRouter()

@router.get("/")
def list_releases():
    return github_client.list_releases()

@router.get("/{release_id}")
def get_release(release_id: int):
    return github_client.get_release(release_id)

@router.post("/")
def create_release(release: ReleaseCreate):
    return github_client.create_release(release.tag_name, release.name, release.body)

@router.patch("/{release_id}")
def update_release(release_id: int, release: ReleaseUpdate):
    return github_client.update_release(release_id, release.name, release.body)

@router.delete("/{release_id}")
def delete_release(release_id: int):
    return github_client.delete_release(release_id)
