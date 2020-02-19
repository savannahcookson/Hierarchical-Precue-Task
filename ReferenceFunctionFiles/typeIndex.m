function index = typeIndex(typeList, type)

for i = 1:length(typeList)
    if strcmpi(typeList{i},type)
        index=i;
    end
end
