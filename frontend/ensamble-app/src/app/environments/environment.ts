export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000', // TODO: API Gateway URL
  microservices: {
    eventos: 'http://localhost:8001',
    musicos: 'http://localhost:8002'
  }
};