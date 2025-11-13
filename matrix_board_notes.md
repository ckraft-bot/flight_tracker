1. On your local machine, remote into rpi via Remote Desktop Connection. you'll need ip address of rpi and login credentials, user = pi, password = <your_password>

2. In the rpi terminal, run the following commands to clone, build, and install the rpi-rgb-led-matrix Python bindings
<!-- Go to your development folder -->
`cd ~/Desktop/dev`

<!-- Remove any existing rpi-rgb-led-matrix folder to start fresh -->
`rm -rf rpi-rgb-led-matrix`

<!-- Clone the full repository, including all submodules (recursive ensures all dependencies) -->
`git clone --recursive https://github.com/hzeller/rpi-rgb-led-matrix.git`

<!-- Enter the cloned repository -->
`cd rpi-rgb-led-matrix`

<!--  Build the Python bindings using the system Python3
This automatically runs Cython to generate core.cpp and compiles the bindings -->
`make build-python PYTHON=$(which python3)`

<!-- Install the compiled Python bindings system-wide 
sudo is needed because this writes to system Python directories -->
`sudo make install-python PYTHON=$(which python3)`

<!-- verify the build was successful -->
`python3 -c "from rgbmatrix import RGBMatrix, RGBMatrixOptions; print('RGBMatrix Python bindings installed successfully')"`

<!-- Now test the led board out -->
`cd ~/Desktop/dev/rpi-rgb-led-matrix/bindings/python/samples`

<!-- hello claire (world) -->
`sudo python3 runtext.py --led-cols=64 --led-rows=32 --led-gpio-mapping=regular --led-slowdown-gpio=4 --text="Hello Claire"`

<!-- pulsing colors -->
`sudo python3 pulsing-colors.py --led-cols=64 --led-rows=32 --led-gpio-mapping=regular --led-slowdown-gpio=4`