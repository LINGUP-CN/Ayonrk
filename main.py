from sys import exit

import pygame as pg

from pygame.locals import OPENGL

import reader

'''
-------------------------------------------------
开发人员：Oupcn
开发日期：2024-03-02
开发工具：PyCharm
功能描述：游戏主体。

-------------------------------------------------
'''
running = 1
'''
0 不运行
1 运行游戏界面
2 运行报错界面
'''

sets = reader.read_ark("test.ark")

if sets.error != '':
    running = 2


R_WIDTH: int = 900
R_HEIGHT: int = 650

WIDTH: int = 900
HEIGHT: int = 650

margin_x: int = sets.border_width  # 边框宽度
margin_y: int = sets.border_width  # 边框宽度
tracks_num: int = sets.tracks  # 轨道数
tracks_width: int = int((WIDTH - (tracks_num + 1) * margin_x) / tracks_num)  # 轨道宽
tracks_height: int = HEIGHT - 2 * margin_y  # 轨道长
lines_height: list = sets.lines  # 判定线高度
fps: float = 120
bpm: float = sets.bpm
beat: float = 60 / bpm
time: float = 0
score: int = 0
scores: float = 0
combo: int = 0
max_combo: int = 0
lines_color: list = []
start_music: bool = False
is_music_time: bool = True

time_bad: float = 0.12
time_good: float = 0.1
time_perfect: float = 0.06

pg.init()
pg.font.init()
pg.mixer.init()
clock = pg.time.Clock()
tracks_bg_image = pg.image.load("bg.bmp")
pg.mixer.music.load(sets.music)
root = pg.display.set_mode((R_WIDTH, R_HEIGHT))
screen = pg.Surface((WIDTH, HEIGHT))
pg.display.set_caption("Ayonrk DEMO")

font1 = pg.font.Font("Fonts/SJ-Narrow-ExtraBold-2.ttf", 30)
font2 = pg.font.Font("Fonts/Heiti_GB18030.ttf", 50)
font3 = pg.font.Font("Fonts/Heiti_GB18030.ttf", 20)

tracks_bg_image_width: int = tracks_bg_image.get_width()
tracks_bg_image_height: int = tracks_bg_image.get_height()

tracks_points: list = []
edges: int = 20
for i in range(tracks_num):
    tracks_points.append([
        (edges, 0),
        (tracks_width, 0),
        (tracks_width, tracks_height - edges),
        (tracks_width - edges, tracks_height),
        (0, tracks_height),
        (0, edges)
    ])

is_keydown: list = []
keydown_start: list = []
keydown_end: list = []
taps: list = []
holds: list = []
tracks_sf: list = []
for i in range(tracks_num):
    is_keydown.append(False)
    keydown_start.append(-1)
    keydown_end.append(-1)
    taps.append([])
    holds.append([])
    tracks_sf.append(pg.Surface((tracks_width, tracks_height)))
    lines_color.append("#00FF00")

t: float
y: float

for i in range(tracks_num):
    for j in sets.taps[i]:
        t = j['time'] * beat - (tracks_height - lines_height[i]) / j['speed']
        if t <= 0:
            y = j['speed'] * beat * j['time']
        else:
            y = 0
        taps[i].append({
            'time': t,
            'time_end': j['time'] * beat,
            'speed': j['speed'],
            'y': y,
            'valid': True,
            'result': False})
        max_combo += 1

for i in range(tracks_num):
    for j in sets.holds[i]:
        holds[i].append({
            'e_time': j['e_time'] * beat - (tracks_height - lines_height[i]) / j['speed'],
            'e_time_end': j['e_time'] * beat,
            's_time': j['s_time'] * beat - (tracks_height - lines_height[i]) / j['speed'],
            's_time_end': j['s_time'] * beat,
            's_y': 0,
            'e_y': 0,
            'speed': j['speed'],
            'valid': True,
            'press': -1,
            'result': False})
        max_combo += 1

del t, y

