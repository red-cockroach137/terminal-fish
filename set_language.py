#!/usr/bin/env python3
import os
import sys
import re

# ── Settings ────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INSTALL_DIR = os.path.expanduser("~/bin")
EN_EXT = ".en"

os.makedirs(INSTALL_DIR, exist_ok=True)

# ── Find all .en files in the current folder ─────────────────────
FILES = [f for f in os.listdir(SCRIPT_DIR) if f.endswith(EN_EXT)]

# ── Translations with context (whole lines or specific patterns) ──
TRANSLATIONS = [
    # fish_book.py
    {"en":"caught","ru":"поймано","zh":"已捕获","ja":"捕獲済み"},
    {"en":"◄ PAGE I","ru":"◄ ЧАСТЬ I","zh":"◄ 第一页","ja":"◄ ページ I"},
    {"en":"PAGE II ►","ru":"ЧАСТЬ II ►","zh":"第二页 ►","ja":"ページ II ►"},
    {"en":" ←→↑↓ navigate | PgUp/PgDn — page | Enter — details | Q — quit",
     "ru":" ←→↑↓ навигация | PgUp/PgDn — страница | Enter — детали | Q — выход",
     "zh":" ←→↑↓ 导航 | PgUp/PgDn — 翻页 | Enter — 详情 | Q — 退出",
     "ja":" ←→↑↓ 移動 | PgUp/PgDn — ページ | Enter — 詳細 | Q — 終了"},
    {"en":" Esc / B — close ","ru":" Esc / B — закрыть ","zh":" Esc / B — 关闭 ","ja":" Esc / B — 閉じる "},
    {"en":"Length","ru":"Длина","zh":"长度","ja":"長さ"},
    {"en":"Max.","ru":"Макс.","zh":"最大","ja":"最大"},
    {"en":"Date","ru":"Дата","zh":"日期","ja":"日付"},
    {"en":"Rating","ru":"Рейтинг","zh":"评级","ja":"評価"},
    {"en":"Progress: ","ru":"Прогресс: ","zh":"进度: ","ja":"進捗: "},
    {"en":"~ not caught ~","ru":"~ не поймана ~","zh":"~ 未捕获 ~","ja":"~ 未捕獲 ~"},
    {"en":"Rarity: ","ru":"Редкость: ","zh":"稀有度: ","ja":"レアリティ: "},
    {"en":"[ any key ]","ru":"[ любая клавиша ]","zh":"[ 按任意键 ]","ja":"[ 任意のキー ]"},
    {"en":"~  See you, fisherman!  ~","ru":"~  До встречи, рыбак!  ~","zh":"~  再见，渔夫！~","ja":"~  またね、釣り人！  ~"},
    {"en":'["Common","Uncommon","Rare","Epic","Legendary"]',
     "ru":'["Common","Uncommon","Rare","Epic","Legendary"]',
     "zh":'["普通","稀有","珍稀","史诗","传说"]',
     "ja":'["コモン","アンコモン","レア","エピック","レジェンダリー"]'},

    # fish_tank.py & fish_tank_colors.py
    {"en":"On screen: ","ru":"На экране: ","zh":"当前: ","ja":"表示中: "},
    {"en":"'q'=quit 'r'=refresh","ru":"'q'=выход 'r'=обновить","zh":"'q'=退出 'r'=刷新","ja":"'q'=終了 'r'=更新"},
    {"en":"🌿 Decor: ON (D=shuffle)","ru":"🌿 Декор: ВКЛ (D=перемешать)","zh":"🌿 装饰: 开 (D=刷新)","ja":"🌿 デコ: ON (D=シャッフル)"},
    {"en":"🪸 Decor: OFF","ru":"🪸 Декор: ВЫКЛ","zh":"🪸 装饰: 关","ja":"🪸 デコ: OFF"},
    {"en":"❌ Catch at least one fish first!","ru":"❌ Сначала поймай хотя бы одну рыбу!","zh":"❌ 请先至少捕获一条鱼！","ja":"❌ まず魚を一匹釣ってください！"},
    {"en":"Press any key to exit...","ru":"Нажми любую клавишу для выхода...","zh":"按任意键退出...","ja":"任意のキーを押して終了..."},
    {"en":"👋 Aquarium closed!","ru":"👋 Аквариум закрыт!","zh":"👋 水族馆已关闭！","ja":"👋 水槽を閉じました！"},

    # fish_catcher.sh - CRITICAL FIX: use whole phrase
    {"en":"🎣 You caught a fish! 🎣",
     "ru":"🎣 Вы поймали рыбу! 🎣",
     "zh":"🎣 你钓到了一条鱼！🎣",
     "ja":"🎣 魚を釣り上げました！🎣"},
    {"en":" Species:  ","ru":" Вид:      ","zh":" 种类:     ","ja":" 種類:     "},
    {"en":" Length:   ","ru":" Длина:    ","zh":" 长度:     ","ja":" 長さ:     "},
    {"en":" Rarity:   ","ru":" Редкость: ","zh":" 稀有度:   ","ja":" レア度:   "},
    {"en":"🏆 NEW RECORD for","ru":"🏆 НОВЫЙ РЕКОРД для","zh":"🏆 新纪录","ja":"🏆 新記録"},
    {"en":"Record for","ru":"Рекорд для","zh":"该种类纪录","ja":"記録"},
    {"en":" cm","ru":" см","zh":" 厘米","ja":" cm"},
    {"en":'RARITY_NAMES=("Common" "Uncommon" "Rare" "Epic" "Legendary")',
     "ru":'RARITY_NAMES=("Common" "Uncommon" "Rare" "Epic" "Legendary")',
     "zh":'RARITY_NAMES=("普通" "稀有" "珍稀" "史诗" "传说")',
     "ja":'RARITY_NAMES=("コモン" "アンコモン" "レア" "エピック" "レジェンダリー")'},
]

