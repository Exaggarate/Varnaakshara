#!/usr/bin/env python3
"""
Varnaakshara Writer — Python Bridge Server

A lightweight HTTP server that wraps the Varnaakshara TransliterationEngine,
providing endpoints for transliteration, script conversion, ANSI conversion,
spell-checking, and related tools.

Spawned by the Electron main process on app start.
Runs on http://127.0.0.1:5111
"""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

# Add the engine to the Python path
ENGINE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'core', 'engine')
sys.path.insert(0, os.path.abspath(ENGINE_DIR))

# Try to import the transliteration engine
engine = None
try:
    from transliteration import TransliterationEngine
    engine = TransliterationEngine()
    print("[Bridge] TransliterationEngine loaded successfully")
except ImportError as e:
    print(f"[Bridge] Warning: Could not import TransliterationEngine: {e}")
    print("[Bridge] Running in stub mode — transliteration features will return errors")
except Exception as e:
    print(f"[Bridge] Warning: Error initializing TransliterationEngine: {e}")
    print("[Bridge] Running in stub mode")


def require_engine(func):
    """Decorator that checks if the engine is available."""
    def wrapper(self, data):
        if engine is None:
            return {"error": "TransliterationEngine not available. Check engine installation."}
        return func(self, data)
    return wrapper


class BridgeHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the bridge server."""

    def log_message(self, format, *args):
        """Override to prefix log messages."""
        print(f"[Bridge] {format % args}")

    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _read_json(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return {}
        raw = self.rfile.read(content_length)
        return json.loads(raw.decode('utf-8'))

    def _respond(self, data, status=200):
        self._set_headers(status)
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self._set_headers(204)

    def do_GET(self):
        if self.path == '/health':
            self._respond({
                "status": "ok",
                "engine_loaded": engine is not None,
            })
        else:
            self._respond({"error": "Not found"}, 404)

    def do_POST(self):
        try:
            data = self._read_json()
        except (json.JSONDecodeError, Exception) as e:
            self._respond({"error": f"Invalid JSON: {e}"}, 400)
            return

        routes = {
            '/transliterate': self.handle_transliterate,
            '/convert-script': self.handle_convert_script,
            '/to-ansi': self.handle_to_ansi,
            '/from-ansi': self.handle_from_ansi,
            '/to-iso15919': self.handle_to_iso15919,
            '/reverse': self.handle_reverse,
            '/spell-check': self.handle_spell_check,
            '/word-count': self.handle_word_count,
        }

        handler = routes.get(self.path)
        if handler:
            try:
                result = handler(data)
                self._respond(result)
            except Exception as e:
                self._respond({"error": str(e)}, 500)
        else:
            self._respond({"error": f"Unknown endpoint: {self.path}"}, 404)

    # ── Endpoint Handlers ──────────────────────────────────────────────────

    @require_engine
    def handle_transliterate(self, data):
        """Transliterate text using the specified scheme."""
        text = data.get('text', '')
        language = data.get('language', 'kannada')
        scheme = data.get('scheme', 'baraha')
        result = engine.transliterate(text, language=language, scheme=scheme)
        return {"result": result}

    @require_engine
    def handle_convert_script(self, data):
        """Convert text from one Indian script to another."""
        text = data.get('text', '')
        from_lang = data.get('from_lang', 'kannada')
        to_lang = data.get('to_lang', 'devanagari')
        result = engine.convert_script(text, from_lang=from_lang, to_lang=to_lang)
        return {"result": result}

    @require_engine
    def handle_to_ansi(self, data):
        """Convert Unicode text to ANSI encoding for a specific font family."""
        text = data.get('text', '')
        language = data.get('language', 'kannada')
        font_family = data.get('font_family', 'nudi')
        result = engine.to_ansi(text, language=language, font_family=font_family)
        return {"result": result}

    @require_engine
    def handle_from_ansi(self, data):
        """Convert ANSI-encoded text to Unicode."""
        text = data.get('text', '')
        language = data.get('language', 'kannada')
        font_family = data.get('font_family', 'nudi')
        result = engine.from_ansi(text, language=language, font_family=font_family)
        return {"result": result}

    @require_engine
    def handle_to_iso15919(self, data):
        """Convert text to ISO 15919 romanization."""
        text = data.get('text', '')
        language = data.get('language', 'kannada')
        result = engine.to_iso15919(text, language=language)
        return {"result": result}

    @require_engine
    def handle_reverse(self, data):
        """Reverse transliterate (Indic → Latin/scheme)."""
        text = data.get('text', '')
        language = data.get('language', 'kannada')
        result = engine.reverse_transliterate(text, language=language)
        return {"result": result}

    def handle_spell_check(self, data):
        """Basic spell-check. Returns suggestions for misspelled words."""
        text = data.get('text', '')
        language = data.get('language', 'kannada')

        if engine and hasattr(engine, 'spell_check'):
            result = engine.spell_check(text, language=language)
            return {"result": result}

        # Stub: spell check not yet implemented in engine
        words = text.split()
        return {
            "result": {
                "word_count": len(words),
                "errors": [],
                "message": "Spell check not yet implemented for this language."
            }
        }

    def handle_word_count(self, data):
        """Count words, characters, sentences, and paragraphs in text."""
        text = data.get('text', '')
        words = text.split()
        chars = len(text)
        chars_no_spaces = len(text.replace(' ', '').replace('\n', '').replace('\t', ''))
        sentences = text.count('.') + text.count('!') + text.count('?') + text.count('।') + text.count('॥')
        paragraphs = len([p for p in text.split('\n\n') if p.strip()])

        return {
            "result": {
                "words": len(words),
                "characters": chars,
                "characters_no_spaces": chars_no_spaces,
                "sentences": max(sentences, 1) if text.strip() else 0,
                "paragraphs": max(paragraphs, 1) if text.strip() else 0,
            }
        }


def main():
    port = int(os.environ.get('BRIDGE_PORT', 5111))
    server = HTTPServer(('127.0.0.1', port), BridgeHandler)
    print(f"[Bridge] Varnaakshara bridge server running on http://127.0.0.1:{port}")
    print(f"[Bridge] Engine dir: {os.path.abspath(ENGINE_DIR)}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Bridge] Shutting down...")
        server.server_close()


if __name__ == '__main__':
    main()
