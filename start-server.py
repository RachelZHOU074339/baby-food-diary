#!/usr/bin/env python3
"""一键启动 PWA 本地服务器"""
import http.server
import socket
import os
import webbrowser

PORT = 8080
DIR = os.path.dirname(os.path.abspath(__file__))

# Get local IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect(('10.254.254.254', 1))
    local_ip = s.getsockname()[0]
except:
    local_ip = '127.0.0.1'
finally:
    s.close()

os.chdir(DIR)

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # quiet

print("=" * 50)
print("  🍼 辣堡辅食日记 PWA 服务器已启动")
print("=" * 50)
print()
print("  📱 手机浏览器打开以下链接：")
print()
print(f"     http://{local_ip}:{PORT}")
print()
print("  ⚠️  如果弹出 Windows 防火墙提示，请点「允许访问」")
print("  ⚠️  手机和电脑必须连接同一个 Wi-Fi")
print()
print("  按 Ctrl+C 停止服务器")
print("=" * 50)
print()

# Open browser on PC
webbrowser.open(f'http://{local_ip}:{PORT}')

with http.server.HTTPServer(('0.0.0.0', PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
