%Lab 4 -Exercise 3: 3D display of roll and pitch angles w/ Filter
clear all
close('all')
pb = PyBench('COM5');
model = IMU_3D();
N = 50;
gx = 0; gy = 0;
theta_x = 0; theta_y = 0;
a = 0.8;
fig1 = figure(1);
tic;
while true
    for i = 1:N
        [p,r] = pb.get_accel();
        [x,y,z] = pb.get_gyro();
        dt = toc;
        tic;
        % calculating gyroscope angles
        gx = max(min(gx+x*dt, pi/2),-pi/2);
        gy = max(min(gy+y*dt,pi/2),-pi/2);
        % calculating using complementary filter
        theta_x = a*(theta_x+x*dt)+(1-a)*r;
        theta_y = a*(theta_y+y*dt)+(1-a)*p;
        % creating figures
        figure(fig1)
        clf(fig1);
        subplot(3,1,1);
        model.draw(fig1, p, r, 'Accelerometer');
        subplot(3, 1, 2);
        model.draw(fig1, gy, gx, 'Gyroscope');
        subplot(3, 1, 3);
        model.draw(fig1, theta_y, theta_x, 'Complementary Filter');
        pause(0.0001);
    end %for
end %while
