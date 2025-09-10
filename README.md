# FIRA Smart Home League (U19)

This repository contains my controller for the **FIRA Smart Home League**: a Webots-based, vacuum-style robot that navigates rooms, avoids obstacles, and maximizes cleaning performance under the official league environment. The project targets Webots R2023a with Python 3.9/3.10. See the official base repo for environment setup, worlds (`U14.wbt` / `U19.wbt`), and scoring overview. [References below]

## Competition context (what the simulator expects)
The league provides a smart-home world in Webots where teams load their Python controller and compete on cleaning efficiency / task execution in a limited time. The official starter repository describes the simulator, how to open the worlds, and that scoring is based on the cleanliness of the home surface. For full details, consult the league rulebook PDF and the base repository instructions. [See references]

## Technical approach (no camera / no CV)
This implementation is **purely sensor-driven**:
- **Proximity sensing:** 8 distance sensors `D1–D8` mapped to logical directions (`Front`, `FrontLeft`, `Left`, `BackLeft`, `Back`, `BackRight`, `Right`, `FrontRight`).
- **Heading:** one **inertial unit** (IMU) for compass/heading control.
- **Supervisor telemetry:** a **receiver** reads JSON packets (current room name and per-room cleaning percentage), and an **emitter** announces the team name/channel.
- **Differential drive:** two wheel motors (`wheel1 motor`, `wheel2 motor`) with a simple velocity scaler.

There is **no camera, no AprilTags, and no computer-vision** in this code path.

## Code overview (SmartHome.py)
Key devices and setup:
- `controller.Robot()` with `timeStep` and `maxSpeed`.
- Devices: two wheel motors, `D1…D8` distance sensors, `inertial_unit`, `receiver`/`emitter`.  
- Comms: `emitter.setChannel(1)` and a team name broadcast; `receiver.setChannel(1)` and JSON parsing of supervisor messages.

Core functions:
- `readSensorsPrimary()` – samples all 8 proximity sensors, computes `Compass` from the inertial unit, and ingests supervisor telemetry (`CurrentRoom`, `Rooms{room: cleaning%}`).
- `move(left, right)` – scales wheel speeds (`maxSpeed`) and drives the motors.
- `turn(deg)` with `eslah()` – heading normalization and a tight window check (±2°) to finish turns.
- `jolo()` – forward advance until a front-arc obstacle is detected; promotes the state.
- `becharkh(deg)` – rotate to a target heading and advance the state if aligned.
- A **lightweight state machine** (`marhale`, `duration`, minor randomness in open spaces) sequences search → align → pass → room coverage behaviors.

Behavioral notes:
- Forward motion is gated by near-field thresholds on the front sensors; turning uses IMU-based heading windows.
- Random micro-perturbations help escape local minima in open areas.
- Supervisor JSON is used to read per-room progress; the debug panel prints live sensor and cleaning stats.

## How to run
1. Install **Webots R2023a** and Python 3.9/3.10.  
2. Open the league’s smart-home world (e.g., `U19.wbt`) in Webots.  
3. Load/select your controller (`SmartHome.py`) and start the simulation (ensure it’s not paused).  
4. Use the robot window / console to observe debug output; the controller auto-registers the team name and reads supervisor telemetry.

> For environment install steps and common troubleshooting (Windows/macOS), follow the league’s base repo and installation guide links.  

## Roadmap
- Finer wall-following and doorway heuristics (side-bias + adaptive thresholds).
- Coverage patterns that react to `Rooms{room: %cleaned}` to prioritize low-coverage rooms.
- Simple stall detection with timed escape routines.

## References
- **FIRA Smart Home base repository** (Webots worlds, setup, scoring overview).  [oai_citation:0‡GitHub](https://github.com/fira-smarthome/Smart-Home)  
- **League rulebook PDF** (linked in the base repository).  [oai_citation:1‡GitHub](https://github.com/fira-smarthome/Smart-Home/blob/master/FIRA%20-%20Smart%20Home%20Rules.pdf)  
- **smarthome-utils** helper library (documents the canonical sensor/actuator stack: D1–D8, IMU, motors, emitter/receiver).  [oai_citation:2‡GitHub](https://github.com/fira-smarthome/smarthome-utils)
