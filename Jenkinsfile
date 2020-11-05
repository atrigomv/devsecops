pipeline{
agent{ label "kali_slave" }

    stages{
        stage('Build'){
            steps{
                echo('Building...')
                sh 'whoami'
                sh 'hostname'
                sh 'sudo systemctl start docker'
                sh 'sudo docker pull secfigo/bandit'
                sh 'sudo docker pull pyupio/safety'
                sh 'pwd'
            }
        }
        stage('SCA'){
            steps{
                echo('Analyzing third parties libraries...')
                sh 'sudo docker run -i --rm pyupio/safety safety check > sca-output.json'
                sh 'sudo docker rmi pyupio/safety'
            }
        }
        stage('Test'){
            steps{
                echo('Testing...')
                sh returnStatus:true, script:'sudo docker run --user $(id -u):$(id -g) -v $(pwd):/src --rm secfigo/bandit bandit -r /src -f json -o /src/bandit-output.json'
                sh 'sudo docker rmi secfigo/bandit'
            }
        }
        stage('Deploy'){
            steps{
                echo('Deploy...')
                sh 'sudo systemctl stop docker'
                sh 'rm -rf caches'
                sh 'rm -rf remoting'
                echo('SCA Results')
                sh 'cat sca-output.json'
                echo('SAST Results:')
                sh 'cat bandit-output.json'
            }
        }
    }
}
