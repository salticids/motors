function Plant = MotorSS(Jload)

if nargin < 1
    Jload = 0;
end

L = 5e-3; % total motor inductance
R = 5; % coil resistance
kb = 12.5e-2; % back emf/speed
ki = 15; % torque/current
J = 3e-2 + Jload; % total inertia
b = 1e-2; % (friction torque)/speed
A = [0, 1, 0; 0, -b/J, ki/J; 0, -kb/L, -R/L];
B = [0; 0; 1/L];
C = [1, 0, 0];
D = 0;
Plant = ss(A, B, C, D);

set(Plant, 'InputName', 'volts', 'OutputName', '\theta')
set(Plant, 'StateName', {'\theta', '\omega', 'i'})
set(Plant, 'Notes', 'Small DC servomotor')

end

