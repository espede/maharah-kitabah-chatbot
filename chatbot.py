#!/usr/bin/env python3
"""
Chatbot Pembelajaran Maharah Kitabah
=====================================
Chatbot interaktif untuk belajar keterampilan menulis bahasa Arab (مهارة الكتابة).
Mengintegrasikan API dari https://chat.b.ai

Fitur:
- Mode belajar: Penjelasan konsep, latihan menulis, koreksi otomatis
- Mode kuis: Tes pemahaman maharah kitabah
- Dukungan teks Arab (UTF-8)
- Interface terminal yang interaktif dengan Rich
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.text import Text
from rich.theme import Theme
from rich import box

# Load environment variables
load_dotenv()

# Initialize Rich console with custom theme
custom_theme = Theme({
    "info": "cyan",
    "success": "green",
    "warning": "yellow",
    "error": "red bold",
    "arabic": "bold white on blue",
    "menu": "bold magenta",
})
console = Console(theme=custom_theme)

# B.AI API Configuration
BAI_API_BASE = "https://chat.b.ai/v1"
BAI_API_KEY = os.getenv("BAI_API_KEY", "")
DEFAULT_MODEL = os.getenv("BAI_MODEL", "openai/gpt-4o-mini")

# System prompt untuk chatbot Maharah Kitabah
SYSTEM_PROMPT = """أنت معلم متخصص في مهارة الكتابة العربية (Maharah Kitabah). 
Anda adalah chatbot pembelajaran yang ahli dalam **Maharah Kitabah** (مهارة الكتابة) - keterampilan menulis bahasa Arab.

**Peran Anda:**
1. Mengajar konsep-konsep dasar maharah kitabah (ejaan, kaligrafi, tanda baca/harakat)
2. Memberikan latihan menulis bahasa Arab dari tingkat dasar sampai lanjutan
3. Mengoreksi tulisan bahasa Arab yang dikirim pengguna
4. Menjelasan perbedaan bentuk huruf Arab (awal, tengah, akhir, terpisah)
5. Memberikan kuis dan evaluasi pemahaman

**Aturan:**
- Selalu jawab dalam Bahasa Indonesia dengan contoh dalam huruf Arab
- Gunakan format yang rapi: huruf Arab, transliterasi, dan terjemahan
- Bersabar dan mendukung seperti guru yang baik
- Berikan pujian ketika pengguna berhasil
- Koreksi kesalahan dengan lembut dan konstruktif
- Jika pengguna bertanya di luar topik maharah kitabah, arahkan kembali dengan sopan

