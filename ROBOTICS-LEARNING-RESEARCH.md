# Best Way to Learn Robotics (Strong Math, No Physics)

_Research date: 2026-09-24. Learner profile: comfortable with math, no physics background, wants hands-on experience._

## Bottom line

1. **Learn a small slice of physics first, tied to the robotics it serves.** Newton's laws, torque and rotational inertia, energy and friction, basic circuits and DC motors. Roughly 3-4 weeks. Your math makes this fast.
2. **Simulate before you buy hardware.** Write your own pendulum simulation (about 20 lines of Python), then move to PyBullet or MuJoCo.
3. **Then build cheap hardware.** A self-balancing robot is the best first project because it forces feedback, sensing, and control in one system.
4. **Use one rigorous text as the spine.** *Modern Robotics* (Lynch & Park) for kinematics, dynamics, and control. *Underactuated Robotics* (Tedrake) afterwards.
5. **Study with retrieval practice, spaced repetition, and mastery gating.** These have the strongest evidence of any study technique. The companion app in `tutor/` implements them.

## 1. Sequencing: simulation first, hardware second

Multiple beginner roadmaps converge on the same order: one language, sensors and actuators, build in simulation, add ROS 2, close the loop on one behavior, then move to hardware ([Robotics for Beginners 2026](https://www.youware.com/guide/getting-started-robotics-beginner-guide), [The Construct](https://www.theconstruct.ai/a-learning-path-to-become-a-robotics-developer/)).

- **Why simulation first:** on hardware a bug could be code, a loose wire, a dying battery, or a miscalibrated sensor. In simulation the only variable is your logic.
- **What simulation cannot replace:** real sensor noise, mechanical behavior (backlash, friction), wiring and integration pain.
- **Implication:** simulation teaches the concepts cleanly; hardware teaches the failure modes. You need both, in that order.

_Source quality: these are beginner-guide blogs, not studies. The sim-first advice is consistent across them and with professional practice, but treat it as convention, not evidence._

## 2. Physics: what you actually need

The primary text is explicit. *Modern Robotics* lists these prerequisites ([Northwestern Modern Robotics wiki](https://hades.mech.northwestern.edu/index.php/Modern_Robotics)):

- Physics fundamentals (forces, torques, free-body diagrams)
- Linear algebra, calculus, basic differential equations
- Programming in Python, MATLAB, or Mathematica

**Correction to my earlier answer:** I said the book introduces physics as needed. The book's own page lists physics as a prerequisite, so a learner with no physics should cover the block below *before* starting it.

Minimum physics block (this is what the companion app's first modules cover):

| Topic | Why robotics needs it |
|---|---|
| Velocity, acceleration, F = ma | Every simulation is integrating this |
| Torque, τ = Iα, moment of inertia | Joints are rotational; motors output torque |
| Gravity, energy, friction | Holding an arm up costs torque; friction limits control |
| Ohm's law, DC motors, back-EMF | Choosing and driving motors; stall current |

## 3. Core robotics topics, in dependency order

1. **Feedback control (PID).** The single most important practical skill. Brian Douglas's Control System Lectures are the standard intuitive resource ([YouTube](https://www.youtube.com/user/ControlLectures)). Tune PID on a real motor or balancing robot.
2. **Kinematics.** Rotation matrices, forward and inverse kinematics, Jacobians, singularities. Modern Robotics chapters 2-7.
3. **Sensors and state estimation.** Noise, gyro drift, complementary filter, then Kalman filter. Roger Labbe's free *Kalman and Bayesian Filters in Python* is intuition-first, with Jupyter notebooks and exercises with solutions ([GitHub](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python)).
4. **Dynamics and trajectory planning.** Modern Robotics chapters 8-11.
5. **ROS 2**, once you have a working robot or sim. Jazzy Jalisco is the current LTS (released May 2024, supported until May 2029) ([ROS 2 learning path](https://github.com/openhorizonrobotics/ros2-learning)).

## 4. Resources

### Primary texts (free)

- ***Modern Robotics*, Lynch & Park.** 13 chapters (configuration space through wheeled mobile robots). Free PDF, full lecture videos, companion code in Python/MATLAB/Mathematica, CoppeliaSim scenes. A six-course Coursera specialization follows the book and can be audited free; certificates and graded work need paid enrollment ([Coursera](https://www.coursera.org/specializations/modernrobotics)).
- ***Underactuated Robotics*, Tedrake (MIT 6.832).** 21 chapters, every chapter has Jupyter/Colab notebooks using the Drake toolbox ([underactuated.csail.mit.edu](https://underactuated.csail.mit.edu/)). Start at chapter 2 (simple pendulum) after finishing the basics. Later chapters (dynamic programming, Lyapunov analysis, trajectory optimization) are for after Modern Robotics.
- ***Kalman and Bayesian Filters in Python*, Labbe.** See above.

### Simulators

| Tool | Best for | Caveat |
|---|---|---|
| Your own Python integrator | Learning what a simulator does | None; do this first |
| PyBullet | Zero-install, simplest API, lots of tutorial code | Described as a legacy choice for new research |
| MuJoCo | Contact-rich manipulation, humanoids, RL research | Steeper than PyBullet |
| Isaac Sim / Isaac Lab | Photorealism, thousands of parallel environments | NVIDIA GPU, heavy install, changes yearly |
| Gazebo | ROS 2 integration | More setup |

Several 2026 comparisons recommend PyBullet for week one and MuJoCo once you touch reinforcement learning ([RobotForge](https://robotforge.org/tutorials/simulators/choosing-a-simulator-2026), [Drift](https://www.godrift.ai/blogs/best-robot-simulators-ros2)).

_Source quality: these comparison sites are vendor/blog content of uneven authority. The MuJoCo-for-research and PyBullet-for-teaching consensus is consistent across them._

### Hardware

- **First project:** self-balancing two-wheel robot (ESP32/Arduino + IMU + two motors). It is an inverted pendulum, the standard exemplar for control ([Cornell ECE4760 project](https://people.ece.cornell.edu/land/courses/ece4760/FinalProjects/f2015/dc686_nn233_hz263/final_project_webpage_v2/dc686_nn233_hz263/index.html)). PID tuning is the main challenge.
- **Second project:** a 6-axis arm. The SO-101 with Hugging Face **LeRobot** handles servo setup, teleoperation data collection, training, and inference through a CLI ([LeRobot SO-101 docs](https://huggingface.co/docs/lerobot/so101)).
- **Caveat:** LeRobot is oriented toward imitation learning, not classical kinematics. You can run inverse kinematics on the same arm yourself, but the tooling will not teach it for you.

### A course that is no longer an option

Georgia Tech's *Control of Mobile Robots* (Egerstedt) closed to new enrollment on 2020-08-17 per the search results. Use Brian Douglas's lectures plus a real balancing robot instead.

## 5. How to study (the evidence)

- **Practice testing and distributed practice** received the highest utility ratings among ten techniques in the Dunlosky et al. review; rereading and highlighting rated low ([Dunlosky et al. 2013](https://pubmed.ncbi.nlm.nih.gov/26173288/)).
- **Retrieval plus spacing combined** outperform either alone; one review summarizes 242 studies, 1,619 effects, and 169,179 participants ([truelearn summary](https://truelearn.com/resource-library/combine-practice-retrieval-and-spaced-repetition-into-a-powerful-teaching-learning-tool/)). Effects are strongest for factual and conceptual knowledge, which is what the physics block is.
- **Mastery learning** (Bloom, 1968): master prerequisites before advancing. Reported average effect size about 0.59 ([Wikipedia summary](https://en.wikipedia.org/wiki/Mastery_learning)); Guskey and Pigott (1988) found d = 0.52-0.94. Learning is hierarchical, and later material depends on complete understanding of earlier material.

_Caveat: multiple-choice quizzing tests recognition and concepts. It does not build the skill of tuning a controller or debugging a robot. That is why the plan pairs quizzes with the simulation and hardware projects above._

## 6. Suggested plan

| Weeks | Focus | Output |
|---|---|---|
| 1-3 | Physics block via the tutor app (motion, rotation, energy/friction, electronics) | Pass modules 1-4 at 80% |
| 3-4 | Feedback control and kinematics concepts | Pass modules 5-6 |
| 4-5 | Sensors/estimation and simulation readiness | Pass modules 7-8; own pendulum simulation in Python |
| 5-8 | PyBullet/MuJoCo arm; Modern Robotics ch. 2-6 | Forward/inverse kinematics of a 2-link arm |
| 8-12 | Self-balancing robot | PID-tuned robot that stands |
| 12+ | Modern Robotics ch. 8-11, Underactuated ch. 2-3, ROS 2, SO-101 arm | Second project |

The week ranges are my estimate, not sourced; adjust to your pace.

## Limitations

- Several sources are blog-level beginner guides and vendor comparison pages; I used them for consensus, not for strong claims.
- I did not verify current pricing or availability of hardware kits.
- I did not find a controlled study on learning robotics specifically; the learning-science evidence is general.

## Sources

- [Robotics for Beginners 2026: Simulation to Hardware](https://www.youware.com/guide/getting-started-robotics-beginner-guide)
- [A Learning Path To Become a Robotics Developer (The Construct)](https://www.theconstruct.ai/a-learning-path-to-become-a-robotics-developer/)
- [Modern Robotics, Northwestern wiki](https://hades.mech.northwestern.edu/index.php/Modern_Robotics)
- [Modern Robotics specialization, Coursera](https://www.coursera.org/specializations/modernrobotics)
- [Underactuated Robotics, MIT course notes](https://underactuated.csail.mit.edu/)
- [Kalman and Bayesian Filters in Python](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python)
- [Brian Douglas, Control System Lectures](https://www.youtube.com/user/ControlLectures)
- [Choosing a robotics simulator in 2026, RobotForge](https://robotforge.org/tutorials/simulators/choosing-a-simulator-2026)
- [Best Robot Simulators for ROS 2, Drift](https://www.godrift.ai/blogs/best-robot-simulators-ros2)
- [ROS 2 Jazzy learning path](https://github.com/openhorizonrobotics/ros2-learning)
- [LeRobot SO-101, Hugging Face docs](https://huggingface.co/docs/lerobot/so101)
- [Self-balancing robot, Cornell ECE4760](https://people.ece.cornell.edu/land/courses/ece4760/FinalProjects/f2015/dc686_nn233_hz263/final_project_webpage_v2/dc686_nn233_hz263/index.html)
- [Dunlosky et al. 2013, Effective Learning Techniques](https://pubmed.ncbi.nlm.nih.gov/26173288/)
- [Quiz-based learning summary](https://truelearn.com/resource-library/combine-practice-retrieval-and-spaced-repetition-into-a-powerful-teaching-learning-tool/)
- [Mastery learning](https://en.wikipedia.org/wiki/Mastery_learning)
