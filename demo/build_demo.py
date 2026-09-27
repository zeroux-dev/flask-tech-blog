# ============================================================
#  TechBlog — static live-demo builder (GitHub Pages)
#  Author   : ZERO (Sobhan) — https://github.com/zeroux-dev
#  Telegram : @fesqhli  (https://t.me/fesqhli)
#  License  : MIT — keep this notice when you use or copy this code
#  Copyright (c) 2025-2026 ZERO (Sobhan)
# ============================================================
"""Renders the real Jinja templates with sample data into ../docs
so the project can be previewed on GitHub Pages without a server.
Run:  python demo/build_demo.py"""
import os, re, shutil, math
from datetime import datetime, timedelta
from types import SimpleNamespace as NS
from jinja2 import Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'docs')
NOW = datetime(2026, 9, 20, 14, 30)

# ---------------- sample data ----------------
def user(i, name, gender=None, email=None, days=60):
    return NS(id=i, username=name, gender=gender, email=email, phone=None, profile_pic=None,
              join_date=NOW - timedelta(days=days), last_login=NOW - timedelta(hours=i * 3),
              posts=[], comments=[], is_authenticated=True)

admin = user(1, 'admin', 'مرد', 'admin@techblog.dev', 200)
users = [admin, user(2, 'sara', 'زن', 'sara@mail.dev', 90), user(3, 'ali', 'مرد', 'ali@mail.dev', 75),
         user(4, 'maryam', 'زن', None, 40), user(5, 'reza', 'مرد', 'reza@mail.dev', 12)]
U = {u.username: u for u in users}

POSTS = [
    ('هوش مصنوعی مولد چطور برنامه‌نویسی را تغییر می‌دهد؟', 'هوش مصنوعی', 'admin', 'ai.jpg', 1840,
     'ابزارهای هوش مصنوعی مولد حالا بخشی از روزمره‌ی برنامه‌نویس‌ها شده‌اند. از تکمیل خودکار کد تا نوشتن تست و مستندات، این ابزارها سرعت توسعه را چند برابر کرده‌اند. اما کلید استفاده‌ی درست، شناخت محدودیت‌ها و بازبینی دقیق خروجی است. در این مقاله نگاهی می‌اندازیم به بهترین روش‌ها، اشتباهات رایج و آینده‌ی همکاری انسان و ماشین در تیم‌های نرم‌افزاری.'),
    ('راهنمای کامل Flask برای ساخت وبلاگ', 'برنامه‌نویسی', 'admin', 'flask.jpg', 1325,
     'فلسک یک فریم‌ورک سبک و قدرتمند پایتون است که برای ساخت وب‌اپلیکیشن‌ها از کوچک تا بزرگ مناسب است. در این آموزش قدم‌به‌قدم یک وبلاگ کامل با ثبت‌نام کاربران، پنل مدیریت، آپلود تصویر، سیستم لایک و کامنت و گزارش تخلف می‌سازیم و با SQLAlchemy به پایگاه داده PostgreSQL وصل می‌شویم.'),
    ('۱۰ ترفند امنیتی که هر توسعه‌دهنده باید بداند', 'امنیت', 'sara', 'security.jpg', 972,
     'امنیت از روز اول پروژه شروع می‌شود، نه بعد از هک شدن. هش کردن رمزها، اعتبارسنجی فایل‌های آپلودی، نگه داشتن کلیدهای مخفی خارج از کد، محدود کردن دسترسی‌ها و به‌روز نگه داشتن کتابخانه‌ها تنها بخشی از کارهایی است که باید انجام دهید.'),
    ('بررسی گوشی‌های پرچمدار ۲۰۲۶', 'گجت', 'ali', 'gadget.jpg', 2210,
     'امسال رقابت پرچمدارها بیش از همیشه داغ است. نمایشگرهای روشن‌تر، باتری‌های سیلیکون-کربن، دوربین‌های پریسکوپی و تراشه‌هایی با هسته‌های اختصاصی هوش مصنوعی. در این بررسی نقاط قوت و ضعف محبوب‌ترین مدل‌ها را کنار هم گذاشته‌ایم.'),
    ('طراحی رابط کاربری مدرن با Glassmorphism', 'طراحی وب', 'maryam', 'design.jpg', 815,
     'افکت شیشه‌ای یا Glassmorphism با پس‌زمینه‌های محو، حاشیه‌های نیمه‌شفاف و سایه‌های نرم، ظاهری لوکس و مدرن به رابط کاربری می‌دهد. در این مطلب یاد می‌گیریم چطور با چند خط CSS این سبک را پیاده کنیم بدون اینکه خوانایی قربانی شود.'),
    ('شروع کار با PostgreSQL در پروژه‌های پایتون', 'برنامه‌نویسی', 'reza', 'db.jpg', 640,
     'PostgreSQL یکی از پایدارترین و کامل‌ترین پایگاه‌های داده متن‌باز است. در این راهنما نصب، ساخت دیتابیس، اتصال با SQLAlchemy و چند نکته برای بهینه‌سازی کوئری‌ها را مرور می‌کنیم.'),
]
posts = []
for i, (t, cat, a, img, views, content) in enumerate(POSTS, 1):
    p = NS(id=i, title=t, category=cat, author=U[a], image_file=img, views=views, content=content,
           date_posted=NOW - timedelta(days=i * 3), comments=[], likes=[])
    U[a].posts.append(p); posts.append(p)

