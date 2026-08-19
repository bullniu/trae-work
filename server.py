"""
焊接工艺评定系统 HTTP 服务
- 提供静态文件服务（index.html 等）
- 提供 /api/gen-pqr 接口：接收 JSON 数据，填充 PQR 模板，返回 docx
"""
import json, os, io, traceback
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import quote

import fill_pqr_template as filler

ROOT = "/workspace"

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/gen-pqr':
            return self._gen_pqr()
        self.send_error(404, 'Not Found')

    def _gen_pqr(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            raw = self.rfile.read(length) if length else b''
            data = json.loads(raw.decode('utf-8')) if raw else {}

            # 输出文件名
            pqr = data.get('pqrForm', {})
            pqr_no = (pqr.get('pqrNo') or 'PQR').strip() or 'PQR'
            out_name = f"{pqr_no}_焊接工艺评定.docx"
            out_path = os.path.join(ROOT, out_name)

            # 填充模板
            filler.fill_template(data, out_path)

            with open(out_path, 'rb') as f:
                content = f.read()

            self.send_response(200)
            self._cors()
            self.send_header('Content-Type',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            self.send_header('Content-Disposition',
                f"attachment; filename*=UTF-8''{quote(out_name)}")
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            print(f"[OK] 生成报告: {out_name} ({len(content)} bytes)")
        except Exception as e:
            traceback.print_exc()
            msg = json.dumps({'error': str(e)}).encode('utf-8')
            self.send_response(500)
            self._cors()
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)

if __name__ == '__main__':
    port = 8090
    srv = HTTPServer(('0.0.0.0', port), Handler)
    print(f"服务启动: http://localhost:{port}/  (API: POST /api/gen-pqr)")
    srv.serve_forever()
