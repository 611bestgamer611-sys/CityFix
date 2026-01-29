pipeline {
    agent any
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'production'],
            description: 'Target deployment environment'
        )
        booleanParam(
            name: 'SKIP_TESTS',
            defaultValue: false,
            description: 'Skip test execution'
        )
        booleanParam(
            name: 'DEPLOY',
            defaultValue: true,
            description: 'Deploy after successful build'
        )
    }
    
    environment {
        DOCKER_REGISTRY = credentials('docker-registry-url')
        DOCKER_CREDENTIALS = credentials('docker-credentials')
        KUBECONFIG = credentials('k8s-config')
        SLACK_WEBHOOK = credentials('slack-webhook-url')
        PROJECT_NAME = 'CityFix'
        IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT.substring(0,7)}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "🔄 Checking out code from ${env.GIT_BRANCH}"
                    checkout scm
                }
                sh 'git log -1 --pretty=format:"%h - %an: %s"'
            }
        }
        
        stage('Environment Setup') {
            steps {
                script {
                    echo "🔧 Setting up environment for ${params.ENVIRONMENT}"
                    sh '''
                        echo "Branch: ${GIT_BRANCH}"
                        echo "Commit: ${GIT_COMMIT}"
                        echo "Build: ${BUILD_NUMBER}"
                        echo "Image Tag: ${IMAGE_TAG}"
                    '''
                }
            }
        }
        
        stage('Build Frontend') {
            steps {
                dir('src/CityFixUI') {
                    script {
                        echo "📦 Building frontend"
                        sh '''
                            npm ci
                            npm run build
                        '''
                    }
                }
            }
        }
        
        stage('Build Backend Services') {
            parallel {
                stage('Build AuthService') {
                    steps {
                        dir('src/AuthService') {
                            sh 'pip install -r requirements.txt'
                        }
                    }
                }
                stage('Build AdminService') {
                    steps {
                        dir('src/AdminService') {
                            sh 'pip install -r requirements.txt'
                        }
                    }
                }
                stage('Build TicketService') {
                    steps {
                        dir('src/TicketService') {
                            sh 'pip install -r requirements.txt'
                        }
                    }
                }
                stage('Build MediaService') {
                    steps {
                        dir('src/MediaService') {
                            sh 'pip install -r requirements.txt'
                        }
                    }
                }
                stage('Build GeoService') {
                    steps {
                        dir('src/GeoService') {
                            sh 'pip install -r requirements.txt'
                        }
                    }
                }
                stage('Build NotificationService') {
                    steps {
                        dir('src/NotificationService') {
                            sh 'pip install -r requirements.txt'
                        }
                    }
                }
                stage('Build Orchestrator') {
                    steps {
                        dir('src/Orchestrator') {
                            sh 'pip install -r requirements.txt'
                        }
                    }
                }
            }
        }
        
        stage('Tests') {
            when {
                expression { !params.SKIP_TESTS }
            }
            parallel {
                stage('Frontend Tests') {
                    steps {
                        dir('src/CityFixUI') {
                            script {
                                echo "🧪 Running frontend tests"
                                sh '''
                                    npm run lint || true
                                    npx tsc --noEmit || true
                                '''
                            }
                        }
                    }
                }
                stage('Backend Tests') {
                    steps {
                        script {
                            echo "🐍 Running backend tests"
                            def services = ['AuthService', 'AdminService', 'TicketService', 
                                          'MediaService', 'GeoService', 'NotificationService', 'Orchestrator']
                            services.each { service ->
                                dir("src/${service}") {
                                    sh """
                                        python3 -m py_compile main.py || true
                                        pytest --maxfail=1 -v || true
                                    """
                                }
                            }
                        }
                    }
                }
            }
        }
        
        stage('Lint & Code Quality') {
            parallel {
                stage('ESLint') {
                    steps {
                        dir('src/CityFixUI') {
                            sh 'npm run lint || true'
                        }
                    }
                }
                stage('Flake8') {
                    steps {
                        script {
                            sh '''
                                find src -name "*.py" -exec flake8 --max-line-length 100 {} + || true
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Docker Build') {
            steps {
                script {
                    echo "🐳 Building Docker images"
                    sh """
                        docker-compose build
                    """
                }
            }
        }
        
        stage('Docker Tag & Push') {
            when {
                expression { params.DEPLOY }
            }
            steps {
                script {
                    echo "📤 Pushing Docker images to registry"
                    sh """
                        echo \${DOCKER_CREDENTIALS_PSW} | docker login -u \${DOCKER_CREDENTIALS_USR} --password-stdin \${DOCKER_REGISTRY}
                        
                        docker tag cityfix-frontend \${DOCKER_REGISTRY}/cityfix/frontend:\${IMAGE_TAG}
                        docker tag cityfix-orchestrator \${DOCKER_REGISTRY}/cityfix/orchestrator:\${IMAGE_TAG}
                        docker tag cityfix-auth-service \${DOCKER_REGISTRY}/cityfix/auth-service:\${IMAGE_TAG}
                        docker tag cityfix-admin-service \${DOCKER_REGISTRY}/cityfix/admin-service:\${IMAGE_TAG}
                        docker tag cityfix-ticket-service \${DOCKER_REGISTRY}/cityfix/ticket-service:\${IMAGE_TAG}
                        docker tag cityfix-media-service \${DOCKER_REGISTRY}/cityfix/media-service:\${IMAGE_TAG}
                        docker tag cityfix-geo-service \${DOCKER_REGISTRY}/cityfix/geo-service:\${IMAGE_TAG}
                        docker tag cityfix-notification-service \${DOCKER_REGISTRY}/cityfix/notification-service:\${IMAGE_TAG}
                        
                        docker push \${DOCKER_REGISTRY}/cityfix/frontend:\${IMAGE_TAG}
                        docker push \${DOCKER_REGISTRY}/cityfix/orchestrator:\${IMAGE_TAG}
                        docker push \${DOCKER_REGISTRY}/cityfix/auth-service:\${IMAGE_TAG}
                        docker push \${DOCKER_REGISTRY}/cityfix/admin-service:\${IMAGE_TAG}
                        docker push \${DOCKER_REGISTRY}/cityfix/ticket-service:\${IMAGE_TAG}
                        docker push \${DOCKER_REGISTRY}/cityfix/media-service:\${IMAGE_TAG}
                        docker push \${DOCKER_REGISTRY}/cityfix/geo-service:\${IMAGE_TAG}
                        docker push \${DOCKER_REGISTRY}/cityfix/notification-service:\${IMAGE_TAG}
                        
                        docker logout \${DOCKER_REGISTRY}
                    """
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            when {
                expression { params.DEPLOY }
            }
            steps {
                script {
                    echo "🚀 Deploying to ${params.ENVIRONMENT}"
                    sh """
                        export KUBECONFIG=\${KUBECONFIG}
                        kubectl config use-context ${params.ENVIRONMENT}
                        
                        kubectl set image deployment/frontend frontend=\${DOCKER_REGISTRY}/cityfix/frontend:\${IMAGE_TAG} -n cityfix
                        kubectl set image deployment/orchestrator orchestrator=\${DOCKER_REGISTRY}/cityfix/orchestrator:\${IMAGE_TAG} -n cityfix
                        kubectl set image deployment/auth-service auth-service=\${DOCKER_REGISTRY}/cityfix/auth-service:\${IMAGE_TAG} -n cityfix
                        kubectl set image deployment/admin-service admin-service=\${DOCKER_REGISTRY}/cityfix/admin-service:\${IMAGE_TAG} -n cityfix
                        kubectl set image deployment/ticket-service ticket-service=\${DOCKER_REGISTRY}/cityfix/ticket-service:\${IMAGE_TAG} -n cityfix
                        kubectl set image deployment/media-service media-service=\${DOCKER_REGISTRY}/cityfix/media-service:\${IMAGE_TAG} -n cityfix
                        kubectl set image deployment/geo-service geo-service=\${DOCKER_REGISTRY}/cityfix/geo-service:\${IMAGE_TAG} -n cityfix
                        kubectl set image deployment/notification-service notification-service=\${DOCKER_REGISTRY}/cityfix/notification-service:\${IMAGE_TAG} -n cityfix
                        
                        kubectl rollout status deployment/orchestrator -n cityfix --timeout=5m
                        kubectl rollout status deployment/frontend -n cityfix --timeout=5m
                    """
                }
            }
        }
        
        stage('Smoke Tests') {
            when {
                expression { params.DEPLOY }
            }
            steps {
                script {
                    echo "🔥 Running smoke tests"
                    sh """
                        # Wait for deployment to stabilize
                        sleep 30
                        
                        # Get service URL based on environment
                        if [ "${params.ENVIRONMENT}" = "production" ]; then
                            API_URL="https://api.cityfix.example.com"
                        elif [ "${params.ENVIRONMENT}" = "staging" ]; then
                            API_URL="https://api-staging.cityfix.example.com"
                        else
                            API_URL="http://localhost:8000"
                        fi
                        
                        # Health check
                        curl -f \${API_URL}/health || exit 1
                        
                        echo "✅ Smoke tests passed"
                    """
                }
            }
        }
    }
    
    post {
        success {
            script {
                echo "✅ Build successful!"
                sh """
                    curl -X POST \${SLACK_WEBHOOK} \
                        -H 'Content-Type: application/json' \
                        -d '{
                            "text": "✅ CityFix Build #${env.BUILD_NUMBER} SUCCESS",
                            "blocks": [
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": "*Build Successful* 🎉\\n*Branch:* ${env.GIT_BRANCH}\\n*Environment:* ${params.ENVIRONMENT}\\n*Build:* #${env.BUILD_NUMBER}"
                                    }
                                }
                            ]
                        }' || true
                """
            }
        }
        failure {
            script {
                echo "❌ Build failed!"
                sh """
                    curl -X POST \${SLACK_WEBHOOK} \
                        -H 'Content-Type: application/json' \
                        -d '{
                            "text": "❌ CityFix Build #${env.BUILD_NUMBER} FAILED",
                            "blocks": [
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": "*Build Failed* ❌\\n*Branch:* ${env.GIT_BRANCH}\\n*Environment:* ${params.ENVIRONMENT}\\n*Build:* #${env.BUILD_NUMBER}\\n*Check:* ${env.BUILD_URL}"
                                    }
                                }
                            ]
                        }' || true
                """
            }
        }
        always {
            cleanWs()
        }
    }
}
