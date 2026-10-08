% The same three calculations as analysis.py, in MATLAB syntax (runs in MATLAB or GNU Octave).
fs = 200;
t = 0:1/fs:10-1/fs;                          % row vector, 1-based indexing from here on

speed = 60 + 8*sin(2*pi*0.1*t);
vib   = sin(2*pi*12.5*t) + 0.4*sin(2*pi*31*t) + 0.1*sin(97*t);
temp  = 25 + 500*exp(-t/3.2) + 0.5*sin(5*t);

distance = trapz(t, speed);                  % note the argument order: x first

n = numel(vib);
spec = abs(fft(vib));
spec = spec(1:floor(n/2)+1);                 % one-sided, like numpy.fft.rfft
freqs = (0:floor(n/2)) * fs / n;
[~, i] = max(spec(2:end));                   % skip DC
dominant = freqs(i + 1);

p = polyfit(t, log(temp - 25), 1);
tau = -1 / p(1);

fprintf('distance_m=%.4f\n', distance);
fprintf('dominant_hz=%.4f\n', dominant);
fprintf('tau_s=%.4f\n', tau);
fprintf('mean_speed=%.4f\n', mean(speed));
