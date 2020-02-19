function writer(cellIn, file)

fh = fopen(file, 'a+');

for i=1:length(cellIn)
    fprintf(fh, cellIn{i});
    fprintf(fh, '\n');
end

fclose(fh);
end

