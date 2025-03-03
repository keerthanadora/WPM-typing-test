import curses
from curses import wrapper
import time
import random
import os

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!", curses.A_BOLD)
    stdscr.addstr("\nPress any key to begin...")
    stdscr.refresh()
    stdscr.getkey()

def load_text():
    filename = "text.txt"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            lines = f.readlines()
            return random.choice(lines).strip()
    else:
        return "This is a sample typing test. Try your best to type quickly and accurately!"

def display_text(stdscr, target, current, wpm):
    stdscr.clear()
    stdscr.addstr(target + "\n\n", curses.color_pair(3))
    stdscr.addstr("WPM: {}".format(wpm), curses.color_pair(4))
    stdscr.addstr("  (Press ESC to exit)\n\n")
    
    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1) if char == correct_char else curses.color_pair(2)
        stdscr.addstr(3, i, char, color)
    
    stdscr.refresh()

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    start_time = time.time()
    stdscr.nodelay(True)
    
    while True:
        elapsed_time = max(time.time() - start_time, 1)
        words_typed = len(current_text) / 5  # Avg word length ~5
        wpm = round((words_typed / elapsed_time) * 60)
        
        display_text(stdscr, target_text, current_text, wpm)
        
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break
        
        try:
            key = stdscr.getkey()
        except curses.error:
            continue
        
        if ord(key) == 27:  # ESC key to exit
            return
        elif key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if current_text:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Correct char
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Incorrect char
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Target text
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)   # WPM display
    
    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr("\nYou completed the text! Press any key to try again, or ESC to exit.\n", curses.A_BOLD)
        key = stdscr.getkey()
        if ord(key) == 27:
            break

wrapper(main)
