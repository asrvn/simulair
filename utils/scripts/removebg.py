from utils.image import remove_background

path = '../monitor/assets/icons/logo.ico'
extension = path.rsplit('.', 1)[1]

output = remove_background(path)
output.save(f'output.{extension}', format='ICO', sizes=[(256, 256)])

# Anieesh Saravanan, 3, 2025