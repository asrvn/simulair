from utils.terminal import nvidia_smi
import dearpygui.dearpygui as dpg
from ctypes import windll
import threading
import time
import math

gui_scale = 1.0
menu_bar_height = 30
show_utilization = True
show_memory = True
show_temperature = True

windll.user32.SetProcessDPIAware()
screen_width, screen_height = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)
window_width, window_height = int(screen_width * 0.5) - 640, int(screen_height * 0.5) - 350

def update_gpu_info():

    while True:

        gpu_data = nvidia_smi()

        while not gpu_data.empty():

            data = gpu_data.get().split(", ")
            index, name = data[:2]
            utilization, temperature, memory_used, memory_total = map(int, data[2:])

            dpg.set_value(f"gpu_name_{index}", f"Name: {name}")
            dpg.set_value(f"gpu_utilization_{index}_bar", round(utilization / 100, 2))
            dpg.set_value(f"gpu_memory_{index}_bar", round((memory_used / memory_total), 2))
            dpg.set_value(f"gpu_temperature_{index}_bar", round(temperature / 100, 2))

            dpg.configure_item(f"gpu_utilization_{index}_bar", overlay=f"Utilization: {utilization:.0f}%")
            dpg.configure_item(f"gpu_memory_{index}_bar", overlay=f"Memory Usage: {memory_used} / {memory_total} MB")
            dpg.configure_item(f"gpu_temperature_{index}_bar", overlay=f"Temperature: {temperature:.0f}°C")

            dpg.delete_item(f"gpu_drawlist_{index}", children_only=True)

            positions = calculate_circle_positions()

            if show_utilization:
                draw_circle_with_border(positions[0], 50, utilization, "Utilization", (100, 100, 250, 255), index)
            if show_memory:
                draw_circle_with_border(positions[1], 50, round((memory_used / memory_total) * 100, 2), "Memory", (100, 250, 100, 255), index)
            if show_temperature:
                draw_circle_with_border(positions[2], 50, temperature, "Temperature", (250, 100, 100, 255), index)

        time.sleep(1)

def calculate_circle_positions():

    positions = []
    current_x, step = 100 * gui_scale, 200 * gui_scale

    if show_utilization:
        positions.append(current_x)
        current_x += step
    else:
        positions.append(None)

    if show_memory:
        positions.append(current_x)
        current_x += step
    else:
        positions.append(None)

    if show_temperature:
        positions.append(current_x)

    return positions

def draw_circle_with_border(x_pos, radius, value, label, fill_color, index):

    if x_pos is None: return

    border_radius = radius * gui_scale + 5

    dpg.draw_circle(center = [x_pos, 100 * gui_scale],
                    radius = border_radius,
                    color = (255, 255, 255, 255),
                    thickness = 2 * gui_scale,
                    parent = f"gpu_drawlist_{index}")

    draw_filled_circle_segment([x_pos, 100 * gui_scale],
                               radius * gui_scale,
                               0,
                               (value / 100) * 360,
                               fill_color,
                               f"gpu_drawlist_{index}")

    formatted_value = f"{value:.0f}%" if label != "Temperature" else f"{value:.0f}°C"

    draw_text_on_arc(formatted_value,
                     [x_pos, 100 * gui_scale],
                     radius * gui_scale,
                     0,
                     (value / 100) * 360,
                     f"gpu_drawlist_{index}")

    dpg.draw_text((x_pos - 20 * gui_scale, 160 * gui_scale),
                  label,
                  size = 15 * gui_scale,
                  color = (255, 255, 255, 255),
                  parent = f"gpu_drawlist_{index}")

def draw_filled_circle_segment(center, radius, start_angle, end_angle, color, parent):

    points = [center]
    resolution = 1

    for angle in range(int(start_angle), int(end_angle) + 1, resolution):

        radians = math.radians(angle)
        x, y = center[0] + radius * math.cos(radians), center[1] + radius * math.sin(radians)

        points.append([x, y])

    dpg.draw_polygon(points, color = color, fill = color, parent = parent)

def draw_text_on_arc(text, center, radius, start_angle, end_angle, parent):

    # TODO: adjust to center better, this isn't the best
    mid_angle = (start_angle + end_angle) / 2
    radians = math.radians(mid_angle)

    distance_from_center = radius - 45 * gui_scale
    x, y = center[0] + distance_from_center * math.cos(radians), center[1] + distance_from_center * math.sin(radians)

    dpg.draw_text((x + 1, y + 1), text, size = 20 * gui_scale, color = (0, 0, 0, 255), parent = parent)
    dpg.draw_text((x, y), text, size = 20 * gui_scale, color = (255, 255, 255, 255), parent = parent)

