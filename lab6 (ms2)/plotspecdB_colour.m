% Lab 2 - Ex 4 - Two drum beats
% 
clear all 
fs = 44100;
[sig fs] = audioread('MJ_Beat_It.mp3');
figure(1)
plot(sig);
xlabel('Sample no');
ylabel('Signal (v)');
title('MJ_Beat_It.mp3');

% solution
T = 0.02;
N = fs*T;
E = [];
for i = 1:N:length(sig) - N + 1
    seg = sig(i: i + N - 1);
    E = [E seg'*seg];
end
% plot the energy graph and the peak values
figure(2);
clf;
x = 1:length(E);
plot(x, E)
xlabel('Segment number');
ylabel('Energy');
title('Energy')
hold on
% Find local maxima
[pks locs] = findpeaks(E);
plot(locs, pks, 'o');
hold off
figure(3)
plot_spec_dB(E, 1/T);