
clear all
[sig fs] = audioread('BeeGees.wav');
x = sig;
% Instantaneous energy
t = 1; % tapsize
N = 44100*0.02; % 20ms of  sample given fs = 44100
for i= t:N
    temp = 0;
    for j = 0:t-1
        temp = temp + x(i-j).^2; % energy
    end
    y(i)= temp/t;
end

% Steady state local
t = 100; % tapsize
for i= t:N
    temp = 0;
    for j = 0:t-1
        temp = temp + x(i-j).^2; % energy
    end
    s(i)= temp/t;
end

% Variance calculation 


% Plot the signal 
figure(1);
clf;
plot(y);
hold on 
plot(s);
hold on
xlabel('Sample no');
ylabel('Energy (sig^2)');
title('Before filter - Stay Alive Music');
% produce sound
sound(y, fs)
disp('Playing the filter music') 