**Topik yang bisa dibahas:**
- حروف الهجاء (Huruf Hijaiyah) dan bentuk-bentuknya
- الحركات (Harakat: Fathah, Kasrah, Dammah, Sukun, Tanwin)
- الكتابة بالتشكيل (Menulis dengan tanda baca)
- قواعد الكتابة (Kaidah penulisan bahasa Arab)
- الإملاء (Imla'/Ejaan)
- الخط العربي (Kaligrafi/Font Arab)
- الترقيم (Tanda baca/punctuation dalam bahasa Arab)

Mulai setiap percakapan dengan salam dan tanyakan tingkat kemampuan pengguna."""


class MaharahKitabahChatbot:
    """Chatbot pembelajaran Maharah Kitabah menggunakan B.AI API."""
    
    def __init__(self, api_key: str = "", model: str = ""):
        self.api_key = api_key or BAI_API_KEY
        self.model = model or DEFAULT_MODEL
        self.api_url = f"{BAI_API_BASE}/chat/completions"
        self.conversation_history = []
        self.session_active = True
        
        if not self.api_key:
            console.print("[error]❌ API Key B.AI belum diatur![/error]")
            console.print("[info]Atur di file .env: BAI_API_KEY=your_api_key[/info]")
            console.print("[info]Dapatkan API key di: https://chat.b.ai[/info]")
            sys.exit(1)
    
    def _get_headers(self) -> dict:
        """Headers untuk API request."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
    
    def _build_payload(self, user_message: str, stream: bool = False) -> dict:
        """Build request payload untuk B.AI API."""
        # Tambahkan system prompt di awal
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Tambahkan history percakapan
        messages.extend(self.conversation_history)
        
        # Tambahkan pesan user
        messages.append({"role": "user", "content": user_message})
        
        return {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2048,
            "stream": stream,
        }
    
    def send_message(self, user_message: str) -> str:
        """Kirim pesan ke B.AI API dan dapatkan respons."""
        try:
            payload = self._build_payload(user_message, stream=False)
            response = requests.post(
                self.api_url,
                headers=self._get_headers(),
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            
            data = response.json()
            assistant_message = data["choices"][0]["message"]["content"]
            
            # Simpan ke history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            # Batasi history (max 20 pesan = 10 pasang)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return assistant_message
            
        except requests.exceptions.HTTPError as e:
            error_detail = ""
            try:
                error_data = e.response.json()
                error_detail = error_data.get("error", {}).get("message", str(e))
            except:
                error_detail = str(e)
            return f"❌ Error API: {error_detail}"
        except requests.exceptions.ConnectionError:
            return "❌ Gagal terhubung ke server B.AI. Periksa koneksi internet."
        except requests.exceptions.Timeout:
            return "❌ Request timeout. Coba lagi."
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def stream_message(self, user_message: str) -> str:
        """Kirim pesan dengan streaming response."""
        try:
            payload = self._build_payload(user_message, stream=True)
            response = requests.post(
                self.api_url,
                headers=self._get_headers(),
                json=payload,
                stream=True,
                timeout=60,
            )
            response.raise_for_status()
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str.strip() == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            delta = data.get("choices", [{}])[0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                full_response += content
                                console.print(content, end="", highlight=False)
                        except json.JSONDecodeError:
                            continue
            
            print()  # Newline after streaming
            
            # Simpan ke history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": full_response})
            
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return full_response
            
        except Exception as e:
            return f"\n❌ Error: {str(e)}"
    
    def show_welcome(self):
        """Tampilkan pesan selamat datang."""
        welcome_art = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     مرحباً بكم في تعلم مهارة الكتابة                        ║
║                                                              ║
║     📝 Chatbot Pembelajaran Maharah Kitabah                  ║
║     ✍️  Keterampilan Menulis Bahasa Arab                      ║
║                                                              ║
║     Powered by B.AI API                                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        console.print(welcome_art, style="bold cyan")
        
        menu = """
**Menu Mode Pembelajaran:**
  `1` 📚 **Belajar** — Penjelasan konsep maharah kitabah
  `2` ✍️  **Latihan** — Praktik menulis bahasa Arab
  `3` 📝 **Kuis** — Tes pemahaman Anda
  `4` 🔍 **Koreksi** — Kirim tulisan untuk dikoreksi
  `5` 💬 **Bebas** — Tanya apa saja tentang menulis Arab
  `6` 📊 **Progres** — Lihat ringkasan pembelajaran
  `0` 🚪 **Keluar**

Ketik angka untuk pilih mode, atau langsung ketik pertanyaan.
"""
        console.print(Panel(menu, title="🎓 Menu", border_style="cyan", box=box.ROUNDED))
    
    def get_mode_prompt(self, mode: str) -> str:
        """Dapatkan prompt khusus berdasarkan mode."""
        mode_prompts = {
            "1": "Saya ingin belajar konsep dasar maharah kitabah. Jelaskan topik yang perlu saya pelajari dan mulai dari level dasar.",
            "2": "Saya ingin latihan menulis bahasa Arab. Berikan saya latihan menulis dengan tingkat kesulitan yang bertahap.",
            "3": "Saya ingin mengerjakan kuis tentang maharah kitabah. Berikan saya 5 soal kuis dengan berbagai tingkat kesulitan.",
            "4": "Saya ingin mengirim tulisan bahasa Arab untuk dikoreksi. Bisakah Anda mengoreksi kesalahan ejaan dan tanda baca?",
            "6": "Tolong berikan ringkasan apa saja yang sudah saya pelajari dalam sesi ini dan berikan saran untuk perbaikan.",
        }
        return mode_prompts.get(mode, "")
    
    def run(self):
        """Jalankan chatbot interaktif."""
        self.show_welcome()
        
        # Kirim pesan pembuka
        console.print("\n[info]🤖 Menghubungkan ke B.AI...[/info]\n")
        opening = self.send_message(
            "Assalamualaikum! Saya adalah siswa baru yang ingin belajar maharah kitabah. "
            "Perkenalkan diri Anda dan tanyakan tingkat kemampuan saya."
        )
        console.print(Panel(Markdown(opening), title="🤖 Guru Kitabah", border_style="green", box=box.ROUNDED))
        
        while self.session_active:
            try:
                # Ambil input user
                console.print()
                user_input = Prompt.ask("[bold cyan]✍️  Anda[/bold cyan]")
                
                # Cek command khusus
                if user_input.strip() in ["0", "exit", "quit", "keluar", "bye"]:
                    farewell = self.send_message(
                        "Saya sudah selesai belajar untuk hari ini. "
                        "Berikan saya kesimpulan dan motivasi untuk terus belajar."
                    )
                    console.print(Panel(Markdown(farewell), title="👋 Sampai Jumpa", border_style="yellow"))
                    self.session_active = False
                    continue
                
                if user_input.strip() in ["1", "2", "3", "4", "5", "6"]:
                    mode_prompt = self.get_mode_prompt(user_input.strip())
                    if mode_prompt:
                        user_input = mode_prompt
                
                if user_input.strip() == "help":
                    self.show_welcome()
                    continue
                
                if not user_input.strip():
                    continue
                
                # Kirim pesan dan tampilkan respons (streaming)
                console.print()
                with console.status("[bold green]🤖 Berpikir...[/bold green]"):
                    pass  # Just a small visual delay
                
                console.print("[bold green]🤖 Guru Kitabah:[/bold green] ", end="")
                response = self.stream_message(user_input)
                
                if not response:
                    console.print("[error]Tidak ada respons dari server.[/error]")
                
            except KeyboardInterrupt:
                console.print("\n\n[warning]👋 Sampai jumpa! Semangat belajar! 📚[/warning]")
                self.session_active = False
            except EOFError:
                self.session_active = False


def main():
    """Entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Chatbot Pembelajaran Maharah Kitabah (مهارة الكتابة)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python chatbot.py                        # Jalankan dengan .env
  python chatbot.py --key YOUR_API_KEY     # Jalankan dengan API key langsung
  python chatbot.py --model openai/gpt-4o  # Gunakan model tertentu
        """
    )
    parser.add_argument("--key", "-k", help="B.AI API Key")
    parser.add_argument("--model", "-m", help="Model AI (default: openai/gpt-4o-mini)")
    
    args = parser.parse_args()
    
    chatbot = MaharahKitabahChatbot(
        api_key=args.key or "",
        model=args.model or "",
    )
    chatbot.run()


if __name__ == "__main__":
    main()
