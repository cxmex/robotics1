"""Robotics building blocks, in prerequisite order.

Each lesson has a short explanation, one question and exactly 3 answer options.
`correct` is the index of the right option in `options`. Modules are meant to be
completed in order; the last one gates the start of Python simulation work.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Lesson:
    id: str
    module: str
    title: str
    teach: str
    question: str
    options: tuple[str, str, str]
    correct: int
    explanation: str


@dataclass(frozen=True)
class Module:
    id: str
    title: str
    summary: str


MODULES: tuple[Module, ...] = (
    Module("motion", "1. Motion and Newton", "Velocity, acceleration, F = ma, and stepping them forward in time."),
    Module("rotation", "2. Torque and rotation", "Torque, moment of inertia, and the rotational form of F = ma."),
    Module("energy", "3. Gravity, energy, friction", "What holding an arm up costs, and what friction takes away."),
    Module("electric", "4. Circuits and motors", "Ohm's law, motor torque, back-EMF, and stall."),
    Module("control", "5. Feedback control", "Closed loops and the P, I, and D terms."),
    Module("kinematics", "6. Kinematics", "Rotations, forward and inverse kinematics, Jacobians."),
    Module("sensing", "7. Sensors and estimation", "Noise, drift, and fusing sensors."),
    Module("sim", "8. Simulation readiness", "What you need to know before writing your first simulator in Python."),
)


LESSONS: tuple[Lesson, ...] = (
    # --- 1. Motion and Newton -------------------------------------------------
    Lesson(
        "motion-accel", "motion", "Acceleration",
        "Velocity is the rate of change of position. Acceleration is the rate of change of velocity. "
        "Average acceleration = (change in velocity) / (time taken).",
        "A robot speeds up from 2 m/s to 6 m/s in 4 s. What is its average acceleration?",
        ("1.5 m/s²", "1 m/s²", "4 m/s²"), 1,
        "(6 - 2) / 4 = 1 m/s². The 4 m/s² option forgets to divide by time.",
    ),
    Lesson(
        "motion-f-ma", "motion", "Newton's second law",
        "Newton's second law: net force = mass × acceleration (F = ma). "
        "This one equation is what almost every robot simulator integrates.",
        "A 2 kg cart is pushed with a net force of 6 N and no friction. What is its acceleration?",
        ("12 m/s²", "0.33 m/s²", "3 m/s²"), 2,
        "a = F / m = 6 / 2 = 3 m/s². Multiplying instead of dividing gives 12.",
    ),
    Lesson(
        "motion-net-force", "motion", "Net force",
        "Only the net force (the sum of all forces, with signs) causes acceleration. "
        "Friction subtracts from a push in the opposite direction.",
        "A 3 kg cart is pushed with 10 N while friction pushes back with 4 N. What is its acceleration?",
        ("3.33 m/s²", "4.67 m/s²", "2 m/s²"), 2,
        "Net force = 10 - 4 = 6 N, so a = 6 / 3 = 2 m/s². Using 10 N alone gives 3.33.",
    ),
    Lesson(
        "motion-euler", "motion", "Stepping forward in time",
        "A simulator advances time in small steps dt. The simplest rule (Euler integration) is "
        "v_new = v + a·dt, then x_new = x + v·dt.",
        "With v = 1 m/s, a = 2 m/s², and dt = 0.1 s, what is v_new after one step?",
        ("3.0 m/s", "1.02 m/s", "1.2 m/s"), 2,
        "v_new = 1 + 2 × 0.1 = 1.2 m/s. Forgetting to multiply by dt gives 3.0.",
    ),
    # --- 2. Torque and rotation ----------------------------------------------
    Lesson(
        "rot-torque", "rotation", "Torque",
        "Torque is the turning effect of a force: torque = distance from pivot × perpendicular force. "
        "Robot joints are driven by torque.",
        "A 0.5 m arm has a 10 N force applied at its end, perpendicular to the arm. What torque acts on the pivot?",
        ("20 N·m", "5 N·m", "0.05 N·m"), 1,
        "torque = 0.5 × 10 = 5 N·m.",
    ),
    Lesson(
        "rot-direction", "rotation", "Direction of the force matters",
        "Only the component of force perpendicular to the arm makes torque. "
        "The component along the arm just pulls or pushes on the pivot.",
        "A force pushes straight along the arm, directly away from the pivot. What torque does it produce about the pivot?",
        ("Zero", "The maximum possible", "force × length, same as a perpendicular push"), 0,
        "The force line passes through the pivot, so its lever arm is zero and so is the torque.",
    ),
    Lesson(
        "rot-tau-i-alpha", "rotation", "Rotational Newton: τ = Iα",
        "Rotation has its own version of F = ma: torque = moment of inertia × angular acceleration (τ = Iα). "
        "Moment of inertia I is the rotational equivalent of mass.",
        "A joint has I = 0.2 kg·m² and receives a net torque of 1 N·m. What is its angular acceleration?",
        ("0.2 rad/s²", "5 rad/s²", "0.8 rad/s²"), 1,
        "α = τ / I = 1 / 0.2 = 5 rad/s².",
    ),
    Lesson(
        "rot-inertia", "rotation", "Moment of inertia",
        "For a point mass, I = m·r². Mass far from the pivot counts much more than mass near it, "
        "because distance is squared.",
        "You slide a payload farther out along a robot arm. What happens to the arm's moment of inertia about the joint?",
        ("It decreases", "It stays the same", "It increases, growing with the square of the distance"), 2,
        "I = m·r² grows as r grows. That is why long, heavy arms need strong motors to accelerate.",
    ),
    # --- 3. Gravity, energy, friction ----------------------------------------
    Lesson(
        "energy-weight", "energy", "Weight",
        "Weight is the gravitational force on a mass: W = m·g, with g ≈ 9.8 m/s² on Earth.",
        "What is the weight of a 2 kg object?",
        ("2 N", "19.6 N", "9.8 N"), 1,
        "W = 2 × 9.8 = 19.6 N. Mass (kg) and weight (N) are different quantities.",
    ),
    Lesson(
        "energy-holding", "energy", "Gravity torque on an arm",
        "Gravity's torque on an arm depends on how far the arm's weight sits horizontally from the pivot. "
        "That horizontal distance is largest when the arm is horizontal and zero when it hangs straight down.",
        "Which arm pose needs more motor torque to hold still against gravity?",
        ("Hanging straight down", "Horizontal", "Both need the same torque"), 1,
        "Horizontal has the longest lever arm. Hanging straight down has zero gravity torque.",
    ),
    Lesson(
        "energy-kinetic", "energy", "Kinetic energy",
        "Kinetic energy is KE = ½·m·v². Energy grows with the square of speed.",
        "A robot doubles its speed. What happens to its kinetic energy?",
        ("It quadruples", "It doubles", "It stays the same"), 0,
        "(2v)² = 4v², so KE becomes 4 times larger. Stopping distance grows accordingly.",
    ),
    Lesson(
        "energy-friction", "energy", "Friction",
        "A common model of sliding friction: friction force ≈ μ × normal force, "
        "where μ is the friction coefficient and the normal force is how hard the surfaces press together.",
        "The normal force between a wheel and the floor doubles. What happens to the maximum friction force?",
        ("It doubles", "It halves", "It stays the same"), 0,
        "Friction is proportional to the normal force in this model, so it doubles.",
    ),
    # --- 4. Circuits and motors ----------------------------------------------
    Lesson(
        "elec-ohm", "electric", "Ohm's law",
        "Ohm's law: voltage = current × resistance (V = I·R).",
        "5 V is applied across a 10 Ω resistor. What current flows?",
        ("50 A", "2 A", "0.5 A"), 2,
        "I = V / R = 5 / 10 = 0.5 A.",
    ),
    Lesson(
        "elec-torque-current", "electric", "Motor torque follows current",
        "For a DC motor, output torque is roughly proportional to current: τ = k·I. "
        "Voltage mostly sets speed; current sets torque.",
        "Which quantity do you increase to roughly double a DC motor's torque?",
        ("Current", "The wire's resistance", "Nothing; torque is fixed by the motor's size"), 0,
        "τ = k·I, so doubling the current roughly doubles the torque.",
    ),
    Lesson(
        "elec-back-emf", "electric", "Back-EMF",
        "A spinning motor also acts as a generator, producing a voltage that opposes the supply (back-EMF). "
        "The faster it spins, the larger the back-EMF.",
        "With a fixed supply voltage, what happens to the current a motor draws as it speeds up?",
        ("It increases", "It decreases", "It stays the same"), 1,
        "Back-EMF cancels more of the supply voltage as speed rises, so the net voltage across the windings, and thus the current, falls.",
    ),
    Lesson(
        "elec-stall", "electric", "Stall",
        "A stalled motor is powered but not spinning, so there is no back-EMF.",
        "What current does a stalled DC motor draw, compared with a freely spinning one?",
        ("Zero", "The maximum current, which can overheat it", "The same as when spinning freely"), 1,
        "With no back-EMF, only the winding resistance limits current. Stall gives peak torque and peak heating.",
    ),
    # --- 5. Feedback control -------------------------------------------------
    Lesson(
        "ctrl-loops", "control", "Open vs closed loop",
        "Open loop: send a command and hope. Closed loop (feedback): measure the result, compare with the goal, "
        "and correct the command continually.",
        "A robot reads a sensor every cycle and adjusts its motor command based on the error. What is this called?",
        ("Open-loop control", "Feedback (closed-loop) control", "Feedforward-only control"), 1,
        "Using a measured result to correct the next command is feedback.",
    ),
    Lesson(
        "ctrl-p", "control", "Proportional control",
        "Proportional control: command = Kp × error, where error = target − measurement.",
        "Target is 10, measurement is 7, and Kp = 2. What is the command?",
        ("3", "20", "6"), 2,
        "error = 10 − 7 = 3, so command = 2 × 3 = 6.",
    ),
    Lesson(
        "ctrl-i", "control", "Integral term",
        "The integral term accumulates error over time and adds it to the command.",
        "What is the main purpose of the integral term?",
        ("Remove steady-state offset", "Filter out sensor noise", "Predict where the error is going"), 0,
        "A P-only controller can settle short of the target; the integral keeps pushing until the error is zero.",
    ),
    Lesson(
        "ctrl-d", "control", "Derivative term",
        "The derivative term responds to how fast the error is changing, so it pushes back as the system rushes toward the target.",
        "What is the main effect of the derivative term?",
        ("It removes steady-state offset", "It damps oscillation and overshoot", "It makes the system respond to noise less"), 1,
        "D acts like a brake against fast approach. It tends to amplify sensor noise, not reduce it.",
    ),
    # --- 6. Kinematics -------------------------------------------------------
    Lesson(
        "kin-rotation", "kinematics", "Rotation matrices",
        "In 2D, rotating a vector by angle θ multiplies it by R = [[cosθ, −sinθ], [sinθ, cosθ]].",
        "What is the point (1, 0) after a 90° counter-clockwise rotation about the origin?",
        ("(0, −1)", "(0, 1)", "(1, 0)"), 1,
        "cos 90° = 0 and sin 90° = 1, so R·(1, 0) = (0, 1).",
    ),
    Lesson(
        "kin-fk", "kinematics", "Forward kinematics",
        "Forward kinematics computes the tip position from joint angles by chaining each link's rotation and length.",
        "A planar arm has two 1 m links. Joint 1 is at 0° and joint 2 is at 90° relative to link 1. Where is the tip?",
        ("(2, 0)", "(1, 1)", "(0, 2)"), 1,
        "Link 1 reaches (1, 0). Link 2 points 90° from link 1, i.e. straight up, adding (0, 1), so the tip is at (1, 1).",
    ),
    Lesson(
        "kin-jacobian", "kinematics", "The Jacobian",
        "The Jacobian is the matrix of partial derivatives of tip position with respect to joint angles. "
        "It is the local, linear map between joint motion and tip motion.",
        "What does the Jacobian relate?",
        ("Joint velocities to tip velocity", "Motor voltage to motor current", "Time to distance travelled"), 0,
        "tip velocity = J × joint velocities.",
    ),
    Lesson(
        "kin-ik", "kinematics", "Inverse kinematics",
        "Inverse kinematics goes the other way: given a target tip position, find joint angles. "
        "It can have zero, one, or several solutions.",
        "A two-link planar arm targets a point strictly inside its reachable area (not on the edge). Generically, how many joint solutions exist?",
        ("One", "Two (elbow up and elbow down)", "Infinitely many"), 1,
        "There are two mirror-image elbow configurations that reach the same point.",
    ),
    # --- 7. Sensors and estimation -------------------------------------------
    Lesson(
        "sense-noise", "sensing", "Averaging noise",
        "Random sensor noise has a standard deviation σ. Averaging N independent readings reduces it.",
        "By what factor does the standard deviation shrink when you average N independent readings?",
        ("√N", "N", "It does not change"), 0,
        "The averaged noise is σ/√N, so you need four times the readings to halve the noise.",
    ),
    Lesson(
        "sense-gyro", "sensing", "Gyro drift",
        "A gyroscope measures angular velocity. To get an angle you integrate it over time.",
        "A gyro has a small constant bias. What happens to the angle you compute by integrating it?",
        ("It drifts, with error growing over time", "It has a small constant error", "Nothing; integration cancels bias"), 0,
        "Integrating a constant bias gives an error that grows linearly with time.",
    ),
    Lesson(
        "sense-accel", "sensing", "Accelerometer tilt",
        "An accelerometer can measure tilt from the direction of gravity, but it also feels the robot's own accelerations.",
        "When is an accelerometer's tilt estimate least reliable?",
        ("When the robot is stationary", "During vibration and rapid movement", "When gravity is present"), 1,
        "Motion adds acceleration on top of gravity and corrupts the tilt reading.",
    ),
    Lesson(
        "sense-complementary", "sensing", "Complementary filter",
        "A complementary filter: angle = 0.98 × (angle + gyro × dt) + 0.02 × accel_angle.",
        "Why blend a gyro with an accelerometer?",
        ("The gyro is accurate short-term but drifts; the accelerometer is noisy but does not drift", "Both sensors have identical errors, so blending doubles accuracy", "It halves the number of sensor readings needed"), 0,
        "Each sensor covers the other's weakness: gyro for fast changes, accelerometer as a slow anchor.",
    ),
    # --- 8. Simulation readiness ---------------------------------------------
    Lesson(
        "sim-state", "sim", "State",
        "A simulation tracks a system's state: the minimum set of numbers needed to predict its future given the inputs.",
        "For a simple pendulum, what is a sufficient state?",
        ("Time only", "Angle only", "Angle and angular velocity"), 2,
        "τ = Iα is second order in angle, so you need both angle and angular velocity.",
    ),
    Lesson(
        "sim-dt", "sim", "Time step",
        "Numerical integration approximates continuous time with steps of size dt.",
        "What does using a smaller dt generally do?",
        ("Improves accuracy but costs more computation", "Makes the result less accurate", "Has no effect on accuracy"), 0,
        "Smaller steps track the true motion more closely, at the price of more steps per simulated second.",
    ),
    Lesson(
        "sim-instability", "sim", "Integrator instability",
        "Explicit Euler integration always uses the state at the start of the step.",
        "What can happen when explicit Euler is used on a spring or pendulum with a large dt?",
        ("The energy can grow each step and the simulation blows up", "Nothing; results are exact", "The simulation slows down but stays accurate"), 0,
        "For oscillators, explicit Euler adds energy every step, so big steps can diverge. Fixes: smaller dt or a better integrator.",
    ),
)


LESSONS_BY_ID: dict[str, Lesson] = {lesson.id: lesson for lesson in LESSONS}
MODULE_IDS: tuple[str, ...] = tuple(m.id for m in MODULES)


def _validate() -> None:
    assert len(LESSONS_BY_ID) == len(LESSONS), "duplicate lesson ids"
    for lesson in LESSONS:
        assert lesson.module in MODULE_IDS, lesson.id
        assert len(lesson.options) == 3, lesson.id
        assert 0 <= lesson.correct < 3, lesson.id
    for module_id in MODULE_IDS:
        assert any(l.module == module_id for l in LESSONS), module_id


_validate()
