import flight_tracker
from flight_tracker import get_flights, format_flight_display
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import pandas as pd

# Fetch flights and prepare display list
arrivals = get_flights('arr', 'CHA')
departures = get_flights('dep', 'CHA')

if arrivals is None or departures is None:
    print("API limit reached or error, exiting.")
    exit(1)

all_flights = arrivals + departures

df = pd.DataFrame(all_flights)

if df.empty:
    print("No flights found, exiting.")
    exit(1)

df.columns = ['Direction', 'Airline', 'Flight', 'From', 'To']

display = format_flight_display(df)

# Setup matrix
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

# Draw lines on the matrix
for i, line in enumerate(display):
    graphics.DrawText(canvas, font, 1, 10 + i*12, color, line)
canvas = matrix.SwapOnVSync(canvas)