CODES = ["en","ru","zh","ja"]
LANG_LABELS = {"en":"🇬🇧 English", "ru":"🇷🇺 Russian", "zh":"🇨🇳 Chinese", "ja":"🇯🇵 Japanese"}

# ── Auxiliary functions ──────────────────────────────────
def parse_arg(arg):
    arg = arg.strip().lower()
    if arg.isdigit() and 1 <= int(arg) <= len(CODES):
        return CODES[int(arg)-1]
    if arg in CODES:
        return arg
    return None

def apply_translation(content, lang):
    """Apply translations safely - whole phrases only, order by length DESC"""
    # Sort by source length (longest first) to avoid partial matches
    sorted_translations = sorted(TRANSLATIONS, key=lambda x: len(x.get("en", "")), reverse=True)
    
    for entry in sorted_translations:
        src = entry.get("en")
        dst = entry.get(lang)
        if src and dst and src != dst:
            # Use word boundary or line-based replacement for safety
            # For phrases with spaces or special chars, replace exactly
            if ' ' in src or any(c in src for c in '!@#$%^&*()'):
                content = content.replace(src, dst)
            else:
                # For single words, use word boundaries
                content = re.sub(r'\b' + re.escape(src) + r'\b', dst, content)
    return content

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    os.chmod(path, 0o755)

# ── Basic logic ─────────────────────────────────────────
def main():
    # ── Determining the language
    to_lang = None
    if len(sys.argv) > 1:
        to_lang = parse_arg(sys.argv[1])
    if to_lang is None:
        print("Select language:")
        for i, code in enumerate(CODES, 1):
            print(f"[{i}] {LANG_LABELS[code]}")
        choice = input("Choice: ").strip()
        to_lang = parse_arg(choice)
    if to_lang not in CODES:
        print("Invalid choice")
        sys.exit(1)

    print(f"Switching language to {LANG_LABELS[to_lang]} ...")

    # ── We process each .en file
    for en_file in FILES:
        src_path = os.path.join(SCRIPT_DIR, en_file)
        dst_name = en_file[:-len(EN_EXT)]  
        dst_path = os.path.join(INSTALL_DIR, dst_name)

        with open(src_path, "r", encoding="utf-8") as f:
            content = f.read()

        # We apply translations
        new_content = apply_translation(content, to_lang)

        # Write to ~/bin
        write_file(dst_path, new_content)
        print(f"✅ {dst_name} → {to_lang}")

    print(f"\n🎣 Language switch complete! Files are in {INSTALL_DIR}")

if __name__ == "__main__":
    main()
