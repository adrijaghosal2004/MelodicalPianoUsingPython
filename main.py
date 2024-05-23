import pygame
from pygame import mixer
import tkinter as tk
from PIL import Image, ImageTk

piano_notes = ['A0', 'A0#', 'B0', 'C1', 'C1#', 'D1', 'D1#', 'E1', 'F1', 'F1#', 'G1', 'G1#',
               'A1', 'A1#', 'B1', 'C2', 'C2#', 'D2', 'D2#', 'E2', 'F2', 'F2#', 'G2', 'G2#',
               'A2', 'A2#', 'B2', 'C3', 'C3#', 'D3', 'D3#', 'E3', 'F3', 'F3#', 'G3', 'G3#',
               'A3', 'A3#', 'B3', 'C4', 'C4#', 'D4', 'D4#', 'E4', 'F4', 'F4#', 'G4', 'G4#',
               'A4', 'A4#', 'B4', 'C5', 'C5#', 'D5', 'D5#', 'E5', 'F5', 'F5#', 'G5', 'G5#',
               'A5', 'A5#', 'B5', 'C6', 'C6#', 'D6', 'D6#', 'E6', 'F6', 'F6#', 'G6', 'G6#',
               'A6', 'A6#', 'B6', 'C7', 'C7#', 'D7', 'D7#', 'E7', 'F7', 'F7#', 'G7', 'G7#',
               'A7', 'A7#', 'B7', 'C8']

white_notes = ['A0', 'B0', 'C1', 'D1', 'E1', 'F1', 'G1',
               'A1', 'B1', 'C2', 'D2', 'E2', 'F2', 'G2',
               'A2', 'B2', 'C3', 'D3', 'E3', 'F3', 'G3',
               'A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4',
               'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5',
               'A5', 'B5', 'C6', 'D6', 'E6', 'F6', 'G6',
               'A6', 'B6', 'C7', 'D7', 'E7', 'F7', 'G7',
               'A7', 'B7', 'C8']

black_notes = ['Bb0', 'Db1', 'Eb1', 'Gb1', 'Ab1',
               'Bb1', 'Db2', 'Eb2', 'Gb2', 'Ab2',
               'Bb2', 'Db3', 'Eb3', 'Gb3', 'Ab3',
               'Bb3', 'Db4', 'Eb4', 'Gb4', 'Ab4',
               'Bb4', 'Db5', 'Eb5', 'Gb5', 'Ab5',
               'Bb5', 'Db6', 'Eb6', 'Gb6', 'Ab6',
               'Bb6', 'Db7', 'Eb7', 'Gb7', 'Ab7',
               'Bb7']

black_labels = ['A#0', 'C#1', 'D#1', 'F#1', 'G#1',
                'A#1', 'C#2', 'D#2', 'F#2', 'G#2',
                'A#2', 'C#3', 'D#3', 'F#3', 'G#3',
                'A#3', 'C#4', 'D#4', 'F#4', 'G#4',
                'A#4', 'C#5', 'D#5', 'F#5', 'G#5',
                'A#5', 'C#6', 'D#6', 'F#6', 'G#6',
                'A#6', 'C#7', 'D#7', 'F#7', 'G#7',
                'A#7']


WIDTH = 52 * 35
HEIGHT = 300
show_piano=False

def show_piano_window():
    global show_piano
    show_piano = True
    root.destroy()
    pygame.display.set_mode([WIDTH, HEIGHT])

