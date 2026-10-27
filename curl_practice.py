
import requests


class APIClient:
    """Base class for API clients. Extend this for each specific API."""

    def __init__(self, base_url: str, default_headers: dict = None):

        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

        if default_headers:
             self.session.headers.update(default_headers) or {}

    def _url(self, path: str) -> str:
        """Combine base_url with a path."""

        return f"{self.base_url}/{path.lstrip('/')}"

    def _request(self, method: str, path: str, **kwargs):

        response = self.session.request(method, self._url(path), **kwargs)
        response.raise_for_status()
        return response

    def get(self, path: str, **kwargs):

        return self._request("GET", path, **kwargs)
        
    def post(self, path: str, **kwargs):
      
      return self._request("POST", path, **kwargs)

    def patch(self, path: str, **kwargs):
      
      return self._request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs):
       
       return self._request("DELETE", path, **kwargs)


class JSONPlaceholderClient(APIClient):
    """Client for https://jsonplaceholder.typicode.com"""

    def __init__(self):
          super().__init__(
            base_url="https://jsonplaceholder.typicode.com",
            default_headers={"Accept": "application/json"},
        )

    def get_user(self, user_id: int) -> dict:
        """Fetch a single user by ID."""

        return self.get(f"/users/{user_id}").json()

    def get_user_posts(self, user_id: int) -> list:
        """Fetch all posts for a specific user."""

        return self.get(
            f"/posts",
            params={"userId": user_id}
            ).json()

    def create_post(self, user_id: int, title: str, body: str) -> dict:
        """Create a new post (simulated). Returns the created post dict."""

        new_post = {
            "userId": user_id,
            "title": title,
            "body": body
        }
        
        response = self.post("/posts", json=new_post)
        return response.json()
    
    def search_posts(self, query: str) -> list:
        """
        Client-side filter: fetch all posts and return those whose title
        contains `query` (case-insensitive).
        """
        posts = self.get("/posts").json()
        needle = query.lower()
        return [p for p in posts if needle in p["title"].lower()]

# ============================================================
# Demo (runs when you execute this file)
# ============================================================
if __name__ == "__main__":
    client = JSONPlaceholderClient()


    print("1. User 5 profile:")

    user = client.get_user(5)
    print(f"   Name:  {user['name']}")
    print(f"   Email: {user['email']}")
    print(f"   City:  {user['address']['city']}")

   
    print("\n2. User 5's posts:")

    posts = client.get_user_posts(5)
    print(f"    Count: {len(posts)}")
    if posts:
            print(f"    First title: {posts[0]['title']}")


    print("\n3. Create a new post:")

    new_post = client.create_post(
            user_id=5,
            title="My first API client post",
            body="Created with the APIClient base class.",
        )
    print(f"   ID:    {new_post['id']}")
    print(f"   Title: {new_post['title']}")


  
    print("\n4. Search posts for 'qui':")
    
    matches = client.search_posts("qui")
    print(f"   Matches: {len(matches)}")
    for post in matches[:3]:
            print(f"   - {post['title']}")


