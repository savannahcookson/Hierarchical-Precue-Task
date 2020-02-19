function functionwrite(sub, blocks, NOLC, NORC, NSLC, NSRC, HOLC, HORC, HSLC, HSRC, JOLC, JORC, JSLC, JSRC, BOLC, BORC, BSLC, BSRC, NOLS, NORS, NSLS, NSRS, HOLS, HORS, HSLS, HSRS, JOLS, JORS, JSLS, JSRS, BOLS, BORS, BSLS, BSRS, ERRS)

mkdir([sub '/stim']);

    NOLCcell = {};
    NORCcell = {};
    NSLCcell = {};
    NSRCcell = {};
    HOLCcell = {};
    HORCcell = {};
    HSLCcell = {};
    HSRCcell = {};
    JOLCcell = {};
    JORCcell = {};
    JSLCcell = {};
    JSRCcell = {};
    BOLCcell = {};
    BORCcell = {};
    BSLCcell = {};
    BSRCcell = {};
    NOLScell = {};
    NORScell = {};
    NSLScell = {};
    NSRScell = {};
    HOLScell = {};
    HORScell = {};
    HSLScell = {};
    HSRScell = {};
    JOLScell = {};
    JORScell = {};
    JSLScell = {};
    JSRScell = {};
    BOLScell = {};
    BORScell = {};
    BSLScell = {};
    BSRScell = {};
    ERRScell = {};

for i=1:blocks
    
    NOLCcell = lineConvert(NOLCcell, NOLC, i);
    NORCcell = lineConvert(NORCcell, NORC, i);
    NSLCcell = lineConvert(NSLCcell, NSLC, i);
    NSRCcell = lineConvert(NSRCcell, NSRC, i);
    HOLCcell = lineConvert(HOLCcell, HOLC, i);
    HORCcell = lineConvert(HORCcell, HORC, i);
    HSLCcell = lineConvert(HSLCcell, HSLC, i);
    HSRCcell = lineConvert(HSRCcell, HSRC, i);
    JOLCcell = lineConvert(JOLCcell, JOLC, i);
    JORCcell = lineConvert(JORCcell, JORC, i);
    JSLCcell = lineConvert(JSLCcell, JSLC, i);
    JSRCcell = lineConvert(JSRCcell, JSRC, i);
    BOLCcell = lineConvert(BOLCcell, BOLC, i);
    BORCcell = lineConvert(BORCcell, BORC, i);
    BSLCcell = lineConvert(BSLCcell, BSLC, i);
    BSRCcell = lineConvert(BSRCcell, BSRC, i);
    NOLScell = lineConvert(NOLScell, NOLS, i);
    NORScell = lineConvert(NORScell, NORS, i);
    NSLScell = lineConvert(NSLScell, NSLS, i);
    NSRScell = lineConvert(NSRScell, NSRS, i);
    HOLScell = lineConvert(HOLScell, HOLS, i);
    HORScell = lineConvert(HORScell, HORS, i);
    HSLScell = lineConvert(HSLScell, HSLS, i);
    HSRScell = lineConvert(HSRScell, HSRS, i);
    JOLScell = lineConvert(JOLScell, JOLS, i);
    JORScell = lineConvert(JORScell, JORS, i);
    JSLScell = lineConvert(JSLScell, JSLS, i);
    JSRScell = lineConvert(JSRScell, JSRS, i);
    BOLScell = lineConvert(BOLScell, BOLS, i);
    BORScell = lineConvert(BORScell, BORS, i);
    BSLScell = lineConvert(BSLScell, BSLS, i);
    BSRScell = lineConvert(BSRScell, BSRS, i);
    ERRScell = errConvert(ERRScell, ERRS, i);
    
end

writer(NOLCcell, [sub '/stim/0OL_C.1D']);
writer(NORCcell, [sub '/stim/0OR_C.1D']);
writer(NSLCcell, [sub '/stim/0SL_C.1D']);
writer(NSRCcell, [sub '/stim/0SR_C.1D']);
writer(HOLCcell, [sub '/stim/1HOL_C.1D']);
writer(HORCcell, [sub '/stim/1HOR_C.1D']);
writer(HSLCcell, [sub '/stim/1HSL_C.1D']);
writer(HSRCcell, [sub '/stim/1HSR_C.1D']);
writer(JOLCcell, [sub '/stim/1JOL_C.1D']);
writer(JORCcell, [sub '/stim/1JOR_C.1D']);
writer(JSLCcell, [sub '/stim/1JSL_C.1D']);
writer(JSRCcell, [sub '/stim/1JSR_C.1D']);
writer(BOLCcell, [sub '/stim/2OL_C.1D']);
writer(BORCcell, [sub '/stim/2OR_C.1D']);
writer(BSLCcell, [sub '/stim/2SL_C.1D']);
writer(BSRCcell, [sub '/stim/2SR_C.1D']);
writer(NOLScell, [sub '/stim/0OL_S.1D']);
writer(NORScell, [sub '/stim/0OR_S.1D']);
writer(NSLScell, [sub '/stim/0SL_S.1D']);
writer(NSRScell, [sub '/stim/0SR_S.1D']);
writer(HOLScell, [sub '/stim/1HOL_S.1D']);
writer(HORScell, [sub '/stim/1HOR_S.1D']);
writer(HSLScell, [sub '/stim/1HSL_S.1D']);
writer(HSRScell, [sub '/stim/1HSR_S.1D']);
writer(JOLScell, [sub '/stim/1JOL_S.1D']);
writer(JORScell, [sub '/stim/1JOR_S.1D']);
writer(JSLScell, [sub '/stim/1JSL_S.1D']);
writer(JSRScell, [sub '/stim/1JSR_S.1D']);
writer(BOLScell, [sub '/stim/2OL_S.1D']);
writer(BORScell, [sub '/stim/2OR_S.1D']);
writer(BSLScell, [sub '/stim/2SL_S.1D']);
writer(BSRScell, [sub '/stim/2SR_S.1D']);
writer(ERRScell, [sub '/stim/ERRS.1D']);

end