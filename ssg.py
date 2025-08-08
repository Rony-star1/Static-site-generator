import os
import sys
import argparse
import shutil
import yaml
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from xml.sax.saxutils import escape

def load_config(config_path='config.yaml'):
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_theme_css(theme_name, theme_dir='themes'):
    css_path = os.path.join(theme_dir, theme_name, 'style.css')
    return css_path if os.path.exists(css_path) else None

def get_markdown_files(content_dir='content'):
    md_files = []
    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def parse_markdown(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    md = markdown.Markdown(extensions=['meta'])
    html = md.convert(text)
    meta = {key: md.Meta[key][0] if key in md.Meta else '' for key in md.Meta}
    return html, meta

def render_html(md_files, env, config, css_path, output_dir):
    posts = []
    for md_file in md_files:
        html_content, meta = parse_markdown(md_file)
        rel_path = os.path.relpath(md_file, 'content')
        url = rel_path.replace('.md', '.html').replace('\\', '/')
        title = meta.get('title', os.path.splitext(os.path.basename(md_file))[0])
        date = meta.get('date', '')
        posts.append({'title': title, 'date': date, 'url': url, 'content': html_content, 'meta': meta})

        # Choose template
        template_name = 'post.html' if 'blog/' in rel_path else 'page.html'
        template = env.get_template(template_name if template_name in env.list_templates() else 'base.html')

        rendered = template.render(
            config=config,
            content=html_content,
            title=title,
            date=date,
            css_path=css_path,
            posts=posts
        )

        output_path = os.path.join(output_dir, url)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered)

    # Generate index.html
    template = env.get_template('index.html')
    rendered = template.render(
        config=config,
        posts=[p for p in posts if 'blog/' in p['url']],
        css_path=css_path
    )
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(rendered)
    return posts

def copy_theme_assets(theme_name, output_dir, theme_dir='themes'):
    src = os.path.join(theme_dir, theme_name)
    dst = os.path.join(output_dir, 'assets')
    if os.path.exists(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)

def generate_rss(posts, config, output_dir):
    items = ""
    for post in posts:
        if not post['url'].startswith('blog/'):
            continue
        items += f"""
        <item>
            <title>{escape(post['title'])}</title>
            <link>{config['site_url'].rstrip('/')}/{post['url']}</link>
            <pubDate>{post['date']}</pubDate>
            <description>{escape(post['content'][:200])}</description>
        </item>
        """
    rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
      <channel>
        <title>{escape(config.get('site_title', 'My Site'))}</title>
        <link>{escape(config['site_url'])}</link>
        <description>{escape(config.get('site_description', ''))}</description>
        {items}
      </channel>
    </rss>
    """
    with open(os.path.join(output_dir, 'rss.xml'), 'w', encoding='utf-8') as f:
        f.write(rss)

def copy_static_files(static_dir, output_dir):
    if os.path.exists(static_dir):
        shutil.copytree(static_dir, os.path.join(output_dir, 'static'), dirs_exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='Static Site Generator')
    parser.add_argument('--config', default='config.yaml', help='Path to config file')
    parser.add_argument('--output', default='output', help='Output directory')
    parser.add_argument('--theme', default=None, help='Theme name (overrides config)')
    args = parser.parse_args()

    config = load_config(args.config)
    theme_name = args.theme or config.get('theme', 'default')
    css_path = get_theme_css(theme_name)
    output_dir = args.output

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    env = Environment(loader=FileSystemLoader('templates'))
    md_files = get_markdown_files('content')
    posts = render_html(md_files, env, config, css_path, output_dir)
    copy_theme_assets(theme_name, output_dir)
    if os.path.exists('static'):
        copy_static_files('static', output_dir)
    generate_rss(posts, config, output_dir)

    # Add simple search JS
    shutil.copyfile('search.js', os.path.join(output_dir, 'search.js'))

if __name__ == "__main__":
    main()