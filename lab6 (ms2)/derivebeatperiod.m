
clear all
[sig fs] = audioread('MJ_BI_seg.wav');
x1 = sig(:,1);
x2 = sig(:,2);
x = sig;
N = 44100*5; % 20 ms of  sample given fs = 44100
start_sam =5474330;

% Instantaneous energy in 20 ms
for i= start_sam:start_sam+N
    for n = 1:N
        y(n)= x(i,1).^2;% energy
        r(n)= x(i,1);
    end
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
    threshold(i) = y(i)/s(i);
    subtracted(i)=y(i)-threshold(i);
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
title('Before filter - Stay Beat it');
% produce sound
sound(subtracted, fs)
disp('Playing the filter music') 