while True:
    if running == 0:
        break
    if running == 1:
        if is_music_time:
            if time >= 0:
                start_music = True
                is_music_time = False
        if start_music:
            pg.mixer.music.play()
            start_music = False
        clock.tick(fps)
        text_scores1 = font1.render('{:07.0f}'.format(scores), True, "#CCCCCC")
        text_scores2 = font1.render('{:07.0f}'.format(scores), True, "#AAAAAA")
        rect_scores1 = [WIDTH - text_scores1.get_width() - 20, 20]
        rect_scores2 = [WIDTH - text_scores2.get_width() - 18, 18]
        text_combo = font1.render("Combo: " + str(combo), True, "#FF8800")

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = 0
            if event.type == pg.KEYDOWN and 49 <= event.key <= 48 + tracks_num:
                is_keydown[event.key - 49] = True
                keydown_start[event.key - 49] = time
            if event.type == pg.KEYUP and 49 <= event.key <= 48 + tracks_num:
                is_keydown[event.key - 49] = False
                keydown_end[event.key - 49] = time

        screen.fill("#F2F2F2")

        for i in range(tracks_num):
            tracks_x = margin_x + i * (margin_x + tracks_width)
            line_y = tracks_height - lines_height[i]

            for y in range(0, tracks_height, tracks_bg_image_height):
                for x in range(0, tracks_width, tracks_bg_image_width):
                    tracks_sf[i].blit(tracks_bg_image, (x, y))

            if is_keydown[i]:
                lines_color[i] = "#00FFFF"
            else:
                lines_color[i] = "#00FF00"

            for j in taps[i]:
                if j['valid']:
                    tap_color = "#FFFFFF"
                else:
                    tap_color = "#FF0000"

                if not j['result']:
                    if j['time'] < time:
                        pg.draw.rect(tracks_sf[i], tap_color, (0, j['y'], tracks_width, 10), 0)
                        j['y'] += j['speed'] / fps

                    if is_keydown[i] and j['valid']:
                        if j['time_end'] - time_good < keydown_start[i] < j['time_end'] + time_good:
                            j['result'] = True
                            combo += 1
                            score += 1
                        elif j['time_end'] - time_bad < keydown_start[i] < j['time_end'] + time_bad:
                            j['valid'] = False
                            combo = 0

                        elif j['time_end'] - time_bad < keydown_start[i] < j['time_end'] + time_bad:
                            combo = 0

                    elif time > j['time_end'] + time_bad and j['valid']:
                        combo = 0
                        j['valid'] = False

            for j in holds[i]:
                if j['valid']:
                    hold_color = "#FFFFFF"
                else:
                    hold_color = "#FF0000"

                if j['e_time'] < time:
                    j['e_y'] += j['speed'] / fps
                if j['s_time'] < time:
                    j['s_y'] += j['speed'] / fps

                if time < j['s_time_end']:
                    if j['s_time'] < time < j['e_time']:
                        pg.draw.rect(tracks_sf[i], "#FFFFFF", (0, 0, tracks_width, j['s_y']), 0)

                    elif j['s_time'] < time and j['e_time'] < time:
                        pg.draw.rect(tracks_sf[i], hold_color, (0, j['e_y'], tracks_width, j['s_y'] - j['e_y']), 0)

                elif time < j['e_time_end']:
                    if j['s_time'] < time < j['e_time']:
                        pg.draw.rect(tracks_sf[i], hold_color, (0, 0, tracks_width, line_y), 0)

                    elif j['s_time'] < time and j['e_time'] < time:
                        pg.draw.rect(tracks_sf[i], hold_color, (0, j['e_y'], tracks_width, line_y - j['e_y']), 0)

                if not j['result']:
                    if is_keydown[i] and j['valid']:

                        if j['s_time_end'] - time_good < keydown_start[i] < j['s_time_end'] + time_good:
                            if time > j['e_time_end'] - time_bad:
                                j['result'] = True
                                combo += 1
                                score += 1

                        elif j['s_time_end'] - time_bad < keydown_start[i] < j['s_time_end'] + time_bad:
                            combo = 0
                            j['valid'] = False
                    elif time > j['s_time_end'] + time_bad:
                        combo = 0
                        j['valid'] = False
            scores = 100000 * score / max_combo

            pg.draw.line(tracks_sf[i], lines_color[i], (0, line_y), (tracks_width, line_y), 2)

            screen.blit(tracks_sf[i], (tracks_x, margin_y))
            pg.draw.rect(screen, "#000000", (tracks_x, margin_y, tracks_width, tracks_height), 3)

        screen.blit(text_scores1, rect_scores1)
        screen.blit(text_scores2, rect_scores2)
        screen.blit(text_combo, (0, 90))
        root.blit(screen, (0, 0))
        pg.display.flip()
        time += 1 / fps
    while running == 2:
        pass

pg.quit()
exit()
