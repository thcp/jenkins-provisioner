# jenkins-provisioner
Jenkins server provisioner for systems where docker isn't a option due to lack of sudo/root permission.

### Features

- Auto provision new master node by testing next available port.
- really basic self restart process for each instance.

### Todo
- [x] Deploy
- [ ] Remove 
- [ ] stop
- [ ] start
- [ ] restart
- [ ] status
- [ ] backup
- [ ] Update Nginx redirect
- [ ] proper log handling


### Usage

#### Deploying new master server

[![asciicast](https://asciinema.org/a/YNBcLat3XN7Ax5rU649z73LMg.svg)](https://asciinema.org/a/YNBcLat3XN7Ax5rU649z73LMg)
