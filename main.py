from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()


# Define a Pydantic model for Post data
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# Store posts in a list
all_posts = [
    {
        "id": 1,
        "title": "School Matter",
        "content": "FUTO has resumed Her academic session..."
    },
    {
        "id": 2,
        "title": "Genesis",
        "content": "This is the beginning of the end"
    }
]


# Function to find a post by its ID
def find_post(post_id):
    for post in all_posts:
        if post['id'] == post_id:
            return post


# Root endpoint, returns a simple message
@app.get("/")
async def root():
    return {"message": "Hello World"}


# Create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.dict()
    # Generate a random ID for the new post
    post_id = randrange(0, 100000000000)
    post_dict['id'] = post_id
    all_posts.append(post_dict)
    return {"data": post_dict}


# Get all posts
@app.get("/posts")
def get_posts():
    return {"data": all_posts}


# Get a specific post by ID
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    return {"post_details": post}


# Update a post by ID
@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    post_dict = updated_post.dict()
    post_dict['id'] = id
    # Find the index of the post and update it
    index = all_posts.index(post)
    all_posts[index] = post_dict
    return {"data": post_dict}

# Delete a post by ID


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    all_posts.remove(post)
