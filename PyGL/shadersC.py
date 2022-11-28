vertexShader = """
#version 440

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 cColor;

out vec3 miColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = projection * view * model * vec4(position.x, position.y, position.z, 1.0);
    miColor = cColor;
}
"""

fragmentShader ="""
#version 440

layout(location = 0) out vec4 fragColor;

in vec3 miColor;

void main()
{
    float newColX = mod(12345.4321 * miColor.x, 1);
    float newColY = mod(12345.4321 * miColor.y, 1);
    float newColZ = mod(12345.4321 * miColor.z, 1);

    fragColor = vec4(newColX, newColY, newColZ, 1);
}
"""