function [NOLC, NORC, NSLC, NSRC, HOLC, HORC, HSLC, HSRC, JOLC, JORC, JSLC, JSRC, BOLC, BORC, BSLC, BSRC, NOLS, NORS, NSLS, NSRS, HOLS, HORS, HSLS, HSRS, JOLS, JORS, JSLS, JSRS, BOLS, BORS, BSLS, BSRS, ERRS] = errCatch(acc, types, csi, b, NOLC, NORC, NSLC, NSRC, HOLC, HORC, HSLC, HSRC, JOLC, JORC, JSLC, JSRC, BOLC, BORC, BSLC, BSRC, NOLS, NORS, NSLS, NSRS, HOLS, HORS, HSLS, HSRS, JOLS, JORS, JSLS, JSRS, BOLS, BORS, BSLS, BSRS, ERRS)

    typeList = {'0OL', '0OR', '0SL', '0SR', '1HOL', '1HOR', '1HSL', '1HSR', '1JOL', '1JOR', '1JSL', '1JSR', '2OL', '2OR', '2SL', '2SR'}; 
    typeCheck = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    
    if length(acc) ~= length(types)
        fprintf('Sorry, your accuracy and type data do not align')
    else
        
        for i=1:length(acc)
            
            type = types{i};
            
            if acc(i) == 0
                if typeCheck(typeIndex(typeList,type)) == 0
                    round = 1;
                else
                    round = 2;
                end

                switch type
                    case '0OL'
                        errtime = NOLC(b,round);
                        NOLC(b,round) = NaN;
                        NOLS(b,round) = NaN;
                    case '0OR'
                        errtime = NORC(b,round);
                        NORC(b,round) = NaN;
                        NORS(b,round) = NaN;
                    case '0SL'
                        errtime = NSLC(b,round);
                        NSLC(b,round) = NaN;
                        NSLS(b,round) = NaN;
                    case '0SR'
                        errtime = NSRC(b,round);
                        NSRC(b,round) = NaN;
                        NSRS(b,round) = NaN;
                    case '1HOL'
                        errtime = HOLC(b,round);
                        HOLC(b,round) = NaN;
                        HOLS(b,round) = NaN;
                    case '1HOR'
                        errtime = HORC(b,round);
                        HORC(b,round) = NaN;
                        HORS(b,round) = NaN;
                    case '1HSL'
                        errtime = HSLC(b,round);
                        HSLC(b,round) = NaN;
                        HSLS(b,round) = NaN;
                    case '1HSR'
                        errtime = HSRC(b,round);
                        HSRC(b,round) = NaN;
                        HSRS(b,round) = NaN;
                    case '1JOL'
                        errtime = JOLC(b,round);
                        JOLC(b,round) = NaN;
                        JOLS(b,round) = NaN;
                    case '1JOR'
                        errtime = JORC(b,round);
                        JORC(b,round) = NaN;
                        JORS(b,round) = NaN;
                    case '1JSL'
                        errtime = JSLC(b,round);
                        JSLC(b,round) = NaN;
                        JSLS(b,round) = NaN;
                    case '1JSR'
                        errtime = JSRC(b,round);
                        JSRC(b,round) = NaN;
                        JSRS(b,round) = NaN;
                    case '2OL'
                        errtime = BOLC(b,round);
                        BOLC(b,round) = NaN;
                        BOLS(b,round) = NaN;
                    case '2OR'
                        errtime = BORC(b,round);
                        BORC(b,round) = NaN;
                        BORS(b,round) = NaN;
                    case '2SL'
                        errtime = BSLC(b,round);
                        BSLC(b,round) = NaN;
                        BSLS(b,round) = NaN;
                    case '2SR'
                        errtime = BSRC(b,round);
                        BSRC(b,round) = NaN;
                        BSRS(b,round) = NaN;
                end
                errdur = csi(i);
                ERRS{b,i} = [num2str(errtime) ':' num2str(errdur + 1.9*2)];
            else
                ERRS{b,i} = NaN;
            

            end
            
            typeCheck(typeIndex(typeList,type)) = typeCheck(typeIndex(typeList,type)) + 1;
            
        end 
        
    end
        

end