
clear all
[sig fs] = audioread('BeeGees.wav');
x = sig;
N = 44100*0.02; % 20 ms of  sample given fs = 44100

% Instantaneous energy in 20 ms
for i= 1:N
    y(i)= x(i)^2;% energy
end

% Beat threshold calculation 
t = 100; % tapsize
beta = 1.5;
alpha = 0.0025;
for i= t:N
    temp = 0;
    for j = 0:t-1
        temp = temp + y(i-j); % average energy
    end
    s(i)= temp/t;
    % calculate threshold constant, b
    temp = 0;
    for j = 0:t-1
        temp = temp + (y(i)-s(i))^2; % variance
    end
    v(i)= temp/t;
    b(i)= beta - alpha*v(i);
    % combining threshold constant + average
    threshold(i) = b(i)*s(i);
    subtracted(i) = y(i) - threshold(i);
end


% Plot the signal 
figure(1);
clf;
plot(y);
hold on 
plot(threshold);
hold on
xlabel('Sample no');
ylabel('Energy (sig^2)');
title('Before filter - Stay Alive Music');
% produce sound
sound(subtracted, fs)
disp('Playing the filter music') 