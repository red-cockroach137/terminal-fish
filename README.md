# 🐠 Terminal Fish

A terminal-based fishing game suite written in Python and Bash. Catch fish, build your collection, watch them swim in a live aquarium, and browse your FishDex like a Pokédex — all inside your terminal.

---

## 📦 What's Included

| File | Description |
|------|-------------|
| `fish_catcher.sh.en` | The main fishing script — cast your line and catch fish |
| `fish_book.py.en` | FishDex — browse your caught fish collection with animations |
| `fish_tank.py.en` | Live aquarium — watch your caught fish swim around |
| `fish_tank_colors.py.en` | Live aquarium — watch your caught fish swim around + colors for the terminal with faded corals |
| `set_language.py` | Language switcher (EN / RU / ZH / JA) |
| `install.sh` | Installer — sets everything up in one command |
| `kitty_fish_record.dat` | full file for aquarium (without fishing) |

---

## 🚀 Quick Start

### Requirements

- **macOS** or **Linux**
- Python 3.8+
- Bash 4+
- A terminal with UTF-8 and 256-color support (iTerm2, Kitty, Alacritty, GNOME Terminal, etc.)

### Install

```bash
# Clone the repo
git clone https://github.com/red-cockroach137/terminal-fish.git && cd terminal-fish

# Run the installer
bash install.sh
```

The installer will:
1. Check all required files and dependencies
2. Copy scripts to `~/bin/`
3. Make everything executable
4. Enters aliases into .zshrc or .bashrc

> 🌍 Language / Язык / 语言 / 言語: Run `python3 set_language.py` to switch between **English**, **Russian**, **Chinese**, and **Japanese**.

### Run

```bash
# Go fishing
open a new tab 

or 

fish_catcher.sh

# Browse your FishDex
fish_book

# Open the live aquarium
fish_tank

# Open the live aquarium + colors
fish_tank_color
```

### If you only need an aquarium with all the fish already in stock:
```
cp kitty_fish_record.dat ~/.kitty_fish_record.dat
```
---

## 🎮 How It Works

### 🎣 Fishing (`fish_catcher.sh`)

Run the script and it randomly generates a catch based on rarity odds:

| Rarity | Chance | Color |
|--------|--------|-------|
| Common | 65% | White |
| Uncommon | 25% | Green |
| Rare | 8% | Blue |
| Epic | 2% | Purple |
| Legendary | 0.01% | Gold |

Each species has its own size range — bigger fish of the same species are rarer. Your personal record per species is saved automatically.

### 📖 FishDex (`fish_book.py`)

Browse your caught fish like a Pokédex:

| Key | Action |
|-----|--------|
| `←` `→` | Switch pages |
| `↑` `↓` | Move between cards |
| `Enter` | Open fish details (animated popup) |
| `Esc` / `B` | Close popup |
| `Q` | Quit |

Each card shows rarity, personal best size, and a rating from **F** to **SSS** based on how close your catch is to the species maximum.

### 🐠 Aquarium (`fish_tank.py`)

A live screensaver — your caught fish swim across the screen with coral decorations:

| Key | Action |
|-----|--------|
| `D` | Toggle / shuffle decorations |
| `R` | Refresh the tank |
| `Q` | Quit |

### 🌍 Language Switcher (`set_language.py`)

Switches all UI text across all scripts at once:

| # | Language |
|---|----------|
| 1 | 🇬🇧 English |
| 2 | 🇷🇺 Russian (Русский) |
| 3 | 🇨🇳 Chinese (中文) |
| 4 | 🇯🇵 Japanese (日本語) |

---

## 🐟 Fish Roster

### ⚪ Common
`fish` · `who` · `comrade` · `lil_bro` · `baby_shark` · `smoking_fish`

### 🟢 Uncommon
`cooperatish` · `piranha` · `smiling_fish` · `flat_earthism` · `bigboy` · `sea_horse`

### 🔵 Rare
`horse_of_sea` · `UFO?` · `f_117` · `dummy`

### 🟣 Epic
`shark_sniffer` · `skull` · `dolphy` · `crush`

### 🟡 Legendary
`shank_fish` · `closed_claw` · `Bubbie` · `mrs_puff`

---

## 💾 Data Storage

All catches are saved to `~/.kitty_fish_record.dat` — a plain text file, one record per species:

```
fish|8|2024-03-12 14:22
baby_shark|28|2024-04-01 09:11
mrs_puff|420|2024-06-01 23:59
```

Format: `species_name | length_cm | date`

To reset your progress:
```bash
rm ~/.kitty_fish_record.dat
```

To delete all:
```bash
bash delete_sad_fish.sh
```

---

## 💛 Support the Project

If you enjoy Terminal Fish and want to say thanks — crypto donations are welcome:

TON:
```
UQBHycodO_bwdPW96UB1wuEPqHcpao-kbQBEkjnrZ3KzRkaW
```

Terminal Fish is free and always will be. ✌️

---

## 📄 License

**Terminal Fish Non-Commercial License (TFNL-1.0)**
Free to use, modify, and share for personal non-commercial purposes.
**Selling or commercial use is prohibited.**
See [LICENSE](./LICENSE) for full terms.

---

## 🙏 Credits

Built with love, `curses`, Bash, and a lot of ASCII art.

> *"The sea, once it casts its spell, holds one in its net of wonder forever."*
