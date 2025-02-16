sudo /usr/local/bin/deployhook \
  --domain=jkfillpack.in \
  --cert_path=/etc/letsencrypt/live/jkfillpack.in \
  --haproxy_pem=/etc/haproxy/certs/jkfillpack.in.pem \
  --haproxy_cfg=/etc/haproxy/haproxy.cfg \
  --mapping=/etc/letsencrypt/mapping.json
