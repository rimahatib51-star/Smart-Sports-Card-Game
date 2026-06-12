import sysimport randomfrom dataclasses import dataclassfrom typing import Dict, List, Optional

from PyQt5.QtCore import Qtfrom PyQt5.QtGui import QPixmapfrom PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,QGridLayout, QFrame, QStackedWidget)



TURN_ORDER = ["Futbol", "Basketbol", "Voleybol"]

@dataclassclass Kart:ad: strbrans: strtakim: strresim: strenerji: intseviye: intdayaniklilik: intozellikler: Dict[str, int]

def performans_hesapla(self, secilen_ozellik: str) -> int:
    temel = self.ozellikler.get(secilen_ozellik, 0)

    if self.enerji > 70:
        enerji_cezasi = 0
    elif 40 <= self.enerji <= 70:
        enerji_cezasi = int(temel * 0.10)
    elif 0 < self.enerji < 40:
        enerji_cezasi = int(temel * 0.20)
    else:
        return 0

    seviye_bonus = (self.seviye - 1) * 5
    return max(0, temel - enerji_cezasi + seviye_bonus)

def enerji_guncelle(self, sonuc: str):
    if sonuc == "win":
        self.enerji = max(0, self.enerji - 5)
    elif sonuc == "lose":
        self.enerji = max(0, self.enerji - 10)
    else:
        self.enerji = max(0, self.enerji - 3)

class Oyuncu:def init(self, ad: str, kartlar: List[Kart]):self.ad = adself.kartlar = kartlarself.skor = 0

def uygun_kartlar(self, brans: str) -> List[Kart]:
    return [k for k in self.kartlar if k.brans == brans and k.enerji > 0]

def kart_sec(self, brans: str) -> Optional[Kart]:
    uygun = self.uygun_kartlar(brans)
    if not uygun:
        return None
    return random.choice(uygun)

class Bilgisayar(Oyuncu):def kart_sec(self, brans: str) -> Optional[Kart]:uygun = self.uygun_kartlar(brans)if not uygun:return None

    en_iyi = None
    en_iyi_ortalama = -1
    for kart in uygun:
        ortalama = sum(kart.ozellikler.values()) / len(kart.ozellikler)
        guncel = ortalama + (kart.seviye - 1) * 5
        if guncel > en_iyi_ortalama:
            en_iyi_ortalama = guncel
            en_iyi = kart
    return en_iyi

class OyunYonetici:def init(self, kullanici: Oyuncu, bilgisayar: Bilgisayar):self.kullanici = kullaniciself.bilgisayar = bilgisayarself.tur_no = 0

    self.kullanici_karti = None
    self.bilgisayar_karti = None
    self.secili_ozellik = ""
    self.kullanici_puan = 0
    self.bilgisayar_puan = 0
    self.sonuc_metni = "Oyuna başlamak için butona bas."

def aktif_brans(self) -> str:
    return TURN_ORDER[self.tur_no % len(TURN_ORDER)]

def uygun_ozellikler(self, brans: str) -> List[str]:
    if brans == "Futbol":
        return ["Penaltı", "Serbest Vuruş", "Kaleci Karşı Karşıya"]
    elif brans == "Basketbol":
        return ["Üçlük", "İkilik", "Serbest Atış"]
    else:
        return ["Servis", "Blok", "Smaç"]

def tur_oyna(self):
    brans = self.aktif_brans()

    self.kullanici_karti = self.kullanici.kart_sec(brans)
    self.bilgisayar_karti = self.bilgisayar.kart_sec(brans)

    if self.kullanici_karti is None and self.bilgisayar_karti is None:
        self.sonuc_metni = f"{brans} turu atlandı. İki tarafta da uygun kart yok."
        self.tur_no += 1
        return

    if self.kullanici_karti is None:
        self.bilgisayar.skor += 8
        self.sonuc_metni = f"{brans} turu: sende uygun kart yok. Bilgisayar hükmen kazandı."
        self.tur_no += 1
        return

    if self.bilgisayar_karti is None:
        self.kullanici.skor += 8
        self.sonuc_metni = f"{brans} turu: bilgisayarda uygun kart yok. Sen hükmen kazandın."
        self.tur_no += 1
        return

    self.secili_ozellik = random.choice(self.uygun_ozellikler(brans))
    self.kullanici_puan = self.kullanici_karti.performans_hesapla(self.secili_ozellik)
    self.bilgisayar_puan = self.bilgisayar_karti.performans_hesapla(self.secili_ozellik)

    if self.kullanici_puan > self.bilgisayar_puan:
        self.kullanici.skor += 10
        self.kullanici_karti.enerji_guncelle("win")
        self.bilgisayar_karti.enerji_guncelle("lose")
        sonuc = "Sen kazandın"
    elif self.bilgisayar_puan > self.kullanici_puan:
        self.bilgisayar.skor += 10
        self.kullanici_karti.enerji_guncelle("lose")
        self.bilgisayar_karti.enerji_guncelle("win")
        sonuc = "Bilgisayar kazandı"
    else:
        self.kullanici_karti.enerji_guncelle("draw")
        self.bilgisayar_karti.enerji_guncelle("draw")
        sonuc = "Berabere"

    self.sonuc_metni = (
        f"Tur: {brans}\n"
        f"Özellik: {self.secili_ozellik}\n"
        f"{self.kullanici_karti.ad}: {self.kullanici_puan}\n"
        f"{self.bilgisayar_karti.ad}: {self.bilgisayar_puan}\n"
        f"Sonuç: {sonuc}"
    )

    self.tur_no += 1



