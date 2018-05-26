# FRC-Grapher
A Python app that graphs data sent from the roboRIO of an FRC robot over NetworkTables. 

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development, testing, and use.

### Prerequisites
This requires [RobotPy NetworkTables](https://github.com/robotpy/pynetworktables) and [SimpleWebSocketServer](https://github.com/dpallot/simple-websocket-server). To install just run:
```
$ pip install -r './requirements.txt'
```

### Installing
Follow this guide to install FRC-Grapher locally.

First clone this repository:
```
$ git clone https://github.com/SumiGovindaraju/FRC-Grapher.git
```

Install prerequisites (see [Prerequisites](#prerequisites)). Then create a directory called `cache/`.

To run FRC-Grapher, start the Python WebSocket server and open `index.html`:
```
$ python main.py
```

To start the dummy NetworkTables server, run:
```
$ python test_server.py
```

To see a list of command-line arguments available, run:
```
$ python main.py --help
```

## Usage
To add SmartDashboard keys to the graph, click "Add Dataset" in the navbar, type in the the SmartDashboard key into the modal, and click the "Add Dataset" button.

To save the current key configuration to a file, click "Save Configuration" in the navbar. To run this program with the saved configuration, run the Python WebSocket server with the `-c` or `--config` flag.

FRC-Grapher graphs Value vs. Time graphs. The Time data is sent over NetworkTables using the key `frc-grapher-timestamp` and is measured in seconds in the dummy server. Here are some examples of how to do this on the robot:

Java:
```java
import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;

// When the robot code is initialized
double startTime = Timer.getFPGATimestamp();

// In each periodic cycle
SmartDashboard.putNumber("frc-grapher-timestamp", Timer.getFPGATimestamp() - startTime);
```

C++:
```cpp
#include "WPILib.h"

using namespace frc;

// When the robot code is initialized
double startTime = Timer::GetFPGATimestamp();

// In each periodic cycle	
SmartDashboard::PutNumber("frc-grapher-timestamp", Timer::GetFPGATimestamp() - startTime);
```

Keep in mind that if multiple values are sent for a single timestamp, FRC-Grapher caches and graphs only the latest value, and discards any previous values for that specific timestamp.

FRC-Grapher automatically caches data during the match in a JSON file in the `cache/` directory, named for the starting datetime of execution. To graph the cached data, run:
```
$ python main.py -r [path to JSON cache file]
```

The default IP address for the NetworkTables server is `localhost`, which is what the dummy NetworkTables server runs on. To run this program where the NetworkTables server is the roboRIO, run:
```
$ python main.py -i [IP address of robot]
```

See [this](https://wpilib.screenstepslive.com/s/4485/m/24193/l/319135-ip-networking-at-the-event) for information on your robot's IP address.

## Built With
* [Chart.js](http://www.chartjs.org/) - Library used for graphing
* [Bootstrap](https://getbootstrap.com/) - Library used for styling
* [jQuery](https://jquery.com/) - Bootstrap dependency 
* [Font Awesome](https://fontawesome.com/) - Icons

## Authors
* Sumi Govindaraju
