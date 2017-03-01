%Lab 5 - Ex 5a: 4-taps moving average filter
% inefficient way 
clear all
[sig fs] = audioread('bgs.wav');
% Add noise to music
x = sig + 0.2*rand(size(sig));
% Plot the signal 
figure(1);
clf;
plot(x);
xlabel('Sample no');
ylabel('Signal (v)');
title('Stay Alive Music');
% Filter music with moving average filter 
t = 20; % tapsize
N = size(x); 
for i= t:N
    temp = 0;
    for j = 0:t-1
        temp = temp + x(i-j); 
    end
    y(i)= temp/t;
end
% Play the original & then the filtered sound 
sound(x, fs)
disp('Playing the original - press return when finished')
pause; 
sound(y, fs)
disp('Playing the filter music') 