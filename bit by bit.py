import turtle
import tkinter as tk

# --- Turtle Setup ---
t = turtle.Turtle()
ts = turtle.Screen()
ts.tracer(0)

def draw_sq(x, y, clr):
    t.penup()
    t.goto(x, y)
    t.setheading(0)
    t.pendown()
    t.fillcolor(clr)
    t.begin_fill()
    for _ in range(4):
        t.forward(20)
        t.left(90)
    t.end_fill()
    t.penup()

# --- Bit Operations ---
def circular_left_shift(pattern, bits=8):
    return ((pattern << 1) & 0xFF) | ((pattern >> (bits-1)) & 1)

def circular_right_shift(pattern, bits=8):
    return (pattern >> 1) | ((pattern & 1) << (bits-1))

def gray_code(n):
    return n ^ (n >> 1)

# --- Display Function ---
def display_pattern(pattern, colors=None):
    t.clear()
    for kk in range(8):
        b = (pattern >> kk) & 1
        x = 100 - 40*kk
        y = 40
        t.goto(x, y+30)
        t.write("b"+str(kk))
        clr = "white"
        if b == 1:
            clr = colors[kk] if colors else "red"
        draw_sq(x, y, clr)
    ts.update()

# --- Styles ---
def style_shift_left(pattern):
    pattern <<= 1
    if pattern > 255:
        pattern = 0b00000011
    return pattern

def style_shift_right(pattern):
    pattern >>= 2
    if pattern == 0:
        pattern = 0b10100000
    return pattern

def style_xor(pattern):
    return pattern ^ 0xFF

def style_gray(cnt):
    return gray_code(cnt % 256)

def style_circular_left(pattern):
    return circular_left_shift(pattern)

def style_circular_right(pattern):
    return circular_right_shift(pattern)

# --- Runner ---
current_style = None
pattern = 0b11000011
cnt = 0
colors = ["red","green","blue","yellow","purple","orange","cyan","magenta"]
job_id = None

def run_style():
    global pattern, cnt, job_id
    display_pattern(pattern, colors if current_style=="colorful" else None)

    if current_style == "shift_left":
        pattern = style_shift_left(pattern)
    elif current_style == "shift_right":
        pattern = style_shift_right(pattern)
    elif current_style == "xor":
        pattern = style_xor(pattern)
    elif current_style == "gray":
        pattern = style_gray(cnt)
    elif current_style == "circular_left":
        pattern = style_circular_left(pattern)
    elif current_style == "circular_right":
        pattern = style_circular_right(pattern)
    elif current_style == "colorful":
        pattern = style_shift_left(pattern)

    cnt += 1
    job_id = root.after(500, run_style)

def start_style(style):
    global current_style, pattern, cnt, job_id
    if job_id is not None:
        root.after_cancel(job_id)
        job_id = None
    t.clear()
    ts.update()
    current_style = style
    pattern = 0b11000011
    cnt = 0
    run_style()

# --- Tkinter Control Panel ---
root = tk.Tk()
root.title("LED Simulator Control Panel")

styles = ["shift_left","shift_right","xor","gray","circular_left","circular_right","colorful"]
for s in styles:
    btn = tk.Button(root, text=s.replace("_"," ").title(), command=lambda st=s: start_style(st))
    btn.pack(fill="x")

root.mainloop()
