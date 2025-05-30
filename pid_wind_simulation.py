import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Time settings
dt = 0.01
T = 5.0
time = np.arange(0, T, dt)

# Default PID and wind parameters
default_Kp = 1.2
default_Ki = 0.01
default_Kd = 0.5
default_wind_start = 1.0
default_wind_duration = 0.5
default_wind_force = -10.0
setpoint = 10


# Simulation function
def simulate(Kp, Ki, Kd, wind_start, wind_duration, wind_force):
    current_value = 0
    prev_error = 0
    integral = 0
    value_log = []
    wind_log = []

    for t in time:
        error = setpoint - current_value
        integral += error * dt
        derivative = (error - prev_error) / dt
        output = Kp * error + Ki * integral + Kd * derivative
        prev_error = error

        current_value += output * dt

        if wind_start <= t < wind_start + wind_duration:
            current_value += wind_force * dt
            wind_log.append(wind_force)
        else:
            wind_log.append(0.0)

        value_log.append(current_value)

    return np.array(value_log), np.array(wind_log)


# Initial simulation
value_log, wind_log = simulate(
    default_Kp,
    default_Ki,
    default_Kd,
    default_wind_start,
    default_wind_duration,
    default_wind_force,
)

# Create plot
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(left=0.1, bottom=0.4)
(l1,) = ax.plot(time, value_log, label="Leņķis (aktuālā vērtība)", color="blue")
(l2,) = ax.plot(time, wind_log, label="Vēja brāzma", linestyle=":", color="purple")
ax.axhline(setpoint, color="red", linestyle="--", label="Mērķis")
ax.set_xlabel("Laiks (s)")
ax.set_ylabel("Leņķis (°)")
ax.set_title("PID reakcija ar vēja brāzmu")
ax.legend()
ax.grid(True)

# Slider positions
axcolor = "lightgoldenrodyellow"
slider_positions = {
    "Kp": plt.axes([0.15, 0.30, 0.7, 0.03], facecolor=axcolor),
    "Ki": plt.axes([0.15, 0.25, 0.7, 0.03], facecolor=axcolor),
    "Kd": plt.axes([0.15, 0.20, 0.7, 0.03], facecolor=axcolor),
    "wind_force": plt.axes([0.15, 0.15, 0.7, 0.03], facecolor=axcolor),
    "wind_start": plt.axes([0.15, 0.10, 0.7, 0.03], facecolor=axcolor),
    "wind_duration": plt.axes([0.15, 0.05, 0.7, 0.03], facecolor=axcolor),
}

# Sliders
sKp = Slider(slider_positions["Kp"], "Kp", 0.0, 5.0, valinit=default_Kp)
sKi = Slider(slider_positions["Ki"], "Ki", 0.0, 1.0, valinit=default_Ki)
sKd = Slider(slider_positions["Kd"], "Kd", 0.0, 2.0, valinit=default_Kd)
sWind = Slider(
    slider_positions["wind_force"],
    "Vēja spēks",
    -20.0,
    20.0,
    valinit=default_wind_force,
)
sStart = Slider(
    slider_positions["wind_start"],
    "Vēja sākums",
    0.0,
    T - 0.1,
    valinit=default_wind_start,
)
sDuration = Slider(
    slider_positions["wind_duration"],
    "Vēja ilgums",
    0.05,
    2.0,
    valinit=default_wind_duration,
)


# Update function
def update(val):
    new_value_log, new_wind_log = simulate(
        sKp.val, sKi.val, sKd.val, sStart.val, sDuration.val, sWind.val
    )
    l1.set_ydata(new_value_log)
    l2.set_ydata(new_wind_log)
    fig.canvas.draw_idle()


# Connect sliders to update
sKp.on_changed(update)
sKi.on_changed(update)
sKd.on_changed(update)
sWind.on_changed(update)
sStart.on_changed(update)
sDuration.on_changed(update)

plt.show()
