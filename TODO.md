# TODO

- [ ] use ansible for production deploys (over Docker Swarm to minimize operational complexity)
- [ ] add in token-based (JWT) authentication to the API
- [ ] add user creation flow and endpoints
- [ ] use flask-security to define admin vs user roles.
- [ ] lock down access to `rq` dashboard for admins only
- [ ] create a service to run `rqscheduler` and configure via ansible
- [ ] add endpoints to query job status
- [ ] add support for other data integrations
