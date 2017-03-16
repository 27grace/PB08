% Lab 2 - Ex 4 - Two drum beats

function [Y] = plot_spec_dB(sig, fs)

% Function to plot frequency spectrum of sig in dB
%   usage: 
%           plot_spectrum_dB(sig, fs)
%
% author: Peter YK Cheung, 17 Jan 2017
    magnitude = abs(fft(sig));
    N = length(sig);
    df = fs/N; 
    f = 0:df:fs/2;
    m_max = max(magnitude);
    Y = 20*log10(magnitude(1:length(f))/m_max);
    plot(f, Y)
       axis([0 fs/2 -60 0]);
    xlabel('\fontsize{14}frequency (Hz)')
    ylabel('\fontsize{14}Magnitude (dB)');
    title('\fontsize{16}Plot spectrum dB');
end

% 
clear all 
fs = 44100;
[sig fs] = audioread('MJ_Beat_It.mp3');
sound(sig, fs)
figure(1)
plot(sig);
xlabel('Sample no');
ylabel('Signal (v)');
title('bgs.wav');

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