t=0:0.001:1;
vo=3;
w=100;
v=vo*cos(w*t);
plot2d(t,v);
io=1;
i=io*sin(w*t);
plot2d(t,i);