def adjust_gui_scale(sender, app_data):

    global gui_scale, window_width, window_height

    gui_scale = app_data
    dpg.set_global_font_scale(gui_scale)

    dpg.configure_item("main_window", width = int(window_width * gui_scale), height = int(window_height * gui_scale - menu_bar_height))
    dpg.set_viewport_width(int(window_width * gui_scale))
    dpg.set_viewport_height(int(window_height * gui_scale))

    dpg.configure_item("menu_window", width = int(window_width * gui_scale))

    for i in range(gpu_count):

        dpg.configure_item(f"gpu_drawlist_{i}", width = int(800 * gui_scale), height = int(400 * gui_scale))

    refresh_gpu_display()  # Apply scale changes to the GPU display

def toggle_utilization(sender, app_data):

    global show_utilization

    show_utilization = app_data
    refresh_gpu_display()

def toggle_memory(sender, app_data):

    global show_memory

    show_memory = app_data
    refresh_gpu_display()

def toggle_temperature(sender, app_data):

    global show_temperature

    show_temperature = app_data
    refresh_gpu_display()

def refresh_gpu_display():

    for i in range(gpu_count):

        dpg.delete_item(f"gpu_drawlist_{i}", children_only = True)
        positions = calculate_circle_positions()

        # TODO: move draw circle check (if none) to here

        if show_utilization:
            draw_circle_with_border(positions[0], 50, dpg.get_value(f"gpu_utilization_{i}_bar") * 100, "Utilization", (100, 100, 250, 255), i)
        if show_memory:
            draw_circle_with_border(positions[1], 50, dpg.get_value(f"gpu_memory_{i}_bar") * 100, "Memory", (100, 250, 100, 255), i)
        if show_temperature:
            draw_circle_with_border(positions[2], 50, dpg.get_value(f"gpu_temperature_{i}_bar") * 100, "Temperature", (250, 100, 100, 255), i)

def initialize_gui():

    global gpu_count; gpu_count = 0

    # CREATE GUI CONTEXT

    dpg.create_context()

    with dpg.window(label = "Menu",
                    width = int(window_width * gui_scale), height = int(menu_bar_height * gui_scale),
                    no_close = True, no_move = True, no_resize = True, no_title_bar = True, no_background = True, tag = "menu_window"):

        dpg.add_text("Menu Bar", pos=(0, 0))

        with dpg.menu_bar():

            with dpg.menu(label = "File"):

                dpg.add_menu_item(label = "Close", callback = dpg.stop_dearpygui)

            with dpg.menu(label = "Visibility"):

                dpg.add_menu_item(label = "Show Utilization", callback = toggle_utilization, check = True, default_value = True)
                dpg.add_menu_item(label = "Show Memory", callback = toggle_memory, check = True, default_value = True)
                dpg.add_menu_item(label = "Show Temperature", callback = toggle_temperature, check = True, default_value = True)

    with dpg.window(label = "NVIDIA GPU Monitor",
                    width = int(window_width * gui_scale), height = int(window_height * gui_scale - menu_bar_height * gui_scale),
                    pos = (0, int(menu_bar_height * gui_scale)),  # TODO: FIX CONNECTION BETWEEN WINDOW AND MENU BAR
                    tag = "main_window",
                    no_title_bar = True, no_move = True, no_resize = True, no_scrollbar = True, no_background = True):

        dpg.add_slider_float(label = "GUI Scale", default_value = 1.0, min_value = 0.5, max_value = 2.0, callback = adjust_gui_scale)
        dpg.add_separator()

        # CONFIGURE DATA DISPLAY

        gpu_data = nvidia_smi()

        while not gpu_data.empty():

            index, name, utilization, temperature, memory_used, memory_total = gpu_data.get().split(", ")

            with dpg.group(tag = f"gpu_group_{index}"):

                dpg.add_text(f"GPU {index} Info", tag = f"gpu_name_{index}")
                dpg.add_progress_bar(tag = f"gpu_utilization_{index}_bar", default_value = 0, overlay = "Utilization: 0%")
                dpg.add_progress_bar(tag = f"gpu_memory_{index}_bar", default_value = 0, overlay = "Memory Usage: 0%")
                dpg.add_progress_bar(tag = f"gpu_temperature_{index}_bar", default_value = 0, overlay = "Temperature: 0°C")

                with dpg.drawlist(width = int(800 * gui_scale), height = int(400 * gui_scale), tag = f"gpu_drawlist_{index}"):

                    dpg.draw_circle(center = [100, 100], radius = 50, color = (255, 255, 255, 255), thickness = 2)
                    dpg.draw_circle(center = [300, 100], radius = 50, color = (255, 255, 255, 255), thickness = 2)
                    dpg.draw_circle(center = [500, 100], radius = 50, color = (255, 255, 255, 255), thickness = 2)

            gpu_count += 1

    dpg.create_viewport(title = 'NVIDIA GPU Monitor', width = window_width, height = window_height, small_icon = "../../assets/icons/monitor_logo.ico", large_icon = "../../assets/icons/monitor_logo.ico")
    dpg.setup_dearpygui()
    dpg.show_viewport()

initialize_gui()

threading.Thread(target = update_gpu_info, daemon = True).start()

dpg.start_dearpygui()
dpg.destroy_context()

# Anieesh Saravanan, 3, 2025