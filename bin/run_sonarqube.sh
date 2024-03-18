#!/bin/bash

docker pull sonarqube

if ! docker ps -q filter "name=sonarqube" 2>/dev/null; then
  docker run -d \
    --name sonarqube \
    -p 9000:9000 \
    sonarqube
fi

echo "Waiting for SonarQube..."
until curl -s http://localhost:9000/api/system/status | grep -o '"status":"UP"' > /dev/null; do
    sleep 5
done
echo "SonarQube is ready."

echo "Executing code analysis for $(pwd)/jobberwocky..."
docker run --rm \
  --name sonarqube-scanner \
  -e SONAR_HOST_URL=http://sonarqube:9000 \
  -e SONAR_LOGIN=admin \
  -e SONAR_PASSWORD=admin \
  -v "$(pwd)/jobberwocky:/usr/src" \
  --link sonarqube \
  sonarsource/sonar-scanner-cli

#docker stop sonarqube
#docker rm sonarqube
