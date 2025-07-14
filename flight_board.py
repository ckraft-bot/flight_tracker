import flight_tracker
from flight_tracker import get_flights, format_flight_display
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import pandas as pd

# # Fetch flights and prepare display list
# arrivals = get_flights('arr', 'CHA')
# departures = get_flights('dep', 'CHA')

# if arrivals is None or departures is None:
#     print("API limit reached or error, exiting.")
#     exit(1)

# all_flights = arrivals + departures

# df = pd.DataFrame(all_flights)

# if df.empty:
#     print("No flights found, exiting.")
#     exit(1)

# df.columns = ['Direction', 'Airline', 'Flight', 'From', 'To']

# Workaround for API limit reached error, read in a local CSV file instead of fetching from the API
df = pd.read_csv('flights.csv')


def format_flight_display(df):
    """
    Expected format examples 
    For departures:
    "<Flight Number> <Airport Code> ➜ <Airport Code>"
    Example: "UA456 CHA ➜ ORD"

    For arrivals:
    "<Flight> CHA ➜ <From>" (flip the airports for arrivals to show inbound to CHA)
    Example: "DL123 ATL ➜ CHA"
    """

    display = []
    for _, row in df.iterrows():
        flight = row['Flight']
        if row['Direction'] == 'Departure':
            display.append(f"{flight} {row['From']} ➜ {row['To']}")
        else:
            display.append(f"{flight} CHA ➜ {row['From']}")
    return display

display = format_flight_display(df)
print(display)

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