COMMENTS = [(1, 'sara', 'مقاله‌ی فوق‌العاده‌ای بود، مخصوصاً بخش محدودیت‌ها 👌'), (1, 'ali', 'به نظرم هنوز بازبینی انسانی حرف اول را می‌زند.'),
            (2, 'reza', 'با همین آموزش اولین پروژه‌ی فلسکم را بالا آوردم، ممنون!'), (2, 'maryam', 'لطفاً بخش استقرار روی سرور را هم اضافه کنید.'),
            (3, 'ali', 'نکته‌ی اعتبارسنجی فایل آپلودی خیلی کاربردی بود.'), (4, 'sara', 'منتظر بررسی دوربین‌ها هستیم!'),
            (5, 'reza', 'چه طراحی قشنگی 😍'), (6, 'admin', 'به‌زودی قسمت دوم منتشر می‌شود.')]
comments = []
for j, (pid, a, body) in enumerate(COMMENTS, 1):
    p = posts[pid - 1]
    c = NS(id=j, body=body, author=U[a], post=p, post_id=p.id, likes=[1] * (j % 4),
           date_posted=p.date_posted + timedelta(hours=j))
    p.comments.append(c); U[a].comments.append(c); comments.append(c)
for k, p in enumerate(posts):
    p.likes = [1] * (18 + k * 7)

reports = [NS(id=1, reason='اسپم', user=U['maryam'], comment=comments[1], comment_id=comments[1].id,
              date_reported=NOW - timedelta(hours=5))]
cats = sorted({p.category for p in posts})
stats = dict(users=len(users), posts=len(posts), comments=len(comments), views=sum(p.views for p in posts),
             reports_count=len(reports), categories_count=len(cats))

# ---------------- rendering ----------------
def url_for(endpoint, **kw):
    if endpoint == 'static': return '/static/' + kw['filename']
    return {'post_detail': f"/read/{kw.get('post_id')}", 'update_post': '/post/new', 'login': '/login'}.get(endpoint, '#')

class Req(NS):
    pass

def env_for(endpoint):
    env = Environment(loader=FileSystemLoader(os.path.join(ROOT, 'templates')))
    env.globals.update(url_for=url_for, get_flashed_messages=lambda **k: [], all_categories=cats,
                       current_user=admin, estimate_reading_time=lambda t: max(1, math.ceil(len(t.split()) / 200)),
                       request=NS(args={}, endpoint=endpoint, cookies={}))
    return env

