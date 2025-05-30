import numpy as np
import matplotlib.pyplot as plt

# Параметры
dt = 0.01
T = 2.0
time = np.arange(0, T, dt)

Kp, Ki, Kd = 1.2, 0.01, 0.5
setpoint = 10
reaction_factor = 1.0

wind_start = 0.8
wind_duration = 0.2
wind_force = -10.0

# Инициализация
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

    current_value += output * dt * reaction_factor

    if wind_start <= t < wind_start + wind_duration:
        current_value += wind_force * dt
        wind_log.append(wind_force)
    else:
        wind_log.append(0.0)

    value_log.append(current_value)

# Построение графика
plt.figure(figsize=(12, 6))
plt.plot(time, value_log, label="Угол (текущее значение)")
plt.axhline(setpoint, color="r", linestyle="--", label="Целевое значение")
plt.plot(time, wind_log, label="Порыв ветра", linestyle=":", color="purple")
plt.xlabel("Время (сек)")
plt.ylabel("Угол (градусы)")
plt.title("Модель реакции дрона на порыв ветра")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
