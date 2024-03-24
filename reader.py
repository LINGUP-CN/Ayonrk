"""
-------------------------------------------------
开发人员：Oupcn
开发日期：2024-03-02
开发工具：Python IDLE
功能描述：用于解析铺面文件。

-------------------------------------------------
"""


def read_ark(s_file: str):
    if s_file.endswith(".ark"):
        try:
            v_name: str = "Unknown"
            v_author_music: str = "Unknown"
            v_author_chat: str = "Unknown"
            v_author_image: str = "Unknown"
            v_fps: float = 60
            v_border_height: int = 10
            v_border_width: int = 10
            v_tracks: int = 4
            v_lines: list = [[], [], [], []]
            v_taps: list = [[], [], [], []]
            v_holds: list = [[], [], [], []]
            v_music: str = ''
            v_image: str = ''
            e_info: str = ''
            e_line_test: int = 0
            e_line: int = 0
            line_height = 0
            file = open(s_file, mode='r', encoding="utf-8")
            text = file.read()
            file.close()
            lines = text.splitlines()
            for s_cmd in lines:
                e_line_test += 1
                cmd = s_cmd.split(' ')
                if s_cmd == "":
                    pass
                elif cmd[0][0] == "#":
                    pass
                elif cmd[0] == "tap":
                    if len(cmd) == 4:
                        v_taps[int(cmd[1])].append({"time": float(cmd[2]), "speed": float(cmd[3])})
                    else:
                        e_info = '指令 "tap" 引用有误'
                        e_line = e_line_test
                elif cmd[0] == "hold":
                    if len(cmd) == 5:
                        v_holds[int(cmd[1])].append(
                            {"s_time": float(cmd[2]), "e_time": float(cmd[3]), "speed": float(cmd[4])})
                    else:
                        e_info = '指令 "hold" 引用有误'
                        e_line = e_line_test
                elif cmd[0] == "set":
                    if cmd[1] == "name":
                        if len(cmd) == 3:
                            v_name = cmd[2]
                        else:
                            e_info = '指令 "set name" 引用有误'
                            e_line = e_line_test
                    elif cmd[1] == "author":
                        if cmd[2] == "music":
                            if len(cmd) == 4:
                                v_author_music = cmd[3]
                            else:
                                e_info = '指令 "set author music" 引用有误'
                                e_line = e_line_test
                        if cmd[2] == "chat":
                            if len(cmd) == 4:
                                v_author_chat = cmd[3]
                            else:
                                e_info = '指令 "set author chat" 引用有误'
                                e_line = e_line_test
                        if cmd[2] == "image":
                            if len(cmd) == 4:
                                v_author_image = cmd[3]
                            else:
                                e_info = '指令 "set author image" 引用有误'
                                e_line = e_line_test
                    elif cmd[1] == "fps":
                        if len(cmd) == 3:
                            v_fps = int(cmd[2])
                        else:
                            e_info = '指令 "set fps" 引用有误'
                            e_line = e_line_test
                    elif cmd[1] == "tracks":
                        if len(cmd) == 3:
                            v_lines = []
                            v_taps = []
                            v_holds = []
                            v_tracks = int(cmd[2])
                            for i in range(v_tracks + 1):
                                v_lines.append(line_height)
                                v_taps.append([])
                                v_holds.append([])
                        else:
                            e_info = '指令 "set tracks" 引用有误'
                            e_line = e_line_test
                    elif cmd[1] == "bpm":
                        if len(cmd) == 3:
                            v_bpm = int(cmd[2])
                        else:
                            e_info = '指令 "set bpm" 引用有误'
                            e_line = e_line_test
                    elif cmd[1] == "lines":
                        if len(cmd) == 3:
                            v_lines = []
                            line_height: int = int(cmd[2])
                            for i in range(v_tracks):
                                v_lines.append(line_height)
                        else:
                            e_info = '指令 "set lines" 引用有误'
                            e_line = e_line_test
                    elif cmd[1] == "line":
                        if len(cmd) == 4:
                            v_lines[int(cmd[2])] = float(cmd[3])
                        else:
                            e_info = '指令 "set line" 引用有误'
                            e_line = e_line_test
                    elif cmd[1] == "border":
                        if len(cmd) == 4:
                            if cmd[2] == "height":
                                v_border_height = int(cmd[3])
                            elif cmd[2] == "width":
                                v_border_width = int(cmd[3])
                        else:
                            e_info = '指令 "set line" 引用有误'
                            e_line = e_line_test
                elif cmd[0] == "load":
                    if cmd[1] == "music":
                        if len(cmd) == 3:
                            v_music = cmd[2]
                        else:
                            e_info = '指令 "set music" 引用有误'
                            e_line = e_line_test
                    if cmd[1] == "image":
                        if len(cmd) == 3:
                            v_image = cmd[2]
                        else:
                            e_info = '指令 "set image" 引用有误'
                            e_line = e_line_test
                else:
                    e_info = '未知指令 "' + cmd[0] + '"'
                    e_line = e_line_test
        except Exception as e:
            e_info = str(e)

        class ClassInfo:
            name = v_name

            class Author:
                music = v_author_music
                chat = v_author_chat
                image = v_author_image

            fps = v_fps
            bpm = v_bpm
            music = v_music
            image = v_image
            tracks = v_tracks
            lines = v_lines
            border_height = v_border_height
            border_width = v_border_width
            taps = v_taps
            holds = v_holds
            error = e_info
            error_line = e_line

        return ClassInfo
    else:
        return ''
