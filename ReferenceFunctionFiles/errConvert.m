function cellIn = errConvert(cellIn, errsIn, block)

cellIn{block} = '';
for i=1:length(errsIn(block, :))
    
    if ~isnan(errsIn{block,i})
        cellIn{block} = [cellIn{block} errsIn{block,i} '\t'];
    end

end

if strcmp(cellIn{block},'')
    cellIn{block} = '*';
end

end