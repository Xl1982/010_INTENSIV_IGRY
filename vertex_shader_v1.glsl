#version 330

// Время начала вспышки
uniform float time;

// (x, y) position passed in входные данные для шейдера Х и У
in vec2 in_pos;

// Velocity of particle Скорость частицы
in vec2 in_vel;

// Color of particle Цвет частицы
in vec3 in_color;

// Fade rate Скорость исчезновения частицы
in float in_fade_rate;

// Output the color to the fragment shader цвет частицы который будет передан в фргаментный шейдер
out vec4 color;


// основная функция шейдер
void main() {

    // Calculate alpha based on time and fade rate рассчет прозрачности и цвета на основе времени жизни
    float alpha = 1.0 - (in_fade_rate * time);
    if(alpha < 0.0) alpha = 0;

    // Set the RGBA color их того что к нам поступило устанавливаем све
    color = vec4(in_color[0], in_color[1], in_color[2], alpha);

    // Adjust velocity based on gravity имитация гравитации, каждую секунду скорость добавляет 10 процентов
    vec2 new_vel = in_vel;
    new_vel[1] -= time * 1.1;

    // Calculate a new position
    vec2 new_pos = in_pos + (time * new_vel);

    // Set the position. (x, y, z, w)
    gl_Position = vec4(new_pos, 0.0, 1);
}