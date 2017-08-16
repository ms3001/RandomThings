data = [];
path = 'shroud/chatoutput';

for i = 1:12
    
    temp = tdfread(,'\t');
    data = [data; temp];
    
end

data