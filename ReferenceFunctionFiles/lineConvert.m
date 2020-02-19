function cellIn = lineConvert(cellIn, arrayIn, block)

cellIn{block} = '';
for i=1:length(arrayIn(block, :))
    
    if ~isnan(arrayIn(block,i))
        cellIn{block} = [cellIn{block} num2str(arrayIn(block,i)) '\t'];
    end

end

if strcmp(cellIn{block},'')
    cellIn{block} = '*';
end

end