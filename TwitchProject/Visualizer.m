data = [];
path = 'chatoutput';

% Loading data
for i = 0:14
    temp = dlmread(strcat(path,num2str(i),'.txt'),'\t');
    data = [data; temp];
end

freq = zeros(int32(max(data)) + 1,1);


for i = 1:(max(data))
    i
    temp = find(abs(data - i) < 20);
    count = length(temp);
    freq(i) = count;
end

plot(freq)