ROUTES = [
    (r'^/\?.*$|^/$', 'index.html'), (r'^/read/(\d+)$', r'read-\1.html'), (r'^/login$', 'login.html'),
    (r'^/register$', 'register.html'), (r'^/logout$', 'index.html'), (r'^/post/new$', 'post-new.html'),
    (r'^/post/\d+/update$', 'post-new.html'), (r'^/admin/dashboard$', 'admin-dashboard.html'),
    (r'^/admin/users$', 'admin-users.html'), (r'^/admin/user/(\d+)$', r'admin-user-\1.html'),
    (r'^/admin/categories$', 'admin-categories.html'), (r'^/static/(.*)$', r'static/\1'),
]
def map_url(u):
    for pat, rep in ROUTES:
        if re.match(pat, u): return re.sub(pat, rep, u)
    return '#'

BANNER = '''
<div id="zero-demo-ribbon" style="position:fixed;bottom:16px;left:16px;z-index:9999;background:linear-gradient(135deg,#6d5dfc,#b58cff);color:#fff;padding:10px 16px;border-radius:14px;font:600 13px Vazirmatn,Tahoma,sans-serif;box-shadow:0 8px 24px rgba(80,60,200,.35);direction:rtl">
  🚀 دموی زنده · طراحی و توسعه: <a href="https://github.com/zeroux-dev" style="color:#fff;text-decoration:underline">ZERO</a> ·
  <a href="https://t.me/fesqhli" style="color:#fff">@fesqhli</a>
</div>
<script>
document.addEventListener('submit',function(e){e.preventDefault();alert('این یک دموی استاتیک است؛ فرم‌ها در نسخه‌ی اصلی Flask کار می‌کنند.\\nDeveloper: ZERO — t.me/fesqhli');},true);
</script>
'''

def write(name, tpl, endpoint, **ctx):
    html = env_for(endpoint).get_template(tpl).render(**ctx)
    html = re.sub(r'((?:href|src|action)=["\'])(/[^"\']*)', lambda m: m.group(1) + map_url(m.group(2)), html)
    html = re.sub(r"url\('(/static/[^']*)'\)", lambda m: "url('" + map_url(m.group(1)) + "')", html)
    html = html.replace('</body>', BANNER + '</body>')
    html = html.replace('<head>', '<head>\n    <meta name="description" content="TechBlog — Flask blog with admin panel. Live demo by ZERO (Sobhan), t.me/fesqhli">', 1)
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(html)

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, 'static', 'uploads'))
    shutil.copy(os.path.join(ROOT, 'static', 'style.css'), os.path.join(OUT, 'static'))
    for f in os.listdir(os.path.join(ROOT, 'demo', 'covers')):
        shutil.copy(os.path.join(ROOT, 'demo', 'covers', f), os.path.join(OUT, 'static', 'uploads', f))
    write('index.html', 'index.html', 'index', posts=posts, page_title='آخرین نوشته‌ها')
    for p in posts:
        write(f'read-{p.id}.html', 'post.html', 'post_detail', post=p, user_liked=p.id % 2 == 1)
    write('login.html', 'login.html', 'login')
    write('register.html', 'register.html', 'register')
    write('post-new.html', 'create_post.html', 'new_post', title='نوشتن پست')
    write('admin-dashboard.html', 'admin_dashboard.html', 'admin_dashboard', stats=stats, reports=reports,
          recent_users=list(reversed(users)), now=NOW)
    write('admin-users.html', 'admin_users.html', 'admin_users', users=users)
    for u in users:
        write(f'admin-user-{u.id}.html', 'admin_user_detail.html', 'admin_user_detail', user=u)
    write('admin-categories.html', 'admin_categories.html', 'admin_categories',
          categories=[(c, sum(p.category == c for p in posts)) for c in cats])
    open(os.path.join(OUT, '.nojekyll'), 'w').close()
    print('Demo built in', OUT)

if __name__ == '__main__':
    main()
