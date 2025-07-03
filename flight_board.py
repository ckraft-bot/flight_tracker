from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.hardware_mapping = 'regular'
matrix = RGBMatrix(options=options)
canvas = matrix.CreateFrameCanvas()
font = graphics.Font()
font.LoadFont("../../../fonts/6x12.bdf")
color = graphics.Color(255, 255, 0)

# Example flight lines
lines = ["DAL 382 CHA ➜ ATL", "UAL 570 CHA ➜ ORD"]
for i, line in enumerate(lines):
    graphics.DrawText(canvas, font, 1, 10 + i*12, color, line)
canvas = matrix.SwapOnVSync(canvas)
