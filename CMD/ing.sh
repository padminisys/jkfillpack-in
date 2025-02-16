kubectl create ingress website --class=nginx --rule="jkfillpack.in/*=website:80,tls=jkfillpack-in-web-tls"