class StatBox(QFrame):def init(self, accent: str):super().init()self.title = QLabel("STAT")self.value = QLabel("0")

    self.title.setStyleSheet("color:#8DA3BF; font-size:10px; font-weight:700;")
    self.value.setStyleSheet("color:white; font-size:24px; font-weight:900;")

    layout = QVBoxLayout()
    layout.setContentsMargins(12, 10, 12, 10)
    layout.setSpacing(6)
    layout.addWidget(self.title)
    layout.addWidget(self.value)
    self.setLayout(layout)

    self.setStyleSheet(f"""
        QFrame {{
            background-color:#101A2D;
            border:1px solid {accent};
            border-radius:14px;
        }}
    """)

def set_data(self, title: str, value: int):
    self.title.setText(title.upper())
    self.value.setText(str(value))

class PlayerCardWidget(QFrame):def init(self, accent: str):super().init()self.accent = accentself.setFixedSize(300, 620)

    self.setStyleSheet(f"""
        QFrame {{
            background-color:#040811;
            border:2px solid {accent};
            border-radius:22px;
        }}
    """)

    self.top_label = QLabel("PLAYER CARD")
    self.top_label.setAlignment(Qt.AlignCenter)
    self.top_label.setStyleSheet("color:#BFD0E5; font-size:13px; font-weight:700;")

    self.image_label = QLabel("NO IMAGE")
    self.image_label.setAlignment(Qt.AlignCenter)
    self.image_label.setFixedHeight(280)
    self.image_label.setStyleSheet("""
        background-color:#0B1324;
        color:#8091A8;
        border-radius:18px;
        font-size:18px;
        font-weight:800;
    """)

    self.name_label = QLabel("OYUNCU")
    self.name_label.setWordWrap(True)
    self.name_label.setStyleSheet("color:white; font-size:28px; font-weight:900;")

    self.branch_label = QLabel("BRANŞ / TAKIM")
    self.branch_label.setStyleSheet(f"color:{accent}; font-size:12px; font-weight:800;")

    self.energy_title = QLabel("ENERJİ SEVİYESİ")
    self.energy_title.setStyleSheet("color:#A6B7CD; font-size:10px; font-weight:700;")

    self.energy_value = QLabel("100%")
    self.energy_value.setStyleSheet(f"color:{accent}; font-size:18px; font-weight:900;")

    energy_row = QHBoxLayout()
    energy_row.addWidget(self.energy_title)
    energy_row.addStretch()
    energy_row.addWidget(self.energy_value)

    self.energy_bg = QFrame()
    self.energy_bg.setFixedHeight(10)
    self.energy_bg.setStyleSheet("background-color:#1A2438; border-radius:5px;")

    self.energy_fill = QFrame(self.energy_bg)
    self.energy_fill.setStyleSheet(f"background-color:{accent}; border-radius:5px;")
    self.energy_fill.setGeometry(0, 0, 260, 10)

    self.info_label = QLabel("TAM GÜÇ AKTİF")
    self.info_label.setStyleSheet(f"color:{accent}; font-size:10px; font-weight:800;")

    self.level_label = QLabel("SEVİYE: 1")
    self.level_label.setStyleSheet("color:#90A1B6; font-size:10px; font-weight:700;")

    info_row = QHBoxLayout()
    info_row.addWidget(self.info_label)
    info_row.addStretch()
    info_row.addWidget(self.level_label)

    self.stat1 = StatBox(accent)
    self.stat2 = StatBox(accent)
    self.stat3 = StatBox(accent)
    self.stat4 = StatBox(accent)

    stats_grid = QGridLayout()
    stats_grid.setSpacing(10)
    stats_grid.addWidget(self.stat1, 0, 0)
    stats_grid.addWidget(self.stat2, 0, 1)
    stats_grid.addWidget(self.stat3, 1, 0)
    stats_grid.addWidget(self.stat4, 1, 1)

    layout = QVBoxLayout()
    layout.setContentsMargins(16, 16, 16, 16)
    layout.setSpacing(10)
    layout.addWidget(self.top_label)
    layout.addWidget(self.image_label)
    layout.addWidget(self.name_label)
    layout.addWidget(self.branch_label)
    layout.addLayout(energy_row)
    layout.addWidget(self.energy_bg)
    layout.addLayout(info_row)
    layout.addLayout(stats_grid)
    layout.addStretch()
    self.setLayout(layout)

