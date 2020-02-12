function PlantTF = MotorTF
L = 5e-3; % total motor inductance
R = 5; % coil resistance
kb = 12.5e-2; % back emf/speed
ki = 15; % torque/current
J = 3e-2; % total inertia
b = 1e-2; % torque/speed (due to friction)
Num = ki;
Den = conv([L, R],[J, b, 0])+[0, 0, kb*ki, 0];
PlantTF = tf(Num, Den);
end