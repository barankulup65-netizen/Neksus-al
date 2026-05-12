import requests
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock

# Profesyonel Renk Paleti (ChatGPT Dark Mode)
C_BG = (20/255, 21/255, 23/255, 1)
C_SIDEBAR = (10/255, 10/255, 11/255, 1)
C_ACCENT = (56/255, 189/255, 248/255, 1) # Modern Mavi

Window.clearcolor = C_BG

class NexusPro(FloatLayout):
    def __init__(self, **kwargs):
        super(NexusPro, self).__init__(**kwargs)
        self.api_key = "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"
        self.selected_model = "llama-3.3-70b-versatile" # Varsayılan Model
        
        self.show_auth_screen()

    def show_auth_screen(self):
        self.clear_widgets()
        # Dikdörtgen ve Modern Kayıt Ekranı
        auth_box = BoxLayout(orientation='vertical', size_hint=(0.85, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5}, spacing=15)
        
        title = Label(text="NEXUS PRO", font_size='32sp', bold=True, color=C_ACCENT)
        desc = Label(text="Baran tarafından 2026'da geliştirildi.", font_size='14sp', color=(0.7, 0.7, 0.7, 1))
        
        self.user_field = TextInput(hint_text="Kullanıcı Adı", multiline=False, size_hint_y=None, height=55, background_color=(0.15, 0.15, 0.15, 1), foreground_color=(1,1,1,1))
        self.pass_field = TextInput(hint_text="Şifre", password=True, multiline=False, size_hint_y=None, height=55, background_color=(0.15, 0.15, 0.15, 1), foreground_color=(1,1,1,1))
        
        login_btn = Button(text="KAYIT OL / GİRİŞ YAP", size_hint_y=None, height=60, background_normal='', background_color=C_ACCENT, color=(0,0,0,1), bold=True)
        login_btn.bind(on_release=self.init_main_app)
        
        auth_box.add_widget(title); auth_box.add_widget(desc); auth_box.add_widget(self.user_field); auth_box.add_widget(self.pass_field); auth_box.add_widget(login_btn)
        self.add_widget(auth_box)

    def init_main_app(self, *args):
        self.clear_widgets()
        
        # 1. ÜST BAR (Model Seçme ve Menü Butonu)
        top_bar = BoxLayout(size_hint=(1, 0.08), pos_hint={'top': 1}, padding=10, spacing=10)
        
        self.menu_btn = Button(text="☰", size_hint_x=None, width=50, background_normal='', background_color=(0,0,0,0), font_size='24sp')
        self.menu_btn.bind(on_release=self.toggle_sidebar)
        
        # Model Seçme Butonları (Sıkıştırılmış / Büyük)
        self.model_btn = Button(text="Model: Llama 70B (Üst)", size_hint_x=0.4, background_color=(0.2, 0.2, 0.2, 1))
        self.model_btn.bind(on_release=self.change_model)

        top_bar.add_widget(self.menu_btn); top_bar.add_widget(self.model_btn)
        self.add_widget(top_bar)

        # 2. SOHBET ALANI
        self.chat_scroll = ScrollView(size_hint=(1, 0.75), pos_hint={'y': 0.15})
        self.chat_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=20, spacing=15)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('size_hint_y'))
        self.chat_scroll.add_widget(self.chat_layout)
        self.add_widget(self.chat_scroll)

        # 3. YAN MENÜ (SIDEBAR) - Başlangıçta gizli
        self.sidebar = BoxLayout(orientation='vertical', size_hint=(0.7, 1), pos_hint={'x': -0.7}, padding=20)
        with self.sidebar.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(10/255, 10/255, 11/255, 1)
            self.rect = Rectangle(size=self.sidebar.size, pos=self.sidebar.pos)
        self.sidebar.bind(size=self._update_rect, pos=self._update_rect)
        
        self.sidebar.add_widget(Label(text="Geçmiş Sohbetler", bold=True, size_hint_y=None, height=50))
        self.add_widget(self.sidebar)

        # 4. GİRİŞ ALANI
        input_box = BoxLayout(size_hint=(0.95, 0.08), pos_hint={'center_x': 0.5, 'y': 0.04}, spacing=10)
        self.msg_input = TextInput(hint_text="Mesajınızı buraya yazın...", multiline=False, background_color=(30/255, 30/255, 33/255, 1), foreground_color=(1,1,1,1), keyboard_suggestions=False)
        send_btn = Button(text="▶", size_hint_x=None, width=60, background_color=C_ACCENT)
        send_btn.bind(on_release=self.send_message)
        input_box.add_widget(self.msg_input); input_box.add_widget(send_btn)
        self.add_widget(input_box)

    def _update_rect(self, instance, value): self.rect.pos = instance.pos; self.rect.size = instance.size

    def toggle_sidebar(self, *args):
        target_x = 0 if self.sidebar.pos_hint['x'] < 0 else -0.7
        Animation(pos_hint={'x': target_x}, duration=0.3, t='out_quad').start(self.sidebar)

    def change_model(self, instance):
        if "70B" in instance.text:
            self.selected_model = "llama3-8b-8192"
            instance.text = "Model: Llama 8B (Hızlı/Küçük)"
        else:
            self.selected_model = "llama-3.3-70b-versatile"
            instance.text = "Model: Llama 70B (Zeki/Büyük)"

    def send_message(self, *args):
        query = self.msg_input.text
        if not query: return
        self.add_chat_bubble("Siz", query, (0.2, 0.2, 0.25, 1))
        self.msg_input.text = ""
        
        # Düşünme Aşaması (Düşünceyi okuma simülasyonu)
        self.thinking_label = self.add_chat_bubble("Nexus", "Düşünülüyor (Reasoning...)", (0.1, 0.1, 0.1, 1))
        Clock.schedule_once(lambda dt: self.get_response(query), 0.5)

    def add_chat_bubble(self, sender, text, color):
        bubble = Label(text=f"[b]{sender}:[/b] {text}", markup=True, size_hint_y=None, text_size=(Window.width * 0.8, None), padding=[15, 15], halign='left')
        bubble.bind(texture_size=bubble.setter('size'))
        self.chat_layout.add_widget(bubble)
        self.chat_scroll.scroll_y = 0
        return bubble

    def get_response(self, query):
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": self.selected_model, "messages": [{"role": "system", "content": "Sen Nexus'sun. Baran tarafından geliştirildin."},{"role": "user", "content": query}]})
            if r.status_code == 200:
                self.thinking_label.text = f"[b]Nexus:[/b] {r.json()['choices'][0]['message']['content']}"
        except:
            self.thinking_label.text = "[b]Nexus:[/b] Bağlantı hatası!"

class MainApp(App):
    def build(self): return NexusPro()

MainApp().run()
