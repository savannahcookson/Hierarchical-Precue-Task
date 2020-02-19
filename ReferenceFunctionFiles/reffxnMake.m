function [NOLC, NORC, NSLC, NSRC, HOLC, HORC, HSLC, HSRC, JOLC, JORC, JSLC, JSRC, BOLC, BORC, BSLC, BSRC, NOLS, NORS, NSLS, NSRS, HOLS, HORS, HSLS, HSRS, JOLS, JORS, JSLS, JSRS, BOLS, BORS, BSLS, BSRS, ERRS] = reffxnMake(acc, type, csi, subs, blocks)

for s = 1:length(subs)
    inFolder = [subs{s} '/s2/'];
    %mkdir(outFolder)
    NOLC = importdata([inFolder '0OL_C.1D']);
    NORC = importdata([inFolder '0OR_C.1D']);
    NSLC = importdata([inFolder '0SL_C.1D']);
    NSRC = importdata([inFolder '0SR_C.1D']);
    HOLC = importdata([inFolder '1HOL_C.1D']);
    HORC = importdata([inFolder '1HOR_C.1D']);
    HSLC = importdata([inFolder '1HSL_C.1D']);
    HSRC = importdata([inFolder '1HSR_C.1D']);
    JOLC = importdata([inFolder '1JOL_C.1D']);
    JORC = importdata([inFolder '1JOR_C.1D']);
    JSLC = importdata([inFolder '1JSL_C.1D']);
    JSRC = importdata([inFolder '1JSR_C.1D']);
    BOLC = importdata([inFolder '2OL_C.1D']);
    BORC = importdata([inFolder '2OR_C.1D']);
    BSLC = importdata([inFolder '2SL_C.1D']);
    BSRC = importdata([inFolder '2SR_C.1D']);
    NOLS = importdata([inFolder '0OL_S.1D']);
    NORS = importdata([inFolder '0OR_S.1D']);
    NSLS = importdata([inFolder '0SL_S.1D']);
    NSRS = importdata([inFolder '0SR_S.1D']);
    HOLS = importdata([inFolder '1HOL_S.1D']);
    HORS = importdata([inFolder '1HOR_S.1D']);
    HSLS = importdata([inFolder '1HSL_S.1D']);
    HSRS = importdata([inFolder '1HSR_S.1D']);
    JOLS = importdata([inFolder '1JOL_S.1D']);
    JORS = importdata([inFolder '1JOR_S.1D']);
    JSLS = importdata([inFolder '1JSL_S.1D']);
    JSRS = importdata([inFolder '1JSR_S.1D']);
    BOLS = importdata([inFolder '2OL_S.1D']);
    BORS = importdata([inFolder '2OR_S.1D']);
    BSLS = importdata([inFolder '2SL_S.1D']);
    BSRS = importdata([inFolder '2SR_S.1D']);
    
    NOLC = NOLC(2:end,:);
    NORC = NORC(2:end,:);
    NSLC = NSLC(2:end,:);
    NSRC = NSRC(2:end,:);
    HOLC = HOLC(2:end,:);
    HORC = HORC(2:end,:);
    HSLC = HSLC(2:end,:);
    HSRC = HSRC(2:end,:);
    JOLC = JOLC(2:end,:);
    JORC = JORC(2:end,:);
    JSLC = JSLC(2:end,:);
    JSRC = JSRC(2:end,:);
    BOLC = BOLC(2:end,:);
    BORC = BORC(2:end,:);
    BSLC = BSLC(2:end,:);
    BSRC = BSRC(2:end,:);
    NOLS = NOLS(2:end,:);
    NORS = NORS(2:end,:);
    NSLS = NSLS(2:end,:);
    NSRS = NSRS(2:end,:);
    HOLS = HOLS(2:end,:);
    HORS = HORS(2:end,:);
    HSLS = HSLS(2:end,:);
    HSRS = HSRS(2:end,:);
    JOLS = JOLS(2:end,:);
    JORS = JORS(2:end,:);
    JSLS = JSLS(2:end,:);
    JSRS = JSRS(2:end,:);
    BOLS = BOLS(2:end,:);
    BORS = BORS(2:end,:);
    BSLS = BSLS(2:end,:);
    BSRS = BSRS(2:end,:);
    ERRS = {};
    for b = 1:blocks(s)
        currTrial = (s-1)*32*16+(b-1)*32+1;
        
        curracc = acc(currTrial:currTrial+31);
        currtype = type(currTrial:currTrial+31);
        currcsi = csi(currTrial:currTrial+31);
            
        [NOLC, NORC, NSLC, NSRC, HOLC, HORC, HSLC, HSRC, JOLC, JORC, JSLC, JSRC, BOLC, BORC, BSLC, BSRC, NOLS, NORS, NSLS, NSRS, HOLS, HORS, HSLS, HSRS, JOLS, JORS, JSLS, JSRS, BOLS, BORS, BSLS, BSRS, ERRS] = errCatch(curracc, currtype, currcsi, b, NOLC, NORC, NSLC, NSRC, HOLC, HORC, HSLC, HSRC, JOLC, JORC, JSLC, JSRC, BOLC, BORC, BSLC, BSRC, NOLS, NORS, NSLS, NSRS, HOLS, HORS, HSLS, HSRS, JOLS, JORS, JSLS, JSRS, BOLS, BORS, BSLS, BSRS, ERRS);
        
    end
    
    functionwrite(subs{s}, blocks(s), NOLC, NORC, NSLC, NSRC, HOLC, HORC, HSLC, HSRC, JOLC, JORC, JSLC, JSRC, BOLC, BORC, BSLC, BSRC, NOLS, NORS, NSLS, NSRS, HOLS, HORS, HSLS, HSRS, JOLS, JORS, JSLS, JSRS, BOLS, BORS, BSLS, BSRS, ERRS);
    
end

end