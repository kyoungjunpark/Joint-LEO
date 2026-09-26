lambda = physconst('LightSpeed')/11.325e9;   % wavelength
rxarray = phased.URA([sqrt(36) sqrt(36)],lambda/2);

rxpos = getElementPosition(rxarray)/lambda;
rxpos(2:3,:) = rxpos(2:3,:)+3;

H = scatteringchanmtx([0;0;0],rxpos, [30;40], [30;40], 0.0000005);

angle(H)