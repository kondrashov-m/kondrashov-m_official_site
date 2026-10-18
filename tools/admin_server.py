"""Локальный помощник админки: раздаёт сайт и делает git commit + git push по кнопке.

Запуск — двойной щелчок по start_admin.bat в корне сайта (или `python tools/admin_server.py`).
Для автозапуска вместе с Windows (без окна): `pythonw tools/admin_server.py --silent`.
Откроется http://localhost:8787/admin.html. Браузер сам по себе не умеет запускать git,
поэтому кнопка «Закоммитить и запушить» во вкладке «Версия» обращается к этому скрипту.

Слушает только 127.0.0.1 — с других компьютеров недоступен. Для push используются
твои обычные учётные данные git (те же, что при ручном git push), отдельно ничего
настраивать не нужно. Только стандартная библиотека Python — ставить ничего не надо.
"""

import json
import os
import subprocess
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

HOST = "127.0.0.1"
PORT = int(os.environ.get("ADMIN_PORT", "8787"))
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_HOSTS = {"localhost", "127.0.0.1"}
_git_lock = threading.Lock()


class GitError(Exception):
    pass


def git(*args, timeout=120, raw=False):
    try:
        r = subprocess.run(
            ["git", *args], cwd=REPO, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except FileNotFoundError as e:
        raise GitError("Не найден git. Установи Git for Windows: https://git-scm.com/download/win") from e
    except subprocess.TimeoutExpired as e:
        raise GitError(f"git {args[0]} не ответил за {timeout} с. Проверь интернет.") from e
    if raw and r.returncode == 0:
        return r.stdout
    out = (r.stdout + r.stderr).strip()
    if r.returncode != 0:
        raise GitError(f"git {' '.join(args)}:\n{out}")
    return out


def repo_status():
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    files = []
    for line in git("status", "--porcelain", "-uall", "-z", raw=True).split("\0"):
        if len(line) < 4:
            continue
        code, path = line[:2], line[3:]
        files.append({"path": path, "code": code.strip() or "?"})
    try:
        ahead = int(git("rev-list", "--count", "@{u}..HEAD"))
    except GitError:
        ahead = 0
    last = git("log", "-1", "--pretty=%h %s")
    return {"branch": branch, "files": files, "ahead": ahead, "last": last}


def commit_and_push(message):
    """То же, что руками: git add . → git commit -m "…" → git pull → git push."""
    message = (message or "").strip()
    if not message:
        raise GitError("Впиши текст коммита.")
    log = []
    git("add", "-A")
    log.append("$ git add .")
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO,
                            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)).returncode != 0
    if staged:
        out = git("commit", "-m", message)
        log.append(f'$ git commit -m "{message}"\n' + out)
    elif repo_status()["ahead"] == 0:
        raise GitError("Нет изменений — коммитить и пушить нечего.")
    else:
        log.append("(новых изменений нет — пушу уже готовые коммиты)")
    out = git("pull", "--rebase", "--autostash", timeout=300)
    log.append("$ git pull\n" + out)
    try:
        out = git("push", timeout=600)
    except GitError as e:
        raise GitError("Коммит сделан, но git push не прошёл. Проверь интернет и вход в GitHub "
                       "(сделай один раз git push вручную из этой папки), потом нажми кнопку ещё раз.\n\n" + str(e))
    log.append("$ git push\n" + (out or "ok"))
    return {"log": "\n\n".join(log), "status": repo_status()}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=REPO, **kw)

    def log_message(self, fmt, *args):
        if self.path.startswith("/__git") and sys.stderr:
            sys.stderr.write("[admin] %s\n" % (fmt % args))

    def _origin_ok(self):
        # Защита от чужих сайтов: git-запросы принимаем только со страниц,
        # открытых с localhost (сам этот сервер, Live Server и т.п.).
        origin = self.headers.get("Origin")
        if origin is None:
            return True
        return urlparse(origin).hostname in ALLOWED_HOSTS

    def _cors(self):
        origin = self.headers.get("Origin")
        if origin and urlparse(origin).hostname in ALLOWED_HOSTS:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Admin")
            self.send_header("Vary", "Origin")

    def _json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        if not self.path.startswith("/__git"):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_OPTIONS(self):
        if not self.path.startswith("/__git") or not self._origin_ok():
            self.send_response(403); self.end_headers(); return
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/__git/ping"):
            # Безопасная проверка «помощник запущен?» — для админки, открытой файлом (file://)
            body = b'{"ok": true, "port": %d}' % PORT
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path.startswith("/__git/"):
            if not self._origin_ok():
                return self._json(403, {"error": "Запрос не с localhost"})
            try:
                with _git_lock:
                    return self._json(200, repo_status())
            except GitError as e:
                return self._json(500, {"error": str(e)})
        return super().do_GET()

    def do_POST(self):
        if self.path != "/__git/commit-push":
            return self._json(404, {"error": "not found"})
        if not self._origin_ok() or self.headers.get("X-Admin") != "1":
            return self._json(403, {"error": "Запрос не с localhost"})
        try:
            length = int(self.headers.get("Content-Length") or 0)
            data = json.loads(self.rfile.read(length) or b"{}")
            with _git_lock:
                result = commit_and_push(data.get("message"))
            return self._json(200, result)
        except GitError as e:
            return self._json(500, {"error": str(e)})
        except (ValueError, TypeError) as e:
            return self._json(400, {"error": "Плохой запрос: " + str(e)})


def main():
    silent = "--silent" in sys.argv  # режим автозагрузки: без окна и без открытия браузера
    try:
        server = ThreadingHTTPServer((HOST, PORT), Handler)
    except OSError:
        url = f"http://localhost:{PORT}/admin.html"
        print(f"Порт {PORT} занят — похоже, админка уже запущена. Открываю {url}")
        if not silent:
            webbrowser.open(url)
        return
    url = f"http://localhost:{PORT}/admin.html"
    print(f"Админка: {url}\nПапка сайта: {REPO}\nЗакрой это окно, чтобы остановить сервер.")
    if not silent:
        threading.Timer(0.7, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
