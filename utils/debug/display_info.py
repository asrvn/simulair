from ctypes import windll

windll.user32.SetProcessDPIAware()
screen_width, screen_height = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)

print(f"Screen width: {screen_width}, Screen height: {screen_height}")

# Anieesh Saravanan, 3, 2025