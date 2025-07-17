from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/") 
def home():
    return "Python API is running."

@app.route("/embed-links", methods=["GET"])
def embed_links_api():
    slug = request.args.get("slug")
    if not slug:
        return jsonify({"error": "Missing slug parameter"}), 400
    links = get_embed_links(slug)
    return jsonify(links)

def get_embed_links(slug):
    url = f"https://phimapi.com/phim/{slug}"
    headers = {
        "User-Agent": "Google"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        episodes = data.get("episodes", [])

        embed_links = []
        for server in episodes:
            server_name = server.get("server_name", "Unknown")
            for ep in server.get("server_data", []):
                ep_name = ep.get("name", "Unknown")
                link = ep.get("link_embed")
                if link:
                    embed_links.append({
                        "server": server_name,
                        "episode": ep_name,
                        "link_embed": link
                    })

        return embed_links

    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []

@app.route("/newest-slugs", methods=["GET"])
def newest_slugs_api():
    pages = int(request.args.get("pages", 1))
    slugs = get_newest_film_slugs(pages)
    return jsonify(slugs)

def get_newest_film_slugs(pages=1):
    headers = {
        "User-Agent": "Google"
    }
    slugs = []

    for i in range(1, pages + 4):
        url = f"https://phimapi.com/danh-sach/phim-moi-cap-nhat?page={i}"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            items = data.get("items", [])
            for item in items:
                slug = item.get("slug")
                if slug:
                    slugs.append(slug)
        except Exception as e:
            print(f"Failed to fetch page {i}: {e}")
    
    return slugs
@app.route("/embed-links-name", methods=["GET"])
def get_embed_links_name():
    slug = request.args.get("slug")
    if not slug:
        return jsonify({"error": "Missing slug parameter"}), 400

    url = f"https://phimapi.com/phim/{slug}"
    headers = {
        "User-Agent": "Google"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        name = data.get("movie", {}).get("origin_name", "Unknown")
        return jsonify({"name": name})
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return jsonify({"error": "Failed to fetch data"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
