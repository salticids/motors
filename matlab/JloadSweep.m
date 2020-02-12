t = 0:0.05:10;
Jload = 0:0.1:1;
data = zeros(length(t), length(Jload));
for i = 1:length(Jload)
    data(:,i) = step(feedback(MotorSS(Jload(i)), 1), t);
end
mesh(Jload, t, data)
view([45,30])
xlabel('Load inertia J_{load} (kg m^2)')
ylabel('Time (s)')
zlabel('Rotor angle \theta(t) (radians)')