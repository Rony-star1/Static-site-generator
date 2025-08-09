# Simple Static Site Generator

This is a simple, yet powerful, static site generator that converts Markdown files into a blog or portfolio website.

## Features

*   **Markdown to HTML Conversion**: Write your content in Markdown and the generator will convert it to HTML.
*   **Theming**: Easily customize the look and feel of your site with CSS-based themes.
*   **RSS Feed Generation**: An RSS feed is automatically generated for your blog posts.
*   **Basic Search**: A simple client-side search functionality is included.
*   **Metadata Support**: Add metadata like title and date to your Markdown files.

## Project Structure

```
.
├── content/            # Your Markdown files go here
│   └── blog/
│       └── first-post.md
├── output/             # The generated static site
├── static/             # Static assets that are copied to the output
├── templates/          # Jinja2 templates for rendering pages
│   ├── base.html
│   ├── index.html
│   ├── page.html
│   └── post.html
├── themes/             # Themes for your site
│   ├── default/
│   │   └── style.css
│   └── dark/
│       └── style.css
├── config.yaml         # Configuration file for your site
├── ssg.py              # The main static site generator script
└── search.js           # Javascript for the search functionality
```

## How to Use

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: I will create this `requirements.txt` file next)*

3.  **Add your content:**
    -   Create new Markdown files in the `content/` directory. For blog posts, place them in `content/blog/`.
    -   Add metadata to the top of your Markdown files:
        ```yaml
        ---
        title: My Awesome Post
        date: 2023-11-15
        ---
        ```

4.  **Configure your site:**
    -   Edit `config.yaml` to set your site's title, URL, description, and author.
    -   Choose a theme in `config.yaml` or create a new one in the `themes/` directory.

5.  **Generate your site:**
    ```bash
    python3 ssg.py
    ```
    -   To use a different theme than the one in the config, use the `--theme` flag:
        ```bash
        python3 ssg.py --theme dark
        ```

6.  **Preview your site:**
    -   Open the `output/index.html` file in your browser to see your generated site.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the terms of the LICENSE file.
*(Note: I will check the LICENSE file next)*