def create_gui_window():
    global root
    root = tk.Tk()
    root.geometry("751x500")
    root.title("MyPiano Homepage")

    def on_enter(event):
        button.config(bg="white", fg="brown")

    def on_leave(event):
        button.config(bg="white", fg="black")

    original_image = Image.open("Designed by Adrija.png")
    bg_image = ImageTk.PhotoImage(original_image)

    background_label = tk.Label(root, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    button = tk.Button(root, text="Play Piano", command=show_piano_window, bg="white", fg="black", width=13, font=("Arial", 17, "bold"),relief='sunken')
    button.place(x=535, y=272)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    root.mainloop()

create_gui_window()

if show_piano:
    pygame.init()
    pygame.mixer.set_num_channels(50)

    font_name = pygame.font.get_default_font()
    font = pygame.font.Font(font_name, 48)
    medium_font = pygame.font.Font(font_name, 28)
    small_font = pygame.font.Font(font_name, 16)
    real_small_font = pygame.font.Font(font_name, 12)

    fps = 60
    timer = pygame.time.Clock()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("MyPiano")

    white_sounds = []
    black_sounds = []

    left_hand =  ['Z', 'Q', 'X', 'W', 'C', 'V', 'E', 'B', 'R', 'N', 'T', 'M']
    right_hand = ['A', 'Y', 'S', 'U', 'D', 'F', 'I', 'G', 'O', 'H', 'P', 'J']

    for i in range(len(white_notes)):
        white_sounds.append(mixer.Sound(f'assets\\notes\\{white_notes[i]}.wav'))

    for i in range(len(black_notes)):
        black_sounds.append(mixer.Sound(f'assets\\notes\\{black_notes[i]}.wav'))

    active_whites = []
    active_blacks = []
    left_oct = 4
    right_oct = 5

    def update_key_dicts():
        global left_dict, right_dict, key_to_note
        left_dict = {   'Z': f'C{left_oct}',
                        'Q': f'C#{left_oct}',
                        'X': f'D{left_oct}',
                        'W': f'D#{left_oct}',
                        'C': f'E{left_oct}',
                        'V': f'F{left_oct}',
                        'E': f'F#{left_oct}',
                        'B': f'G{left_oct}',
                        'R': f'G#{left_oct}',
                        'N': f'A{left_oct}',
                        'T': f'A#{left_oct}',
                        'M': f'B{left_oct}'}


        right_dict = {  'A': f'C{right_oct}',
                        'Y': f'C#{right_oct}',
                        'S': f'D{right_oct}',
                        'U': f'D#{right_oct}',
                        'D': f'E{right_oct}',
                        'F': f'F{right_oct}',
                        'I': f'F#{right_oct}',
                        'G': f'G{right_oct}',
                        'O': f'G#{right_oct}',
                        'H': f'A{right_oct}',
                        'P': f'A#{right_oct}',
                        'J': f'B{right_oct}'}


        key_to_note = {v: k for k, v in left_dict.items()}
        key_to_note.update({v: k for k, v in right_dict.items()})

    update_key_dicts()

    def draw_piano(whites, blacks):
        white_rects = []
        for i in range(52):
            rect = pygame.draw.rect(screen, 'white', [i * 35, 0, 35, HEIGHT], 0, 2)
            white_rects.append(rect)
            pygame.draw.rect(screen, 'black', [i * 35, 0, 35, HEIGHT], 2, 2)
            
            key_label = small_font.render(white_notes[i], True, 'black')
            screen.blit(key_label, (i * 35 + 3, HEIGHT - 20))

            if white_notes[i] in key_to_note:
                key_char = key_to_note[white_notes[i]]
                key_char_label = real_small_font.render(key_char, True, 'black')
                label_x = (i * 35) + (35 // 2) - (key_char_label.get_width() // 2)
                if i < 30:  
                    pygame.draw.rect(screen, 'lightblue', [label_x - 5, HEIGHT - 60, key_char_label.get_width() + 10, 30], 0)
                    screen.blit(key_char_label, (label_x, HEIGHT - 50))
                else:       
                    pygame.draw.rect(screen, 'lightgreen', [label_x - 5, HEIGHT - 60, key_char_label.get_width() + 10, 30], 0)
                    screen.blit(key_char_label, (label_x, HEIGHT - 50))

        skip_count = 0
        last_skip = 2
        skip_track = 2
        black_rects = []
        for i in range(36):
            rect = pygame.draw.rect(screen, 'black', [23 + (i * 35) + (skip_count * 35), 0, 24, HEIGHT - 100], 0, 2)
            for q in range(len(blacks)):
                if blacks[q][0] == i:
                    if blacks[q][1] > 0:
                        pygame.draw.rect(screen, 'green', [23 + (i * 35) + (skip_count * 35), 0, 24, HEIGHT - 100], 2, 2)
                        blacks[q][1] -= 1

            note_label = real_small_font.render(black_labels[i], True, 'white')
            label_x = (23 + (i * 35) + (skip_count * 35)) + (24 // 2) - (note_label.get_width() // 2)
            screen.blit(note_label, (label_x, HEIGHT - 120))

            if black_labels[i] in key_to_note:
                key_char = key_to_note[black_labels[i]]
                key_char_label = real_small_font.render(key_char, True, 'white')
                label_x = (22 + (i * 35) + (skip_count * 35)) + (24 // 2) - (key_char_label.get_width() // 2)
                screen.blit(key_char_label, (label_x, HEIGHT - 140))

            black_rects.append(rect)
            skip_track += 1
            if last_skip == 2 and skip_track == 3:
                last_skip = 3
                skip_track = 0
                skip_count += 1
            elif last_skip == 3 and skip_track == 2:
                last_skip = 2
                skip_track = 0
                skip_count += 1

        for i in range(len(whites)):
            if whites[i][1] > 0:
                j = whites[i][0]
                pygame.draw.rect(screen, 'green', [j * 35, 0, 35, HEIGHT], 2, 2)
                whites[i][1] -= 1

        return white_rects, black_rects, whites, blacks

    def play_black_sound(index):
        black_sounds[index].play(0, 1000)
        active_blacks.append([index, 30])

    def play_white_sound(index):
        white_sounds[index].play(0, 3000)
        active_whites.append([index, 15])

    run = True
    while run:
        timer.tick(fps)
        screen.fill('gray')
        white_keys, black_keys, active_whites, active_blacks = draw_piano(active_whites, active_blacks)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                black_key = False
                for i in range(len(black_keys)):
                    if black_keys[i].collidepoint(event.pos):
                        black_sounds[i].play(0, 1000)
                        black_key = True
                        active_blacks.append([i, 30])
                for i in range(len(white_keys)):
                    if white_keys[i].collidepoint(event.pos) and not black_key:
                        white_sounds[i].play(0, 1000)
                        active_whites.append([i, 30])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if right_oct < 8:
                        right_oct += 1
                        update_key_dicts()
                elif event.key == pygame.K_LEFT:
                    if right_oct > 0:
                        right_oct -= 1
                        update_key_dicts()
                elif event.key == pygame.K_UP:
                    if left_oct < 8:
                        left_oct += 1
                        update_key_dicts()
                elif event.key == pygame.K_DOWN:
                    if left_oct > 0:
                        left_oct -= 1
                        update_key_dicts()
                else:
                    key = pygame.key.name(event.key)
                    if key.upper() in left_dict:
                        note = left_dict[key.upper()]
                        if note in white_notes:
                            index = white_notes.index(note)
                            play_white_sound(index)
                        else:
                            index = black_labels.index(note)
                            play_black_sound(index)
                    elif key.upper() in right_dict:
                        note = right_dict[key.upper()]
                        if note in white_notes:
                            index = white_notes.index(note)
                            play_white_sound(index)
                        else:
                            index = black_labels.index(note)
                            play_black_sound(index)

        pygame.display.flip()

    pygame.quit()