def load_image(self, path: str):
    pixmap = QPixmap(path)
    if pixmap.isNull():
        self.image_label.setText("IMAGE\nNOT FOUND")
        self.image_label.setPixmap(QPixmap())
        return

    self.image_label.setText("")
    self.image_label.setPixmap(
        pixmap.scaled(
            self.image_label.width(),
            self.image_label.height(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
    )

def set_card(self, kart: Kart):
    self.load_image(kart.resim)
    self.name_label.setText(kart.ad.upper())
    self.branch_label.setText(f"{kart.brans.upper()} / {kart.takim.upper()}")
    self.energy_value.setText(f"{kart.enerji}%")
    self.level_label.setText(f"SEVİYE: {kart.seviye}")

    if kart.enerji >= 80:
        self.info_label.setText("TAM GÜÇ AKTİF")
    elif kart.enerji >= 40:
        self.info_label.setText("KONDİSYON NORMAL")
    else:
        self.info_label.setText("KRİTİK ENERJİ")

    fill_width = int((kart.enerji / 100) * 260)
    fill_width = max(0, min(fill_width, 260))
    self.energy_fill.setGeometry(0, 0, fill_width, 10)

    items = list(kart.ozellikler.items())
    self.stat1.set_data(items[0][0], items[0][1])
    self.stat2.set_data(items[1][0], items[1][1])
    self.stat3.set_data(items[2][0], items[2][1])
    self.stat4.set_data("Dayanıklılık", kart.dayaniklilik)

class StartScreen(QWidget):def init(self, go_to_game_callback):super().init()self.go_to_game_callback = go_to_game_callback

    self.setStyleSheet("""
        QWidget {
            background-color:#0A0F19;
            color:white;
        }
        QPushButton {
            background-color:white;
            color:black;
            border:none;
            border-radius:10px;
            font-size:18px;
            font-weight:900;
            padding:12px 28px;
        }
        QPushButton:hover {
            background-color:#14D0FF;
        }
    """)

    self.image_label = QLabel()
    self.image_label.setAlignment(Qt.AlignCenter)
    self.image_label.setFixedSize(700, 420)
    self.image_label.setStyleSheet("""
        background-color:#050914;
        border:2px solid #1E2B44;
        border-radius:18px;
    """)

    pixmap = QPixmap("start_screen.png")
    if not pixmap.isNull():
        self.image_label.setPixmap(
            pixmap.scaled(
                self.image_label.width(),
                self.image_label.height(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
        )
    else:
        self.image_label.setText("start_screen.png\nbulunamadı")

    self.button = QPushButton("OYUNA BAŞLA")
    self.button.clicked.connect(self.go_to_game_callback)

    layout = QVBoxLayout()
    layout.addStretch()
    layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
    layout.addSpacing(20)
    layout.addWidget(self.button, alignment=Qt.AlignCenter)
    layout.addStretch()
    self.setLayout(layout)

class GameScreen(QWidget):def init(self, oyun: OyunYonetici):super().init()self.oyun = oyun

    self.setStyleSheet("""
        QWidget {
            background-color:#10151F;
            color:white;
            font-family:'Segoe UI';
        }
        QPushButton {
            background-color:#14D0FF;
            color:#05111B;
            border:none;
            border-radius:14px;
            font-size:16px;
            font-weight:900;
            padding:14px 18px;
        }
        QPushButton:hover {
            background-color:#37DAFF;
        }
    """)

    self.title_label = QLabel("AKILLI SPORCU KART LİGİ SİMÜLASYONU")
    self.title_label.setAlignment(Qt.AlignCenter)
    self.title_label.setStyleSheet("font-size:28px; font-weight:900;")

    self.turn_label = QLabel("Tur: Futbol")
    self.turn_label.setAlignment(Qt.AlignCenter)
    self.turn_label.setStyleSheet("font-size:18px; font-weight:800; color:#B1C4DD;")

    self.score_label = QLabel("Skor: 0 - 0")
    self.score_label.setAlignment(Qt.AlignCenter)
    self.score_label.setStyleSheet("font-size:22px; font-weight:900; color:#14D0FF;")

    self.left_card = PlayerCardWidget("#13D6FF")
    self.right_card = PlayerCardWidget("#48FF1E")

    self.vs_label = QLabel("VS")
    self.vs_label.setAlignment(Qt.AlignCenter)
    self.vs_label.setStyleSheet("font-size:34px; font-weight:900; color:white;")

    cards_layout = QHBoxLayout()
    cards_layout.addStretch()
    cards_layout.addWidget(self.left_card)
    cards_layout.addWidget(self.vs_label)
    cards_layout.addWidget(self.right_card)
    cards_layout.addStretch()

    self.result_label = QLabel("Oyuna başlamak için TUR OYNA butonuna bas.")
    self.result_label.setAlignment(Qt.AlignCenter)
    self.result_label.setWordWrap(True)
    self.result_label.setStyleSheet("""
        background-color:#0B1320;
        border:1px solid #233149;
        border-radius:16px;
        padding:16px;
        font-size:15px;
        font-weight:700;
        color:#DBE7F6;
    """)

    self.play_button = QPushButton("TUR OYNA")
    self.play_button.clicked.connect(self.play_turn)

    layout = QVBoxLayout()
    layout.setContentsMargins(20, 18, 20, 20)
    layout.setSpacing(16)
    layout.addWidget(self.title_label)
    layout.addWidget(self.turn_label)
    layout.addWidget(self.score_label)
    layout.addLayout(cards_layout)
    layout.addWidget(self.result_label)
    layout.addWidget(self.play_button, alignment=Qt.AlignCenter)
    self.setLayout(layout)

def play_turn(self):
    current_branch = self.oyun.aktif_brans()
    self.oyun.tur_oyna()

    self.turn_label.setText(f"Tur: {current_branch}")
    self.score_label.setText(f"Skor: {self.oyun.kullanici.skor} - {self.oyun.bilgisayar.skor}")
    self.result_label.setText(self.oyun.sonuc_metni)

    if self.oyun.kullanici_karti:
        self.left_card.set_card(self.oyun.kullanici_karti)

    if self.oyun.bilgisayar_karti:
        self.right_card.set_card(self.oyun.bilgisayar_karti)

class MainWindow(QWidget):def init(self, oyun: OyunYonetici):super().init()self.setWindowTitle("Akıllı Sporcu Kart Oyunu")self.resize(1100, 860)

    self.stack = QStackedWidget()

    self.start_screen = StartScreen(self.show_game_screen)
    self.game_screen = GameScreen(oyun)

    self.stack.addWidget(self.start_screen)
    self.stack.addWidget(self.game_screen)

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(self.stack)
    self.setLayout(layout)

def show_game_screen(self):
    self.stack.setCurrentWidget(self.game_screen)



def kartlari_olustur():kullanici_kartlar = [Kart(ad="Cristiano Ronaldo",brans="Futbol",takim="Al Nassr",resim="ronaldo.png",enerji=100,seviye=1,dayaniklilik=100,ozellikler={"Penaltı": 99,"Serbest Vuruş": 95,"Kaleci Karşı Karşıya": 98}),Kart(ad="Hidayet Türkoğlu",brans="Basketbol",takim="Türkiye",resim="hidayet.png",enerji=100,seviye=1,dayaniklilik=100,ozellikler={"Üçlük": 95,"İkilik": 92,"Serbest Atış": 90}),Kart(ad="Melissa Vargas",brans="Voleybol",takim="Türkiye",resim="vargas.png",enerji=100,seviye=1,dayaniklilik=100,ozellikler={"Servis": 95,"Blok": 92,"Smaç": 98}),]

bilgisayar_kartlar = [
    Kart(
        ad="Lionel Messi",
        brans="Futbol",
        takim="Inter Miami",
        resim="messi.png",
        enerji=100,
        seviye=1,
        dayaniklilik=98,
        ozellikler={
            "Penaltı": 96,
            "Serbest Vuruş": 97,
            "Kaleci Karşı Karşıya": 97
        }
    ),
    Kart(
        ad="Michael Jordan",
        brans="Basketbol",
        takim="Chicago Bulls",
        resim="jordan.png",
        enerji=100,
        seviye=1,
        dayaniklilik=99,
        ozellikler={
            "Üçlük": 90,
            "İkilik": 99,
            "Serbest Atış": 94
        }
    ),
    Kart(
        ad="Earvin N'Gapeth",
        brans="Voleybol",
        takim="France",
        resim="ngapeth.png",
        enerji=100,
        seviye=1,
        dayaniklilik=97,
        ozellikler={
            "Servis": 91,
            "Blok": 90,
            "Smaç": 96
        }
    ),
]
return kullanici_kartlar, bilgisayar_kartlar



def main():app = QApplication(sys.argv)

kullanici_kartlar, bilgisayar_kartlar = kartlari_olustur()
kullanici = Oyuncu("Sen", kullanici_kartlar)
bilgisayar = Bilgisayar("Bilgisayar", bilgisayar_kartlar)

oyun = OyunYonetici(kullanici, bilgisayar)
window = MainWindow(oyun)
window.show()

sys.exit(app.exec_())

if name == "main":main()
