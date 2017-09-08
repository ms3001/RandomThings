data = [];
path = 'chatoutput';

% Loading data
for i = 64:85
    temp = dlmread(strcat(path,num2str(i),'.txt'),'\t');
    data = [data; temp];
end

freq = zeros(int32(max(data)) + 1,1);

% Generating activity graph
for i = 1:(max(data))
    temp = find(abs(data - i) < 20);
    count = length(temp);
    freq(i) = count;
end

plot(freq)
hold on;
plot(mean(freq)*ones(length(freq),1))
plot(tsmovavg(freq,'s',600,1))
plot(smooth(freq,600)*1.8)
% Finding peaks
